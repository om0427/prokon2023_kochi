import requests,time

server_id_url="http://localhost:3000/matches"

token="token2"
header={"procon-token": token}


response = requests.get(server_id_url, headers=header)
while response.status_code != 200:  # ステータスコード200は成功を示します
    response = requests.get(server_id_url, headers=header)
    time.sleep(0.3)

data=response.json()

print(data["matches"][0]["id"])