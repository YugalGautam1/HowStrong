import csv

with open('data\openpowerlifting-2025-02-01-58ad7467.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    data_table = [row for row in csv_reader]  

cleandata = []
for i in range(1,len(data_table)):
    if(data_table[i][2]=='SBD' and (data_table[i][3]=='Raw' or data_table[i][3]=='Wraps')):
        p = data_table[i][25]
        weight = data_table[i][8]
        if(p.strip() and weight.strip()):
            
            weight = float(data_table[i][8])
            if(weight <= 44):
                weight = 44
            elif(weight <= 48):
                weight = 48
            elif(weight <= 52):
                weight = 52
            elif(weight <= 56):
                weight = 56
            elif(weight <= 60):
                weight = 60
            elif(weight <= 67.5):
                weight = 67.5
            elif(weight <= 75):
                weight = 75
            elif(weight <= 82.5):
                weight = 82.5
            elif(weight <= 90):
                weight = 90
            elif(weight <= 100):
                weight = 100
            elif(weight <= 110):
                weight = 110
            elif(weight <= 125):
                weight = 125
            else:
                weight = 140
            cleandata += [[float(p), data_table[i][1],weight,data_table[i][31]]]

cleandata = sorted(cleandata, key=lambda x: x[0])
finaldata = [["M44"],["M48"],["M52"],["M56"],["M60"],["M67.5"],["M75"],["M82.5"],["M90"],["M100"],["M110"],["M125"],["M140"],
             ["M44T"],["M48T"],["M52T"],["M56T"],["M60T"],["M67.5T"],["M75T"],["M82.5T"],["M90T"],["M100T"],["M110T"],["M125T"],["M140T"],
            ["F44"],["F48"],["F52"],["F56"],["F60"],["F67.5"],["F75"],["F82.5"],["F90"],["F100"],["F110"],["F125"],["F140"],
             ["F44T"],["F48T"],["F52T"],["F56T"],["F60T"],["F67.5T"],["F75T"],["F82.5T"],["F90T"],["F100T"],["F110T"],["F125T"],["F140T"]
             ]

for i in range(len(cleandata)):
    if cleandata[i][1] == 'M':
        if cleandata[i][2] == 44:
            finaldata[0] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[13] += [cleandata[i][0]]
        elif cleandata[i][2] == 48:
            finaldata[1] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[14] += [cleandata[i][0]]
        elif cleandata[i][2] == 52:
            finaldata[2] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[15] += [cleandata[i][0]]
        elif cleandata[i][2] == 56:
            finaldata[3] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[16] += [cleandata[i][0]]
        elif cleandata[i][2] == 60:
            finaldata[4] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[17] += [cleandata[i][0]]
        elif cleandata[i][2] == 67.5:
            finaldata[5] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[18] += [cleandata[i][0]]
        elif cleandata[i][2] == 75:
            finaldata[6] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[19] += [cleandata[i][0]]
        elif cleandata[i][2] == 82.5:
            finaldata[7] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[20] += [cleandata[i][0]]
        elif cleandata[i][2] == 90:
            finaldata[8] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[21] += [cleandata[i][0]]
        elif cleandata[i][2] == 100:
            finaldata[9] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[22] += [cleandata[i][0]]
        elif cleandata[i][2] == 110:
            finaldata[10] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[23] += [cleandata[i][0]]
        elif cleandata[i][2] == 125:
            finaldata[11] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[24] += [cleandata[i][0]]
        elif cleandata[i][2] == 140:
            finaldata[12] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[25] += [cleandata[i][0]]

    elif cleandata[i][1] == 'F':
        if cleandata[i][2] == 44:
            finaldata[26] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[39] += [cleandata[i][0]]
        elif cleandata[i][2] == 48:
            finaldata[27] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[40] += [cleandata[i][0]]
        elif cleandata[i][2] == 52:
            finaldata[28] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[41] += [cleandata[i][0]]
        elif cleandata[i][2] == 56:
            finaldata[29] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[42] += [cleandata[i][0]]
        elif cleandata[i][2] == 60:
            finaldata[30] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[43] += [cleandata[i][0]]
        elif cleandata[i][2] == 67.5:
            finaldata[31] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[44] += [cleandata[i][0]]
        elif cleandata[i][2] == 75:
            finaldata[32] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[45] += [cleandata[i][0]]
        elif cleandata[i][2] == 82.5:
            finaldata[33] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[46] += [cleandata[i][0]]
        elif cleandata[i][2] == 90:
            finaldata[34] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[47] += [cleandata[i][0]]
        elif cleandata[i][2] == 100:
            finaldata[35] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[48] += [cleandata[i][0]]
        elif cleandata[i][2] == 110:
            finaldata[36] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[49] += [cleandata[i][0]]
        elif cleandata[i][2] == 125:
            finaldata[37] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[50] += [cleandata[i][0]]
        elif cleandata[i][2] == 140:
            finaldata[38] += [cleandata[i][0]]
            if cleandata[i][3] == 'Yes':
                finaldata[51] += [cleandata[i][0]]

with open("data/cleandata.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(finaldata)  
print("Done")