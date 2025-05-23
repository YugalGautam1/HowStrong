import csv
from flask import Flask, request, jsonify
from flask_cors import CORS 
import math
import matplotlib
matplotlib.use('Agg')
import numpy as np
import base64
import io
from scipy.ndimage import gaussian_filter1d

import matplotlib.pyplot as plt


app = Flask(__name__)
CORS(app)



S = []
with open('data/S.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    S = [row for row in csv_reader]

B = []
with open('data/B.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    B = [row for row in csv_reader]

SB = []
with open('data/SB.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    SB = [row for row in csv_reader]

SBD = []
with open('data/SBD.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    SBD = [row for row in csv_reader]

SD = []
with open('data/SD.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    SD = [row for row in csv_reader]

BD = []
with open('data/BD.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    BD = [row for row in csv_reader]

D = []
with open('data/D.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    D = [row for row in csv_reader]

def picturemaker(arr,you):
        threshold = you
        data = np.array(arr)
        
        counts, bin_edges = np.histogram(data, bins=100)
        
        smoothed_counts = gaussian_filter1d(counts, sigma=2)

        plt.figure(figsize=(60,40))        
        plt.plot(bin_edges[:-1], smoothed_counts, color='#a855f7', linestyle='-', linewidth=2)

        below_threshold = bin_edges[:-1] <= threshold 
        plt.fill_between(bin_edges[:-1], smoothed_counts, where=below_threshold, color='#a855f7', alpha=0.3)
        

        
        plt.grid(False)
        plt.axis('off')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', transparent=True, facecolor=(30/255, 41/255, 59/255, 0.5))  

        buffer.seek(0)
        plt.close()

        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        return  f"data:image/png;base64,{image_base64}"

@app.route('/finders',methods=['POST'])
def percentile():
    data = request.json
    units = bool(data['units'])
    total = 0 
    equipped = bool(data['equipment'])
    tested = bool(data['tested'])
    gender = data['gender']
    bench = (data['bench'])
    squat = (data['squat'])
    deadlift = (data['deadlift'])
    minA = (data['minA'])
    maxA = (data['maxA'])
    minW = (data['minW'])
    maxW = (data['maxW'])

    currData = []
    total = 0
    if(bench=='' and squat=='' and deadlift ==''):
        return jsonify({"percentile" :"No people within these parameters",
                        "image": ''})
    elif(bench=='' and squat!='' and deadlift ==''):
        currData = S
        total = float(squat)
    elif(bench!='' and squat=='' and deadlift ==''):
        currData = B
        total = float(bench)
    elif(bench!='' and squat!='' and deadlift ==''):
        currData = SB
        total = float(squat)+float(bench)
    elif(bench=='' and squat!='' and deadlift !=''):
        currData = SD
        total = float(squat)+float(deadlift)
    elif(bench!='' and squat=='' and deadlift !=''):
        currData = BD
        total = float(bench)+float(deadlift)
    elif(bench=='' and squat=='' and deadlift !=''):
        currData = D
        total =float(deadlift)
    else:
        currData = SBD
        total = float(squat)+float(bench)+float(deadlift)
    parameters = ""

    if(minW!=''):
        minW = float(minW)
        maxW = float(maxW)
        minA = float(minA)
        maxA = float(maxA)
        parameters += "within these parameters"


    if(units):
        total=total/2.2046226218488
        if(minW!=''):
            minW = minW/2.2046226218488
            maxW = maxW/2.2046226218488



    numfull = 0
    you = 0
    values = []
    for i in range(0,len(currData)):
        if(currData[i][6]!=''):
            if((equipped and currData[i][1]=="True") or ((not equipped) and currData[i][1]=="False")):
                if(gender=="All" or (gender=="Male" and currData[i][0]=="M") or (gender=="Female" and currData[i][0]=="F")):
                    if((tested and currData[i][7]=="Yes") or not tested):
                        if(minA == ''):
                            if(total>float(currData[i][6])):
                                you+=1
                            values+=[float(currData[i][6])]
                            numfull+=1

                        elif((currData[i][8]!="" and currData[i][2]!="")):
                            age = float(currData[i][2])
                            weight = float(currData[i][8])
                            if(minA<=age and maxA>=age and minW<=weight and maxW>=weight):
                                if(total>float(currData[i][6])):
                                    you+=1
                                values+=[float(currData[i][6])]
                                numfull+=1
    
                            
    if(numfull==0):
        return jsonify({"percentile" :"No people within these parameters",
                        "image": ''})

    you = float(you)
    numfull = float(numfull)
    potatotired = round((you/numfull) *100,2) 


    return jsonify({"percentile" :"You are stronger than " + str(potatotired) + "% of people " + parameters,
                    "image":picturemaker(values,total)})
    
def ipfFun(total, bodyweight, coeffificents, roundint):
    if(bodyweight<28):
        bodyweight=28
    ipf = total*100/(coeffificents[0]-coeffificents[1]*pow(math.e, -coeffificents[2]*bodyweight))
    ipf = round(ipf,roundint)
    if(ipf<=0):
        ipf=0.0

    return str(ipf)

def dotsFun(ming,maxg,total, bodyweight,coefficients,roundint):
    if(bodyweight<ming):
        bodyweight = ming
    elif(bodyweight>maxg):
        bodyweight = maxg
    D = coefficients[-1]
    for i in range(len(coefficients)-2,-1,-1):
        D+=coefficients[i]*pow(bodyweight,len(coefficients)-1-i)
    D = 500*total/D
    D = round(D,roundint)
    return str(D)

@app.route('/submit',methods=['POST'])
def dotsCalc():
    data = request.json
    units = bool(data['units'])
    total = 0 
    equipped = bool(data['equipment'])
    gender = data['gender']
    bodyweight = float(data['bodyweight'])
    bench = data['bench']
    squat = data['squat']
    deadlift = data['deadlift']
    dots = ""
    ipf = ""
    if(bench =='' and squat == '' and deadlift==''):
        return jsonify({
            "dots": "-----",
            "ipf": "-----"
            })
    if(bench!=''):
        total += float(bench)
    if(squat!=''):
        total+= float(squat)
    if(deadlift!=''):
        total += float(deadlift)
    if(units):
        total=total/2.2046226218488
        bodyweight = bodyweight/2.2046226218488

    roundingin = 2
    if(gender=="All"):
        roundingin = 1
    if(gender == "Male" or gender == "All"):
        dots += dotsFun(15,228,total,bodyweight,[-0.000001093,0.0007391293 ,-0.1918759221,24.0900756,-307.75076],roundingin)
        if(squat=='' and deadlift == ''):
            if(equipped):
                ipf += ipfFun(total, bodyweight, [381.22073,733.79378,0.02398], roundingin)
            else:
                ipf += ipfFun(total, bodyweight, [320.98041,281.40258, 0.01008], roundingin)

        else: 
            if(equipped):
                ipf += ipfFun(total, bodyweight, [1236.25115, 1449.21864,0.01644], roundingin)

            else:
                ipf += ipfFun(total, bodyweight, [1199.72839,1025.18162, 0.00921], roundingin)

    if(gender == "All"):
        dots+='/'
        ipf+='/'

    if(gender=="Female" or gender == "All"):
        dots+= dotsFun(5,153,total,bodyweight,[-0.0000010706,0.0005158568,-0.1126655495,13.6175032,-57.96288],roundingin)
        if(squat=='' and deadlift == ''):
            if(equipped):
                ipf += ipfFun(total, bodyweight, [221.82209, 357.00377, 0.02937], roundingin)
            else:
                ipf += ipfFun(total, bodyweight, [142.40398, 442.52671, 0.04724], roundingin)

        else: 
            if(equipped):
                ipf += ipfFun(total, bodyweight, [758.63878, 949.31382, 0.02435], roundingin)

            else:
                ipf += ipfFun(total, bodyweight, [610.32796, 1045.59282, 0.03048], roundingin)
    
        
    return jsonify({
        "dots": dots,
        "ipf" : ipf

        })
    

    



if __name__ == '__main__':
    app.run(debug=True)