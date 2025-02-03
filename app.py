
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
data = []

with open('data/cleandata.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    data_table = [row for row in csv_reader]


@app.route('/submit', methods=['POST'])
def submit():
    global position
    global value
    data = request.json
    lbs = data.get('lbs')
    tested = data.get('tested')
    gender = data.get('gender')
    weightclass = data.get('weight')
    total=0
    multiplier=1
    unit = "kgs"
    
    if(lbs):
        multiplier=2.20462
        unit = "lbs"
    if(data.get('bench','').strip()):
        bench = float(data.get('bench', 0))/multiplier
        total+=bench
    else:
        bench = None

    if(data.get('squat','').strip()):
        squat = float(data.get('squat', 0))/multiplier
        total+=squat
    else:
        squat = None
    
    if(data.get('deadlift','').strip()):
        deadlift = float(data.get('deadlift', 0))/multiplier
        total+=deadlift
    else:
        deadlift = None
    
    
    if(bench and squat and deadlift):
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
        total = bench+squat+deadlift
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

    
    position = None
    return("missing vals")
    


@app.route('/histogram', methods=['GET'])
def line_histogram():
    
    global value
    global position

    if not position:
        return ""

    try:
        threshold = position
        data = data_table[value][1:]

        for i in range(0,len(data)):
            data[i] = float(data[i])
        data = np.array(data)
        
        counts, bin_edges = np.histogram(data, bins="auto")

        plt.figure(figsize=(10, 6))
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

        plt.title(f'All data below your Total is Blue', fontsize=16, fontweight='bold')
        plt.grid(False)
        plt.axis('off')

        for spine in plt.gca().spines.values():
            spine.set_visible(False)

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', facecolor=(180/255,180/255,180/255))  

        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        plt.close()

        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        return jsonify({"image": f"data:image/png;base64,{image_base64}"})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)