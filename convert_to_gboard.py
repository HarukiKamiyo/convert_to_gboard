import argparse
import plistlib
import zipfile


def convert_plist_to_gboard_zip(input_path, output_zip_path):
    # 1. Appleのplistファイルをバイナリモードで読み込む
    with open(input_path, 'rb') as f:
        plist_data = plistlib.load(f)

    # 2. 重複を除外しながらデータを抽出・整形する
    seen = set()
    entries = []
    for item in plist_data:
        if isinstance(item, dict):
            # 前後の空白を削り、TSVが崩れないようタブと改行をスペースに置換
            phrase = (
                item.get('phrase', '')
                .strip()
                .replace('\r\n', ' ')
                .replace('\r', ' ')
                .replace('\n', ' ')
                .replace('\t', ' ')
            )
            shortcut = (
                item.get('shortcut', '')
                .strip()
                .replace('\r\n', ' ')
                .replace('\r', ' ')
                .replace('\n', ' ')
                .replace('\t', ' ')
            )

            if phrase and shortcut:
                key = (shortcut, phrase)
                if key not in seen:
                    seen.add(key)
                    entries.append({
                        'shortcut': shortcut,
                        'phrase': phrase,
                        'lang': 'ja-JP',
                        'pos': '品詞なし',
                    })

    # 3. Gboard version:2 形式のテキストを組み立てる
    lines = [
        "# Gboard Dictionary version:2",
        "# Gboard Dictionary format:shortcut\tword\tlanguage_tag\tpos_tag",
    ]
    for entry in entries:
        lines.append(
            f"{entry['shortcut']}\t{entry['phrase']}\t{entry['lang']}\t{entry['pos']}"
        )
    content = "\n".join(lines) + "\n"

    # 4. テキストを直接ZIPファイル内の dictionary.txt として保存する
    with zipfile.ZipFile(output_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('dictionary.txt', content.encode('utf-8'))

    print(f"変換完了: {len(entries)} 件の単語を {output_zip_path} に出力しました。")


def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert iOS/macOS user dictionary plist to Gboard dictionary ZIP.'
    )
    parser.add_argument(
        'input_path',
        help='入力するplistファイルのパス (例: プロパティリスト.txt)'
    )
    parser.add_argument(
        'output_zip_path',
        help='出力するZIPファイルのパス (例: PersonalDictionary.zip)'
    )
    return parser.parse_args()


def main():
    args = parse_args()
    convert_plist_to_gboard_zip(args.input_path, args.output_zip_path)


if __name__ == '__main__':
    main()
