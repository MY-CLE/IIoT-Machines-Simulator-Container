import React, { useEffect, useState } from "react";
import StatusBar from "./statusbar/statusBar";
import SelectionBar from "./machineOrProgramBar/selectionBar";
import ParameterComponent from "./parameters/parameter";
import SendError from "./parameters/sendError";
import IconQuitLock from "../icons/iconQuitLock";
import { useLocation, useNavigate } from "react-router-dom";
import { authenticate, getErrors, getMachine } from "../api-service";
import { Errors, Machine, Parameter, StatusBarValues } from "../interfaces";
import Modal from "react-modal";

const customStyles = {
  content: {
    width: "25%",
    top: "50%",
    left: "50%",
    right: "auto",
    bottom: "auto",
    marginRight: "-50%",
    transform: "translate(-50%, -50%)",
    backgroundColor: "#F2F2F2",
  },
};
Modal.setAppElement("#root");

const paramterDefault: Array<Parameter> = [
  { id: 0, description: "", value: 0 },
  { id: 1, description: "", value: 0 },
];
function MachineStatePage(props: {
  state: {
    simulation_id: number;
    program_id: number;
  };
  setState: React.Dispatch<
    React.SetStateAction<{
      simulation_id: number;
      program_id: number;
    }>
  >;
}) {
  const [parameters, setParameters] =
    useState<Array<Parameter>>(paramterDefault); // Array mit Parametern
  const [errors, setErrors] = useState<Errors>({
    errors: [{ id: 0, name: "" }],
    warnings: [{ id: 0, name: "" }],
  });
  const [statuesBarValues, setStatusesBarValues] = useState<StatusBarValues>({
    runtime: 0,
    utilization: 0,
    error: 0,
    warning: 0,
    safety_door: false,
    lock: false,
  }); // Werte für die Statusbar
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [listPopup, setListPopup] = useState(false);
  const [activeErrorsAndWarnings, setActiveErrorsAndWarnings] = useState<{
    errors: { id: number; name: string }[];
    warnings: { id: number; name: string }[];
  }>({
    errors: [],
    warnings: [],
  });

  const navigation = useNavigate();

  useEffect(() => {
    (async () => {
      // when the page is loaded the first time, the errors are fetched
      let newErrors = await getErrors(props.state.simulation_id | 0);
      console.log("new Errors getting fetched");
      if (newErrors.errors && newErrors.warnings) {
        setErrors(newErrors);
      }

      let machineState = await getMachine(
        props.state.simulation_id ? props.state.simulation_id : 0
      );
      console.log(machineState);

      let values: StatusBarValues = getStatusbarValues(machineState);
      setStatusesBarValues(values);

      setParameters(machineState.parameters);
    })();

    const id = setInterval(async () => {
      let machineState = await getMachine(
        props.state.simulation_id ? props.state.simulation_id : 0
      );
      console.log(machineState);

      let values: StatusBarValues = getStatusbarValues(machineState);
      setStatusesBarValues(values);

      setParameters(machineState.parameters);
      setActiveErrorsAndWarnings(machineState.error_state);
    }, 5000);
    return () => clearInterval(id);
  }, []);

  function getStatusbarValues(machineState: Machine): StatusBarValues {
    let runtime = machineState.parameters[0].value;
    let errors = 0,
      warnings = 0,
      safetyDoorStatus = false;
    if (machineState.error_state) {
      errors = machineState.error_state.errors.length;
      warnings = machineState.error_state.warnings.length;
      for(const err of machineState.error_state.errors){
        if(err.name[1] === 'Safety door is open! Close it.'){
          safetyDoorStatus = true;
        }
      }
    }
    return {
      runtime: runtime,
      utilization: 5,
      warning: warnings,
      error: errors,
      safety_door: safetyDoorStatus,
      lock: false,
    };
  }

  async function openModal() {
    console.log("open modal");
    setListPopup(false);
    setModalIsOpen(true);
  }
  function afterOpenModal() {}
  function closeModal() {
    setModalIsOpen(false);
  }

  function sendQuittieren() {
    let inputfield = document.getElementById(
      "inputPassword"
    ) as HTMLInputElement;
    let password = inputfield.value;
    console.log(password);
    (async () => {
      let statuscode = await authenticate(
        props.state.simulation_id | 0,
        password
      );
      console.log(statuscode);
    })();

    closeModal();
  }

  function openListPopup() {
    setListPopup(true);
    //console.log(activeErrorsAndWarnings.errors[0]);
    //console.log(activeErrorsAndWarnings.errors[0].id);
    //console.log(activeErrorsAndWarnings.errors[0].name[0]);
  }

  function navigateToProgram() {
    console.log(props.state.program_id);
    if (props.state.program_id === -1) {
      navigation(`/programs`);
    } else {
      navigation(`/program/current`);
    }
  }

  return (
    <div className="flex flex-col flex-grow flex-nowrap">
      <div className="flex flex-row items-center justify-start h-32 max-w-full bg-gray-300">
        <div className="w-full text-2xl">
          <StatusBar
            runtime={statuesBarValues.runtime}
            utilization={statuesBarValues.utilization}
            error={statuesBarValues.error}
            warning={statuesBarValues.warning}
            safety_door={statuesBarValues.safety_door}
            lock={statuesBarValues.lock}
          />
        </div>
      </div>
      <div>
        <SelectionBar whichPage={"machine"} />
      </div>
      <div className="flex flex-col justify-start w-full h-full p-4 text-2xl bg-gray-200 border border-t-0 border-black border-1">
        {listPopup && (
          <div className="fixed top-0 left-0 z-50 w-full h-full bg-gray-800 bg-opacity-50 flex items-center justify-center">
            <div className="bg-white w-1/2 h-full p-4 flex flex-col justify-between items-center border border-gray-500">
              <div>
                {activeErrorsAndWarnings.errors.length > 0 && (
                  <>
                    <h1>Errors:</h1>
                    <br />
                    <table className="border-collapse">
                      <thead>
                        <tr>
                          <th className="border border-gray-500 px-4 py-2 w-1/4">
                            Time
                          </th>
                          <th className="border border-gray-500 px-4 py-2 w-3/4">
                            Description
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {activeErrorsAndWarnings.errors.map(
                          (error: { id: number; name: string }) => (
                            <tr key={error.id}>
                              <td className="border border-gray-500 px-4 py-2 w-1/4">
                                {error.name[0]}
                              </td>
                              <td className="border border-gray-500 px-4 py-2 w-3/4">
                                {error.name[1]}
                              </td>
                            </tr>
                          )
                        )}
                      </tbody>
                    </table>
                  </>
                )}
              </div>
              <div>
                {activeErrorsAndWarnings.warnings.length > 0 && (
                  <>
                    <br />
                    <h1>Warnings:</h1>
                    <br />
                    <table className="border-collapse">
                      <thead>
                        <tr>
                          <th className="border border-gray-500 px-4 py-2 w-1/4">
                            Time
                          </th>
                          <th className="border border-gray-500 px-4 py-2 w-3/4">
                            Description
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {activeErrorsAndWarnings.warnings.map(
                          (warning: { id: number; name: string }) => (
                            <tr key={warning.id}>
                              <td className="border border-gray-500 px-4 py-2 w-1/4">
                                {warning.name[0]}
                              </td>
                              <td className="border border-gray-500 px-4 py-2 w-3/4">
                                {warning.name[1]}
                              </td>
                            </tr>
                          )
                        )}
                      </tbody>
                    </table>
                  </>
                )}
              </div>
              <button
                className="border border-gray-500 rounded px-4 py-2 mt-4"
                onClick={openModal}
              >
                Quittieren
              </button>
            </div>
          </div>
        )}
        <div className="w-full h-auto text-left text-4xl sm:text-base lg:text-xl xl:text-2xl 2xl:text-3xl 3xl:text-4xl">Maschinenzustand</div>
        <div className="flex flex-row w-full h-full py-5 justify-between">
          <div className="flex flex-col items-center justify-between w-1/3 h-full text-center">
            {parameters.map((item, index) => {
              return (
                <ParameterComponent
                  simulation_id={props.state.simulation_id}
                  key={item.id}
                  name={item.description}
                  value={item.value}
                  id={item.id}
                />
              );
            })}
          </div>
          <div className="flex w-3/20 h-full justify-center">
            <div className="flex items-center justify-center w-full h-full">
              <div className="flex flex-col items-center justify-between w-full h-full align-middle bg-white border border-black rounded-lg">
                <div className="mt-5">
                  <IconQuitLock />
                </div>
              
                <button
                  className={`flex items-center justify-center border border-black rounded-full mb-5 bg-red-500 text-black font-medium`}
                  style={{ width: "10vw", height: "10vw", minWidth: "50px", minHeight: "50px" }}
                  onClick={openListPopup}
                >
                  <span className="text-xs sm:text-base lg:text-xl"> Quittieren</span>
                </button>
  
                <Modal
                  isOpen={modalIsOpen}
                  onAfterOpen={afterOpenModal}
                  onRequestClose={closeModal}
                  style={customStyles}
                >
                  <h1 className="w-full font-bold">Authentification</h1>
                  <span className="w-full">
                    Bitte geben sie das Administrator Passwort ein
                  </span>
                  <input
                    placeholder=""
                    id="inputPassword"
                    type="password"
                    className="w-full text-center border border-black rounded-lg "
                  />
                  <button
                    type="submit"
                    onClick={sendQuittieren}
                    className="w-full mt-5 border border-black rounded-lg "
                  >
                    send
                  </button>
                </Modal>
              </div>
            </div>
          </div>
          <div className="flex flex-col w-1/3 h-full text-2xl text-center justify-between">
            <div className="flex flex-grow w-full mb-5 text-2xl">
              <SendError
                simulationID={props.state.simulation_id}
                name={"Error"}
                messages={errors.errors}
                color={"bg-red-500"}
              />
            </div>
            <div className="flex flex-grow w-full mt-5 text-2xl">
              <SendError
                simulationID={props.state.simulation_id}
                name={"Warning"}
                messages={errors.warnings}
                color={"bg-orange-500"}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
export default MachineStatePage;
