# convert_to_gboard

iPhone / macOS のユーザー辞書（plist 形式）を、Android（Pixel 等）の Gboard にインポートできる形式（`version:2` の ZIP ファイル）へ変換する Python スクリプトです。

Python 3 の標準ライブラリ（`argparse`, `plistlib`, `zipfile`）のみで動作するため、追加パッケージのインストールは不要です。

## 使い方

### 1. Apple 側のユーザー辞書を書き出す

macOS の **「システム設定」＞「キーボード」＞「ユーザ辞書」** を開き、登録されている単語をすべて選択してデスクトップ等へドラッグ＆ドロップすると、plist ファイル（例: `プロパティリスト.txt`）が書き出されます。

### 2. スクリプトを実行する

```bash
python3 convert_to_gboard.py <入力plistファイル> <出力ZIPファイル>
```

実行例:

```bash
python3 convert_to_gboard.py プロパティリスト.txt PersonalDictionary.zip
```

### 3. Pixel（Gboard）にインポートする

1. 生成された `PersonalDictionary.zip` を Pixel に転送します。
2. Gboard の設定から **「単語リスト」＞「日本語」** を開きます。
3. 右上のメニューから **「インポート」** を選び、転送した `PersonalDictionary.zip` を選択します。

## 変換仕様

- 出力 ZIP 内に UTF-8 の `dictionary.txt` を直接格納します（macOS の Finder 圧縮による `__MACOSX` フォルダ混入を防止）。
- `dictionary.txt` は Gboard Dictionary `version:2` 形式（タブ区切り）で出力します。
  - 言語タグ: `ja-JP`
  - 品詞タグ: `品詞なし`
- 重複する `(よみ, 単語)` のペアは自動で除外されます。
- 値に含まれるタブ文字・改行文字は半角スペースに置換されます。

## 注意事項

書き出した辞書ファイルや出力 ZIP には個人情報が含まれる可能性があるため、`.gitignore` により `*.plist` / `*.txt` / `*.zip` は Git の追跡対象から除外しています。
