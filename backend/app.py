#FIND ALL INFORMATION ABOUT THIS REST API HERE: https://mycle-iiot.postman.co/workspace/57d25410-5868-44d8-b432-6a596c9b6b73/documentation/24866334-307d89c6-7fe0-4a54-9190-dc6372836be1?entity=&branch=&version=


from venv import logger
from flask_cors import CORS
from datetime import datetime
from logic.simulator import Simulator
from database.handler.databaseHandler import DatabaseHandler
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)
CORS(app)

# Initialize Simulator
simulator = Simulator()


# ------------------------------------------------------------------------------
# Get Simulations or save Simulation
@app.route('/api/simulations', methods=['GET', 'POST'])
def simulations():
    if request.method == 'GET':
        json = {
          "simulations": []
        }
        for sim in DatabaseHandler.selectMachineStates():
            json["simulations"].append({
              "id": sim.getId(),
              "description": sim.getName(),
              "last_edited": sim.getLastEdited(),
            })
        return make_response(json, 200) # give back all sims
    
    elif request.method == 'POST':
        simulator.saveSimulation(request.form['name']) #save a new sim
        return make_response("Simulation saved successfully", 201)

# ------------------------------------------------------------------------------
# Start/Load or Delete Simulation
@app.route('/api/simulations/<int:simulationId>', methods=['PUT', 'DELETE'])
def simulation(simulationId):
    if request.method == 'PUT':
        if simulationId == 0:
            #reset machine
            simulator.startMachine()
            return make_response("Simulation created successfully", 201)
        else:
            simulator.loadSimulation(simulationId) #load a selected sim
            return make_response(jsonify(simulator.loadSimulationById(simulationId)), 200) #give back the selected sim
    
    elif request.method == 'DELETE':
        if DatabaseHandler.selectMachineState(simulationId) != None: #delete a selected sim
            simulator.deleteSimulationById(simulationId)
            return make_response(f"Simulation '{simulationId}' was deleted successfully", 200)
        else:
            return make_response(f"Simulation '{simulationId}' does not exist", 400)
# ------------------------------------------------------------------------------
# Protocol
@app.route('/api/simulations/protocol', methods=['PATCH'])
def simulationsProtocol():
  if request.method == 'PATCH':
    if request.form['protocol'] == 'OPCUA' or request.form['protocol'] == 'Modbus/TCP' or request.form['protocol'] == 'None':
        simulator.setProtocol(request.form['protocol'])
        return make_response(f"Protocol '{request.form['protocol']}' was set successfully", 200)
    else:
        return make_response(f"Protocol '{request.form['protocol']}' is not supported", 400)

# ------------------------------------------------------------------------------
# Machine
@app.route('/api/simulations/machine', methods=['GET', 'PATCH'])
def machines():
    if request.method == 'GET':
        simulator.updateSimulation(datetime.now())
        return make_response(jsonify(simulator.simulatedMachine.getMachineStateSnapshot()), 200) #give back the current machine state
    elif request.method == 'PATCH':
        simulator.updateMachineStateParameters(request.get_json())
        return make_response("Machine state parameters updated successfully", 200)  #change parameter(s) in the machine state

# ------------------------------------------------------------------------------
# Machine Authentication
@app.route('/api/simulations/machine/auth', methods=['PUT'])
def auth():
    if request.method == 'PUT':
      for admin in DatabaseHandler.selectAdminUsers():
        if(admin.getPassword() == request.form['password']):
            return make_response("Successefully authenticated", 200)
        return make_response("Authentication failed", 401)

# ------------------------------------------------------------------------------
# Machine Notifications
@app.route('/api/simulations/machine/notifications', methods=['GET', 'POST', 'PATCH'])
def error():
    if request.method == 'GET':
        return make_response(simulator.notification.getNotificationsJSON(), 200) #list of all errors and warnings
    
    elif request.method == 'POST':
        error_id = request.form['error_id']
        warning_id = request.form['warning_id']

        if error_id == '' and warning_id == '':
            return make_response('No Error Id or Warning Id provided', 400)
        if error_id and warning_id == '':
            simulator.notification.setSelectedError(error_id)
            simulator.stopProgram()
            return make_response('Error was successfully set', 200)
        elif warning_id and error_id == '':
            simulator.notification.setSelectedWarning(warning_id)
            return make_response('Warning was successfully set', 200)

    elif request.method == 'PATCH':
        simulator.notification.errors = []
        simulator.notification.warnings = []
        return make_response('Errors and Warnings were successfully reset', 200)

# ------------------------------------------------------------------------------
# Programs
@app.route('/api/simulations/machine/programs', methods=['GET'])
def allPrograms():
    if request.method == 'GET':
        listOfPrograms = simulator.getPrograms()
        data = {"programs": []}
        for program in listOfPrograms:
            data["programs"].append(program.toJSON())
        return make_response(jsonify(data), 200) #list of all programs

# ------------------------------------------------------------------------------
# Current Program
@app.route('/api/simulations/machine/programs/current', methods=['GET', 'PUT', 'PATCH'])
def currentProgram():
    if request.method == 'GET':
         return make_response(jsonify(simulator.simulatedProgram.getProgramStateSnapshot()), 200) #current program state
    
    elif request.method == 'PUT':
        programId = request.form['program_id']
        machineProgram = DatabaseHandler().selectMachineProgramById(programId)
        simulator.simulatedProgram.setMachineProgram(machineProgram)
        simulator.simulatedMachine.isProgramRunning = False
        return make_response("Program was successfully changed", 200) #set a new program
    
    elif request.method == 'PATCH':
        json = request.get_json()
        if(json['value'] == "start"):
            simulator.startProgram()
            return make_response("Program was successfully started", 200)
        elif(json['value'] == "stop"):
            simulator.stopProgram()
            return make_response("Program was successfully stopped", 200)
        elif(json['value'] == "reset"):
            simulator.resetSimulator()
            return make_response("Program was successfully reset", 200) 
        return make_response("Program was successfully changed", 200) #change parameter(s) in the current program state


  
    