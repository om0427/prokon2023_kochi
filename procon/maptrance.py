import csv

with open("\\仕事\\高専プロコン2023\\field\\フィールドデータ\\c17.csv") as file:
    ax = list(csv.reader(file))
    print(ax)  # 変換確認用

pm = len(ax)
structures = [[0] * pm for _ in range(pm)]
masons = [[0] * pm for _ in range(pm)]
no1 = 0
no2 = 0
for i in range(pm):
    for j in range(pm-1):
        if ax[i][j] == '1':
            structures[i][j] = 1
        elif ax[i][j] == '2':
            structures[i][j] = 2
        elif ax[i][j] == 'a':
            no1 += 1
            masons[i][j] = no1
        elif ax[i][j] == 'b':
            no2 += 1
            masons[i][j] = -no2

for row in structures:
    print(row)
print("--------------------------------")
for row in masons:
    print(row)


    
    

        