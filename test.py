import csv
from flask import Flask, request, jsonify
from flask_cors import CORS 
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import math

app = Flask(__name__)
CORS(app)
@app.route("/exerciseList",methods=['GET'])
def potato():
    data_table=[]
    with open('data/exercises.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data_table = [row for row in csv_reader]
    list = []
    for i in range(1,len(data_table)):
        list+=[data_table[i][0]]
    return jsonify(list)

@app.route("/submitWorkout",methods=['POST'])
def hahahah():
    data = request.json
    return data
if __name__ == '__main__':
    app.run(debug=True)