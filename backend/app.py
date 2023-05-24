#FIND ALL INFORMATION ABOUT THIS REST API HERE: https://mycle-iiot.postman.co/workspace/57d25410-5868-44d8-b432-6a596c9b6b73/documentation/24866334-307d89c6-7fe0-4a54-9190-dc6372836be1?entity=&branch=&version=


from datetime import datetime
from flask import Flask, jsonify, request
import sqlite3
from simulator import Simulator

app = Flask(__name__)

simulator = Simulator()

#/time to test the API

@app.route('/api/time')
def get_current_time():
    return {'time': datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}

#Database Example

@app.route('/api/db')
def getLine():
    conn = sqlite3.connect("database/machine-sim.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO error (error_type) VALUES ('error1'), ('error');")
    return {'error': cursor.execute("SELECT error_type FROM error").fetchall()}

# Simulations

@app.route('/api/simulations', methods=['GET', 'POST', 'DELETE'])
def simulations():
    if request.method == 'GET':
        return jsonify("nichts")  #list of all sims
    elif request.method == 'POST':
        #formtest = request.form["team1"]
        jsontest = request.get_json()
        return jsonify(f'{jsontest["description"]} ist krass!')
    elif request.method == 'DELETE':
        return #delete all stored sims


@app.route('/api/simulations/<int:simulations_id>', methods=['GET', 'DELETE'])
def simulationsId(simulation_id):
    if request.method == 'GET':
        return #data of a selected sim
    elif request.method == 'DELETE':
        return #delete a selected sim
    
    
#Machines
#####!!!!!here!!!!!
@app.route('/api/simulations/<int:simulations_id>/machine', methods=['GET', 'PATCH'])
def machines(simulations_id):
    if request.method == 'GET':
        simulator.updateSimulation(datetime.now())
        return simulator.getMachinState()
    elif request.method == 'PATCH':
        return #change parameter(s) in the machine state

@app.route('/api/simulations/<int:simulations_id>/machine/auth')
def auth(simulation_id):
    return #pw in http body sets auth in machine

@app.route('/api/simulations/<int:simulations_id>/machine/errors', methods=['GET', 'POST'])
def error(simulation_id):
    if request.method == 'GET':
        return #list of all errors and warnings
    elif request.method == 'POST':
        error_id = request.args.get('error_id')
        return #creates the given error (via id) on the machine


#Programs

@app.route('/api/simulations/<int:simulations_id>/machine/programs')
def program(simulations_id):
    return #list of all programs

@app.route('/api/simulations/<int:simulations_id>/machine/programs/current', methods=['GET', 'POST', 'PATCH'])
def currentProgram(simulations_id):
    if request.method == 'GET':
        return #current program state
    elif request.method == 'POST':
        program_id = request.args.get('program_id')
        return #set this program to be the current one
    elif request.method == 'PATCH':
        return #change parameter(s) in the current program state