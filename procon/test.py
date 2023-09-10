import requests,json

# サーバーのURLを指定 (サーバーのアドレスとポート番号に合わせて変更)
server_url = "https://localhost?token=kochi89665ca9ed3105039b52d806dab0a35e70b96906f7a7db2025da133a323:3000/matches"  # 例: http://localhost:8080

# サーバーにGETリクエストを送信してJSONデータを取得
response = requests.get(server_url)  # エンドポイントも適切に指定

# レスポンスのステータスコードを確認
if response.status_code == 200:  # ステータスコード200は成功を示します
    # JSONデータをPythonのディクショナリにパース
    #json_data = response.json()

    # パースしたデータを利用
    print("受け取ったJSONデータ:", response.text)
else:
    print("リクエストが失敗しました。ステータスコード:", response.status_code)