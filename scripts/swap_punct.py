import re
from pathlib import Path

tex_dir = Path('.')
files = [tex_dir / 'main_thesis.tex'] + list(tex_dir.glob('tex/*.tex')) + list(tex_dir.glob('library/*.tex'))

math_envs = ['equation', 'align', 'align\*', 'multline', 'gather', 'eqnarray', 'split']
verbatim_envs = ['verbatim', 'lstlisting', 'minted', 'Verbatim']

pat_verbatim = re.compile(r"\\begin\{(" + '|'.join(verbatim_envs) + r")\}.*?\\end\{\1\}", re.DOTALL)
pat_dollars_disp = re.compile(r"\$\$.*?\$\$", re.DOTALL)
pat_bracket = re.compile(r"\\\[.*?\\\]", re.DOTALL)
pat_envs = re.compile(r"\\begin\{(" + '|'.join(math_envs) + r")\}.*?\\end\{\1\}", re.DOTALL)
pat_dollars_inline = re.compile(r"(?<!\\)\$.*?(?<!\\)\$", re.DOTALL)
# comments: % not preceded by backslash
pat_comment = re.compile(r"(?<!\\)%.*")

made_changes = []
for f in files:
    if not f.exists():
        continue
    text = f.read_text(encoding='utf-8')
    orig = text
    # backup
    bak = f.with_suffix(f.suffix + '.bak')
    if not bak.exists():
        bak.write_text(orig, encoding='utf-8')

    masks = []
    def mask(pattern, s):
        def repl(m):
            masks.append(m.group(0))
            return f'__MASK{len(masks)-1}__'
        return pattern.sub(repl, s)

    # mask verbatim-like envs
    text = mask(pat_verbatim, text)
    # mask display math and math envs
    text = mask(pat_dollars_disp, text)
    text = mask(pat_bracket, text)
    text = mask(pat_envs, text)
    # mask inline math (after display math masked)
    text = mask(pat_dollars_inline, text)
    # mask comments (line by line)
    def mask_comments(s):
        res = []
        for line in s.splitlines(True):
            m = pat_comment.search(line)
            if m:
                masks.append(m.group(0))
                token = f'__MASK{len(masks)-1}__'
                line = line[:m.start()] + token + ("\n" if line.endswith('\n') else '')
            res.append(line)
        return ''.join(res)
    text = mask_comments(text)

    # do replacements in the remaining (unmasked) text
    text = text.replace('、', '，')
    text = text.replace('。', '．')

    # restore masks
    for i, content in enumerate(masks):
        text = text.replace(f'__MASK{i}__', content)

    if text != orig:
        f.write_text(text, encoding='utf-8')
        made_changes.append(str(f))

if made_changes:
    print('Modified files:')
    for m in made_changes:
        print(' -', m)
else:
    print('No changes made.')
