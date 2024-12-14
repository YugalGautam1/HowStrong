#his page uses data from the OpenPowerlifting project, https://www.openpowerlifting.org.
#You may download a copy of the data at https://gitlab.com/openpowerlifting/opl-data.


import csv
from flask import Flask, request
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

with open('openpowerlifting-2024-12-07-f0ae63ed.csv', 'r',encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    data_table = [row for row in csv_reader]  



@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    lbs = data.get('lbs')
    tested = data.get('tested')
    total=0
    multiplier=1
    if(lbs):
        multiplier=2.20462
    if(data.get('bench','').strip()):
        bench = int(data.get('bench', 0))/multiplier
        total+=bench
    else:
        bench = None

    if(data.get('squat','').strip()):
        squat = int(data.get('squat', 0))/multiplier
        total+=squat
    else:
        squat = None
    
    if(data.get('deadlift','').strip()):
        deadlift = int(data.get('deadlift', 0))/multiplier
        total+=deadlift
    else:
        deadlift = None
    

    if(bench and squat and deadlift):
        if(tested):
            x=0
            y = 0
            for i in range(1,len(data_table)):
                if(data_table[i][25].strip()!='' and data_table[i][31].strip()=="Yes"):
                    if(float(data_table[i][25])<total):
                        x+=1  
                    y+=1
            response = f"Your total lift is {total*multiplier} kg! This makes you stronger than {x/y*100}% of Tested Lifters "

            return response
        else:
            x=0
            y = 0
            for i in range(1,len(data_table)):
                if(data_table[i][25].strip()!=''):
                    if(float(data_table[i][25])<total):
                        x+=1  
                    y+=1
            response = f"Your total lift is {total*2.20462} kg! This makes you stronger than {x/y*100}% of All Lifters"

            return response
    return("missing vals")
    
if __name__ == '__main__':
    app.run(debug=True)