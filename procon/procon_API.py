import time,requests,json,os,csv,time

def main():
    t1=time.time()
    
    num=0

    #token="kochi89665ca9ed3105039b52d806dab0a35e70b96906f7a7db2025da133a323"
    token="token1"
    header={"procon-token": token}

    server_id_url="http://localhost:3000/matches"

    response = requests.get(server_id_url, headers=header)
    while response.status_code != 200:  # ステータスコード200は成功を示します
        response = requests.get(server_id_url, headers=header)
        time.sleep(0.3)

    data=response.json()


    if num<len(data):
        id=data["matches"][num]["id"]

    server_url = "http://localhost:3000/matches/"+str(id)

    response = requests.get(server_url, headers=header)
    while response.status_code != 200:  # ステータスコード200は成功を示します
        response = requests.get(server_url, headers=header)
        time.sleep(0.3)
        print("wait")
    
    json_data = response.json()
    DataSave(json_data)

    t2=time.time()
    print(t2-t1)

    ctime=time.time()
    reload_time=0.2
    turn=json_data["turn"]
    print(turn)
    
    while 1:
        if time.time()-ctime > reload_time:
            response = requests.get(server_url, headers=header)
            if response.status_code == 200:  # ステータスコード200は成功を示します
                json_data = response.json()
 
            if turn!=json_data["turn"]:
                turn=json_data["turn"]
                DataSave(json_data)
                print(turn)

            ctime=time.time()


def DataSave(json_data):
    turn=json_data["turn"]
    board=json_data["board"]
    width=board["width"]
    height=board["height"]
    mason=board["mason"]
    masons=board["masons"]
    structures=board["structures"]
    walls=board["walls"]
    territories=board["territories"]

    cwd=os.getcwd()
    os.chdir(cwd+"/status")
    
    with open("masons.csv", "w", newline='') as file:
        writer=csv.writer(file)
        for i in range(height):
            writer.writerow(masons[i])
    
    with open("structures.csv", "w", newline='') as file:
        writer=csv.writer(file)
        for i in range(height):
            writer.writerow(structures[i])

    with open("territories.csv", "w", newline='') as file:
        writer=csv.writer(file)
        for i in range(height):
            writer.writerow(territories[i])

    with open("walls.csv", "w", newline='') as file:
        writer=csv.writer(file)
        for i in range(height):
            writer.writerow(walls[i])

    with open("mason.dat", "w", newline='') as file:
        file.write(str(mason))
    
    with open("size.dat", "w", newline='') as file:
        file.write(str(height)+", "+str(width))
    
    with open("turn.dat", "w", newline='') as file:
        file.write(str(turn))
    
    os.chdir("../")



if __name__=='__main__':
    main()