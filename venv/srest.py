import json
import traci
from flask import Flask, request, jsonify
import os
import sys
from functions import getNumberOfCarsInEdges

maxTime = 60
my_edge = 'Via3ToInter'

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")


with open("config_sumo.json","r") as file:
    config = json.load(file)

Sumo_config = [
    config["sumo_binary"],
    '-c', config["config_file"],
    '--step-length', config["step_length"],
    '--delay', config["delay"],
    '--lateral-resolution', config["delay"]
]

app = Flask(__name__)

@app.route('/getNumberCars')
def getNumbersCars():
    current_time = 0
    traci.start(Sumo_config)

    while current_time < maxTime:
        traci.simulationStep() # Move simulation forward 1 step
        # Here you can decide what to do with simulation data at each step
        getNumberOfCarsInEdges(my_edge)
        # step_count = step_count + 1
        current_time += 1
    traci.close()
    return jsonify({"message": "Simulacao iniciada"}),200
app.run()