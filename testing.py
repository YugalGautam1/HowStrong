import csv 





def check(arr):
    for i in range(0,len(arr)):
        if(arr[i]>=10):
            return False
    return True

data_table = []
with open('data/exercises.csv', 'r', encoding='utf-8') as file: 
    csv_reader = csv.reader(file)
    data_table = [row for row in csv_reader]

d = {}
for i in range(0,len(data_table)):
    d[data_table[i][0]] = data_table[i][1:]

man = []
for i in range(0,len(data_table[0])):
    man.append([0])

exercises = [
    [
        ["Flat Bench Press", 12, 8], 
        ["Push Ups", 15, 7], 
        ["Dumbbell Bench Press (Flat)", 10, 8]
    ],
    [
        ["Lowbar Back Squat", 8, 9], 
        ["Highbar Back Squat", 10, 8], 
        ["Sumo Deadlift", 6, 9]
    ],
    [
        ["Tricep Pushdown (neutral grip)", 12, 8], 
        ["Skull Crushers (Dumbbell)", 10, 7], 
        ["Overhead Tricep Extension Dumbbell", 12, 8]
    ],
    [
        ["Barbell Curl", 10, 7], 
        ["Hammer Curl", 12, 7], 
        ["Pull Ups", 8, 9]
    ],
    [
        ["Overhead Press", 8, 9], 
        ["Lateral Raise", 15, 6], 
        ["Tricep Dips", 10, 8]
    ]
]

for i in range(0,len(exercises)):
    for j in range(0,len(exercises[i])):
        if(j!=0):
            for k in range(0,len(d[exercises[i][j][0]])):
                a = d[exercises[i][j][0]]
                b = d[exercises[i][j-1][0]]

                if(int(a[k])>=3 and int(b[k])>=3):
                    print("Warning:  It seems you have back to back two exercises that heavily work out the " + str(data_table[0][k]) )
                man[k]+=exercises[i][j][k]
        else:
            for k in range(0,len(d[exercises[i][j][0]])):
                a = d[exercises[i][j][0]]
                man[k]+=exercises[i][j][k]
                
