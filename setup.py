import csv
data_table = []
with open('data\openpowerlifting-2025-05-17-c19f7b97.csv', 'r', encoding = 'utf-8') as file:
    csv_reader = csv.reader(file)
    data_table = [row for row in csv_reader]

people = [[],[],[],[],[],[],[]]
other = ["B","SB","SBD","SD","BD","S","D"]
event = {"B":0,"SB":1,"SBD":2,"SD":3,"BD":4,"S":5,"D":6}
data_table = data_table[1:]
for i in range(0,len(data_table)):
    #event SBD is column 2 
    #gender is column 1 
    #equipment is 3 
    #age is 4
    #age class is 5 
    #squat is 14
    #bench is 19
    #deadlift is 24
    #total is 25
    #tested is 31 
    E = True
    if(data_table[i][3]=='Raw' or data_table[i][3]=='Wraps'):
        E = False
    squat = "0"
    if(data_table[i][14]!='' and data_table[i][14][0]!='-'):
        squat = data_table[i][14]
    bench = "0"
    if(data_table[i][19]!=''and data_table[i][19][0]!='-'):
        bench = data_table[i][19] 
    deadlift = "0"
    if(data_table[i][24]!='' and data_table[i][24][0]!='-'):
        deadlift = data_table[i][24] 
    total = "0"
    if(data_table[i][25]!='' and data_table[i][25][0]!='-'):
        total = data_table[i][25] 

    people[event[data_table[i][2]]]+=[[data_table[i][1],E,data_table[i][4],squat,bench,deadlift,data_table[i][25],data_table[i][31],data_table[i][8]]]



for i in range(0,len(people)):
    with open("data/"+other[i]+".csv", mode="w", newline="",encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(people[i])  

