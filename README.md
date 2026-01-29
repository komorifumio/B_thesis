## latex
### main
texのテンプレートをブランチに分けて保存しています。
ダウンロードするか，以下の手順で利用してください。
1. このリポジトリに接続<br>
git remote add template git@github.com:KUARLab/latex.git
2. ほしいテンプレートを取得<br>
git pull template <branch_name>
3. テンプレ取得先を削除<br>
git remote remove template<br>
<br>

setting.jsonとkeybindings.jsonのテンプレートをmainにおいているので，適宜利用してください．
> **注意**  
 build時にpdfを表示するために，pathを設定する必要があります．latex-workshop.latex.tools内のshow-pdfを変更してください．vscode外でPDFを開きたくない人は，latex-workshop.latex.recipes内のshow-pdfを削除してください．
<br>

### meeting
研究会用の2段組みテンプレート

### thesis
修論卒論用のテンプレート

### RoboMech
ロボメカ用のテンプレート．2025に配布されたテンプレを様式に合わせて変更．
