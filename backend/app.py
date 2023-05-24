#FIND ALL INFORMATION ABOUT THIS REST API HERE: https://mycle-iiot.postman.co/workspace/57d25410-5868-44d8-b432-6a596c9b6b73/documentation/24866334-307d89c6-7fe0-4a54-9190-dc6372836be1?entity=&branch=&version=


from datetime import datetime
from flask import Flask, jsonify, request, make_response
import sqlite3
from flask_cors import CORS
from simulator import Simulator

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
        return jsonify({
                            "simulation_id": 1
                        })
    elif request.method == 'DELETE':
        return #delete all stored sims


@app.route('/api/simulations/<int:simulations_id>', methods=['GET', 'DELETE'])
def simulationsId(simulation_id):
    if request.method == 'GET':
        return jsonify({
  "id": "0",
  "description": "Simulation LCM Rechteck",
  "last_edited": "1984-06-09:12:18:33",
  "machine": {
    "parameters": [
      {
        "id": "1",
        "description": "runtime",
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
        return simulator.getMachinState()
    elif request.method == 'PATCH':
        return #change parameter(s) in the machine state

@app.route('/api/simulations/<int:simulations_id>/machine/auth')
def auth(simulation_id):
    response = make_response("<h1>Success</h1>")
    response.status_code = 200
    return response#pw in http body sets auth in machine

@app.route('/api/simulations/<int:simulations_id>/machine/errors', methods=['GET', 'POST'])
def error(simulation_id):
    if request.method == 'GET':
        return jsonify({
    "errors": [
        {
            "id":"0",
            "name":"Sicherheitstüre offen"
        },
        {
            "id":"1",
            "name":"Leistung Lasermodul unzureichend"
        },
        {
            "id":"2",
            "name":"Programmfehler"
        }
    ],
    "warnings": [
        {
            "id":"0",
            "name":"Kühlwasser zu sauer"
        },
        {
            "id":"1",
            "name":"Hohe Laufzeit"
        },
        {
            "id":"2",
            "name":"Kühlwasserstand niedrig"
        }
    ]
    }) #list of all errors and warnings
    elif request.method == 'POST':
        error_id = request.args.get('error_id')
        return #creates the given error (via id) on the machine


#Programs

@app.route('/api/simulations/<int:simulations_id>/machine/programs')
def program(simulations_id):
    return jsonify({
    "programs": [
        {
            "description": "",
            "id": "0"
        },
        {
            "description": "Kreis",
            "id": "1"
        },
        {
            "description": "Rechteck",
            "id": "2"
        },
        {
            "description": "Dreieck",
            "id": "3"
        }
    ]
})#list of all programs

@app.route('/api/simulations/<int:simulations_id>/machine/programs/current', methods=['GET', 'POST', 'PATCH'])
def currentProgram(simulations_id):
    if request.method == 'GET':
         return jsonify({
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
})#current program state
    elif request.method == 'POST':
        program_id = request.args.get('program_id')
        return #set this program to be the current one
    elif request.method == 'PATCH':
        return jsonify({
    "parameters": [
        {
            "id": "2",
            "description": "target_amount",
            "value": "100"
        }
    ]
}) #change parameter(s) in the current program state