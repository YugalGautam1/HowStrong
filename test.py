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
    list = ["Bench","Squat","Deadlift"]
    return jsonify(list)

@app.route("/submitWorkout",methods=['POST'])
def hahahah():
    data = request.json
    return data
if __name__ == '__main__':
    app.run(debug=True)