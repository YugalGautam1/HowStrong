from flask import Flask, request, jsonify
from flask_cors import CORS 
import math

app = Flask(__name__)
CORS(app)




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