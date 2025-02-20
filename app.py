
import csv
from flask import Flask, request, jsonify
from flask_cors import CORS 
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
CORS(app)

with open('data/cleandata.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    data_table = [row for row in csv_reader]

@app.route('/submitScore',methods=['POST'])
def submitScore():
    data = request.json
    lbs = data.get('lbs')
    gender = data.get('gender') 

    multiplier = 1
    if(lbs=='1'):
        multiplier = 2.20462 
    total=0
    dots = [[-0.000001093,0.0007391293 ,-0.1918759221,24.0900756,-307.75076],[-0.0000010706,0.0005158568,-0.1126655495,13.6175032,-57.96288]]
    value = 0 
    if(gender=='Female'):
        value=1
    
    if(data.get('weight','').strip() and data.get('bench','').strip() and data.get('squat','').strip() and data.get('deadlift','').strip()):
        bench = float(data.get('bench', 0))/multiplier
        total+=bench
        squat = float(data.get('squat', 0))/multiplier
        total+=squat
        deadlift = float(data.get('deadlift', 0))/multiplier
        total+=deadlift
        bodyweight = float(data.get('weight',0))/multiplier
        if(value == 1 and bodyweight<15):
            return "Male Bodyweight must be at least 15kg or 33.07 lbs"
        elif(value ==1 and bodyweight>228):
            return "Maximum Male bodyweight is 228kg or 502.65 lbs"
        elif(value==0 and bodyweight<5):
            return "Male Bodyweight must be at least 5kg or 11.03 lbs"
        elif(value==0 and bodyweight>153):
            return "Maximum Male bodyweight is 153kg or 337.31 lbs"

        

        D = dots[value][-1]
        for i in range(len(dots[value])-2,-1,-1):
            D+=dots[value][i]*pow(bodyweight,len(dots[value])-1-i)
        dots = 500*total/D
        return f"Your dots score is {round(dots,3)}"

    else:
        return "missing vals"





    

@app.route('/submit', methods=['POST'])
def submit():

    data = request.json
    lbs = data.get('lbs')
    tested = data.get('tested')
    gender = data.get('gender')
    weightclass = data.get('weight')
    total=0
    multiplier=1
    unit = "kgs"
        
    if(lbs=='1'):
        multiplier=2.20462
        unit = "lbs"
    if(data.get('bench','').strip() and data.get('squat','').strip() and data.get('deadlift','').strip()):
        bench = float(data.get('bench', 0))/multiplier
        total+=bench
        squat = float(data.get('squat', 0))/multiplier
        total+=squat
        deadlift = float(data.get('deadlift', 0))/multiplier
        total+=deadlift

    else:
        return ("missing values")
    

    if(total!=0):
        test = ""
        if(gender == 'Male'):
            value = 0 
            if(tested):
                value=13
                test = " tested"
        else:
            value = 26
            if(tested):
                value = 39
                test = " tested"
        value+=int(weightclass)
        
        percentile = 0 
        position = total
        high = len(data_table[value])-1
        low = 1
        if(total<float(data_table[value][low])):
            percentile = 0 
        elif(total>float(data_table[value][high])):
            percentile = 100
        else:
            while(low<=high):
                mid = (low+high)//2
                if(float(data_table[value][mid])>total):
                   high = mid-1
                elif(float(data_table[value][mid])<total and float(data_table[value][mid+1])<total):
                    low=mid+1
                elif(float(data_table[value][mid])<total and float(data_table[value][mid+1])>=total):
                    percentile = ((mid+1)/(len(data_table[value])+1))*100    
                    break
                elif(float(data_table[value][mid])==total and float(data_table[value][mid+1])==total):
                    high = mid-1

        temporary = data_table[value][0][1:]
        if(temporary[-1]=='T'):
            temporary=temporary[:-1]
        temporary = float(temporary)*multiplier
        
        response = f"Your total lift is {round(total*multiplier,3)} {unit} This makes you stronger than {round(percentile,3)}% of {test} {gender} Lifters at {round(temporary,1)} {unit}"    
        return response

    
    return("missing vals")
    


@app.route('/histogram', methods=['POST'])
def line_histogram():
    data = request.json
    lbs = data.get('lbs')
    tested = data.get('tested')
    gender = data.get('gender')
    weightclass = data.get('weight')
    total=0
    multiplier=1
    width = data.get('width')
    height = data.get('height')

    if(lbs=='1'):
        multiplier=2.20462
    if(data.get('bench','').strip() and data.get('squat','').strip() and data.get('deadlift','').strip()):
        bench = float(data.get('bench', 0))/multiplier
        total+=bench
        squat = float(data.get('squat', 0))/multiplier
        total+=squat
        deadlift = float(data.get('deadlift', 0))/multiplier
        total+=deadlift

        if(gender == 'Male'):
            value = 0
            if(tested):
                value=13
        else:
            value = 26
            if(tested):
                value = 39
        value+=int(weightclass)
    try:
        width = float(width)
        height = float(height)
        threshold = total
        data = data_table[value][1:]

        for i in range(0,len(data)):
            data[i] = float(data[i])
        data = np.array(data)
        
        counts, bin_edges = np.histogram(data, bins="auto")

        plt.figure(figsize=(width//10,height//10))        
        plt.plot(bin_edges[:-1], counts, color='blue', linestyle='-')

        below_threshold = bin_edges[:-1] <= threshold 
        plt.fill_between(bin_edges[:-1], counts, where=below_threshold, color='blue', alpha=0.3)
        
        above_threshold = list(below_threshold)
        find = True 
        for i in range(0,len(above_threshold)):

            if(find):
                if(not above_threshold[i]):
                    if(i-1>=0):
                        above_threshold[i-1]=True
                        find=True
                above_threshold[i]=False
            else:
                above_threshold[i] = True

        above_threshold = np.array(above_threshold)
        plt.fill_between(bin_edges[:-1], counts, where=above_threshold, color='red', alpha=0.3)
        plt.title(f'All data below your Total is Blue', fontsize=width//10, fontweight='bold')
        plt.grid(False)
        plt.axis('off')

        for spine in plt.gca().spines.values():
            spine.set_visible(False)

        buffer = io.BytesIO()
        
        plt.savefig(buffer, format='png', bbox_inches='tight', facecolor=("#7E8F92"))  

        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        plt.close()

        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        return jsonify({"image": f"data:image/png;base64,{image_base64}"})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    return jsonify({"Missing values"})


if __name__ == '__main__':
    app.run(debug=True)