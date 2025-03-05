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
    list = [
        "Bench", 
        "Squat", 
        "Deadlift", 
        "Tricep Pushdown (neutral grip)", 
        "Tricep Pushdown (pronated grip)", 
        "Tricep Pushdown (supinated grip)", 
        "Flat Bench Press", 
        "Highbar Back Squat", 
        "Conventional Deadlift", 
        "Tricep Dips", 
        "Skull Crushers (Cable)", 
        "Skull Crushers (Dumbbell)", 
        "Skull Crushers (Barbell)", 
        "Push Ups", 
        "Dumbbell Bench Press (Flat)", 
        "Sumo Deadlift", 
        "Lowbar Back Squat", 
        "Overhead Tricep Extension Dumbbell", 
        "Overhead Tricep Extension Cable"
    ]    
    return jsonify(list)

@app.route("/submitWorkout",methods=['POST'])
def hahahah():
    data = request.json
    return data
if __name__ == '__main__':
    app.run(debug=True)