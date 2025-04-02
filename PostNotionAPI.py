import requests
import json

# Notion API トークンとデータベースID（ハイフンなしの形式）を指定
NOTION_TOKEN = "トークンを取得"
DATABASE_ID = "データベースID"  # ハイフン除去済みの32文字の文字列

if not NOTION_TOKEN or not DATABASE_ID:
    raise ValueError("NOTION_TOKEN と DATABASE_ID を設定してください。")

# 長いテキスト（改行あり）の例
long_text = """これは長いテキストです。
改行が含まれています。
例えば、このように、
複数行に分かれています。"""

def create_paragraph_blocks(text):
    """
    入力テキストを改行で分割し、各行を段落ブロックに変換する関数
    """
    # 改行で分割（空行もそのまま扱います）
    lines = text.splitlines()
    blocks = []
    for line in lines:
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": line}
                    }
                ]
            }
        })
    return blocks

# 長いテキストを段落ブロックに変換
children_blocks = create_paragraph_blocks(long_text)

# Notion に追加するページの内容
data = {
    "parent": {"database_id": DATABASE_ID},
    "properties": {
        "Name": {
            "title": [
                {"text": {"content": "メモのタイトル"}}
            ]
        }
    },
    "children": children_blocks
}

# Notion API のページ作成エンドポイント
url = "https://api.notion.com/v1/pages"

# リクエストヘッダー（最新の Notion-Version を指定）
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# API へ POST リクエストを送信
response = requests.post(url, headers=headers, json=data)

# レスポンスの確認
if response.status_code == 200:
    print("ページが正常に作成されました:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
else:
    print("エラーが発生しました:")
    print(response.status_code, response.text)
