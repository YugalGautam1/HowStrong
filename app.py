

import csv
from flask import Flask, request
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)


with open('openpowerlifting-2024-12-21-6322a115.csv', 'r',encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    data_table = [row for row in csv_reader]  

male = []
male_tested = []
female = []
female_tested = []

for i in range(0,len(data_table)):
    if(data_table[i][1]=='M'):
        p = data_table[i][25]
        if(p.strip()):
            male+=[(float(data_table[i][25]))]
            if( data_table[i][31].strip()=="Yes"):
                male_tested+=[(float(data_table[i][25]))]
           
    elif(data_table[i][1]=='F'):
        p = data_table[i][25]
        if(p.strip()):
            female+=[(float(data_table[i][25]))]
            if( data_table[i][31].strip()=="Yes"):
                female_tested+=[(float(data_table[i][25]))]
           
male = sorted(male)
female = sorted(female)
male_tested = sorted(male_tested)
female_tested=sorted(female_tested)


@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    lbs = data.get('lbs')
    tested = data.get('tested')
    gender = data.get('gender')
    total=0
    multiplier=1
    unit = "kgs"
    
    
    if(lbs):
        multiplier=2.20462
        unit = "lbs"
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
        if(gender=='Male'):
            if(tested):
                percentile = 0 
                if(total>male_tested[-1]):
                    percentile = 100
                elif(total<male_tested[0]):
                    percentile = 0 
                else: 
                    low = 0
                    high = len(male_tested)-2
                    while(True):
                        mid = (low+high)//2
                        if(male_tested[mid]>total):
                            high=mid-1
                        elif(male_tested[mid]<total and male_tested[mid+1]<total):
                            low=mid+1
                        elif(male_tested[mid]<total and male_tested[mid+1]>=total):
                            percentile= ((mid+1)/len(male_tested))*100
                            break
                        elif(male_tested[mid]==total and male_tested[mid+1]==total):
                            high=mid-1


                response = f"Your total lift is {round(total*multiplier,3)} {unit}! This makes you stronger than {round(percentile,3)}% of Male Tested Lifters "

                return response
            else:
                percentile = 0 
                if(total>male[-1]):
                    percentile = 100
                elif(total<male[0]):
                    percentile = 0 
                else: 
                    low = 1
                    high = len(male)-2
                    while(True):
                        mid = (low+high)//2
                        if(male[mid]>total):
                            high=mid-1
                        elif(male[mid]<total and male[mid+1]<total):
                            low=mid+1
                        elif(male[mid]<total and male[mid+1]>=total):
                            percentile= ((mid+1)/len(male))*100
                            break
                        elif(male[mid]==total and male[mid+1]==total):
                            high=mid-1

                response = f"Your total lift is {round(total*multiplier,3)} {unit}! This makes you stronger than {round(percentile,3)}% of all Male Lifters"
        else:
            if(tested):
                percentile = 0 
                if(total>female_tested[-1]):
                    percentile = 100
                elif(total<female_tested[0]):
                    percentile = 0 
                else: 
                    low = 0
                    high = len(female_tested)-2
                    while(True):
                        mid = (low+high)//2
                        if(female_tested[mid]>total):
                            high=mid-1
                        elif(female_tested[mid]<total and female_tested[mid+1]<total):
                            low=mid+1
                        elif(female_tested[mid]<total and female_tested[mid+1]>=total):
                            percentile= ((mid+1)/len(female_tested))*100
                            break
                        elif(female_tested[mid]==total and female_tested[mid+1]==total):
                            high=mid-1


                response = f"Your total lift is {round(total*multiplier,3)} {unit}! This makes you stronger than {round(percentile,3)}% of Female Tested Lifters "

                return response
            else:
                percentile = 0 
                if(total>female[-1]):
                    percentile = 100
                elif(total<female[0]):
                    percentile = 0 
                else: 
                    low = 1
                    high = len(female)-2
                    while(True):
                        mid = (low+high)//2
                        if(female[mid]>total):
                            high=mid-1
                        elif(female[mid]<total and female[mid+1]<total):
                            low=mid+1
                        elif(female[mid]<total and female[mid+1]>=total):
                            percentile= ((mid+1)/len(female))*100
                            break
                        elif(female[mid]==total and female[mid+1]==total):
                            high=mid-1

                response = f"Your total lift is {round(total*multiplier,3)} {unit}! This makes you stronger than {round(percentile,3)}% of all Female Lifters"
        

            return response
    return("missing vals")
    
if __name__ == '__main__':
    app.run(debug=True)