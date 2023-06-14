#FIND ALL INFORMATION ABOUT THIS REST API HERE: https://mycle-iiot.postman.co/workspace/57d25410-5868-44d8-b432-6a596c9b6b73/documentation/24866334-307d89c6-7fe0-4a54-9190-dc6372836be1?entity=&branch=&version=


from datetime import datetime
from flask import Flask, jsonify, request, make_response
import sqlite3
from flask_cors import CORS
from database.handler.databaseHandler import DatabaseHandler
from simulator import Simulator
from triangle import Triangle
from circle import Circle

app = Flask(__name__)
CORS(app) #For local testing

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
        return jsonify({
  "simulations": [
    {
      "id": "0",
      "description": "Simulation LCM Rechteck",
      "last_edited": "1984-06-09:12:18:33"
    },
    {
      "id": "1",
      "description": "Simulation LCM Dreieck",
      "last_edited": "1984-06-09:12:18:33"
    },
    {
      "id": "0",
      "description": "Simulation LCM Kreis",
      "last_edited": "1984-06-09:12:18:33"
    }
  ]
})  #list of all sims
    elif request.method == 'POST':
        simulator.startSimulator()
        return jsonify({
                            "simulation_id": 1
                        })
    elif request.method == 'DELETE':
        return #delete all stored sims


@app.route('/api/simulations/protocol', methods=['PUT'])
def simulationsProtocol():
  if request.method == 'PUT':
    simulator.setProtocol(request.form['protocol']);
    return "Protocol set successfully"

@app.route('/api/simulations/<int:simulations_id>', methods=['GET', 'DELETE'])
def simulationsId(simulations_id):
    if request.method == 'GET':
        return jsonify({
  "id": "0",
  "description": "Simulation LCM Rechteck",
  "last_edited": "1984-06-09:12:18:33",
  "machine": {
    "parameters": [
      {
        "id": "1",
        "description": "run_time",
        "value": "0"
      },
      {
        "id": "2",
        "description": "coolant_level",
        "value": "1000"
      },
      {
        "id": "3",
        "description": "power_consumption",
        "value": "0"
      },
      {
        "id": "4",
        "description": "power_laser_module",
        "value": "0"
      },
      {
        "id": "5",
        "description": "idle_time",
        "value": "0"
      },
      {
        "id": "6",
        "description": "error_state",
        "value": "false"
      },
      {
        "id": "7",
        "description": "privilage_state",
        "value": "false"
      }
    ]
  },
  "program": {
    "description": "Zahnrad",
    "parameters": [
      {
        "id": "1",
        "description": "current_amount",
        "value": "50"
      },
      {
        "id": "2",
        "description": "target_amount",
        "value": "100"
      },
      {
        "id": "3",
        "description": "uptime_in_s",
        "value": "50"
      },
      {
        "id": "4",
        "description": "power_consumption_in_Wh",
        "value": "5000"
      },
      {
        "id": "5",
        "description": "coolant_consumption_in_percent",
        "value": "10"
      },
      {
        "id": "6",
        "description": "time_per_item_in_s",
        "value": "1"
      }
    ]
  }
})
    elif request.method == 'DELETE':
        return #delete a selected sim
    
    
#Machines
#####!!!!!here!!!!!
@app.route('/api/simulations/<int:simulations_id>/machine', methods=['GET', 'PATCH'])
def machines(simulations_id):
    if request.method == 'GET':
        simulator.updateSimulation(datetime.now())
        return simulator.getMachineStateJson()
    elif request.method == 'PATCH':
        data = request.get_json()
        simulator.updateMachineStateParameters(data)
        print(data)

        return jsonify({'message': 'Success'})#change parameter(s) in the machine state

@app.route('/api/simulations/<int:simulations_id>/machine/auth')
def auth(simulations_id):
    response = make_response("<h1>Success</h1>")
    response.status_code = 200
    return response #pw in http body sets auth in machine

@app.route('/api/simulations/<int:simulations_id>/machine/errors', methods=['GET', 'POST'])
def error(simulations_id):
    if request.method == 'GET':
        data = simulator.warnings.getNotificationsJSON()
        return data #list of all errors and warnings
    elif request.method == 'POST':
        error_id = request.form.get('error_id')
        warning_id = request.form.get('warning_id')

        if error_id is None and warning_id is None:
            return jsonify({'error': 'No error_id or warning_id provided.'})
        if error_id:
            simulator.warnings.setSelectedError(error_id)
            simulator.stopProgram()
        elif warning_id:
            simulator.warnings.setSelectedWarning(warning_id)

        return jsonify({'message': 'Success'})


#Programs

@app.route('/api/simulations/<int:simulations_id>/machine/programs')
def allPrograms(simulations_id):
    listOfPrograms = simulator.getPrograms()
    data = {"programs": []}
    for program in listOfPrograms:
        data["programs"].append(program.toJSON())
    print(data)
    
    return jsonify(data)#list of all programs

@app.route('/api/simulations/<int:simulations_id>/machine/programs/current', methods=['GET', 'POST', 'PATCH'])
def currentProgram(simulations_id):
    if request.method == 'GET':
         return simulator.getProgramState()#current program state
    elif request.method == 'POST':
        programId = request.form.get('program_id')
        print(programId)
        simulator.setMode(programId)
        return "Success"#set this program to be the current one
    elif request.method == 'PATCH':
        json = request.get_json()
        for parameter in json["parameters"]:
            if(parameter['value'] == "start"):
                simulator.startProgram()
            elif(parameter['value'] == "stop"):
                simulator.stopProgram()
            elif(parameter['value'] == "restart"):
                simulator.resetSimulator()
        return jsonify({
        "parameters": [
        {
            "id": "2",
            "description": "target_amount",
            "value": "100"
        }
    ]
    }) #change parameter(s) in the current program state


#debuggin purposes
if __name__ == '__main__':
  print(jsonify(simulator.warnings.getNotificationsJSON()))