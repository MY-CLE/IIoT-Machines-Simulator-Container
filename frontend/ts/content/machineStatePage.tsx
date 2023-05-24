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
  const location = useLocation(); // mit location.state.simulation_id erhält man die Simulation ID
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

  const navigation = useNavigate();

  useEffect(() => {
    (async () => {
      let newErrors = await getErrors(props.state.simulation_id | 0);

      if (newErrors.errors && newErrors.warnings) {
        // wenn es Fehlermeldungen gibt, werden diese gesetzt
        setErrors(newErrors);
      }
    })();
    const id = setInterval(async () => {
      let machineState = await getMachine(
        props.state.simulation_id ? props.state.simulation_id : 0
      );
      console.log(machineState);

      let values: StatusBarValues = getStatusbarValues(machineState);
      setStatusesBarValues(values);

      setParameters(machineState.parameters);
    }, 1000);
    return () => clearInterval(id);
  }, []);

  function getStatusbarValues(machineState: Machine): StatusBarValues {
    let runtime = 0;
    machineState.parameters.forEach((parameter) => {
      if (parameter.id === 0) runtime = parameter.value;
    });
    let errors = 0,
      warnings = 0;
    if (machineState.error_state) {
      errors = machineState.error_state.errors.length;
      warnings = machineState.error_state.warnings.length;
    }
    return {
      runtime: runtime,
      utilization: 5,
      warning: warnings,
      error: errors,
      safety_door: false,
      lock: false,
    };
  }

  async function openModal() {
    console.log("open modal");
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
        location.state.simulation_id | 0,
        password
      );
      console.log(statuscode);
    })();

    closeModal();
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
        <SelectionBar program={navigateToProgram} machine={null} />
      </div>
      <div className="flex flex-col justify-start w-full h-full p-2 text-2xl bg-gray-200 border border-t-0 border-black border-1">
        <div className="w-full h-auto text-4xl text-left">Maschinenzustand</div>
        <div className="flex flex-row flex-grow w-full h-full">
          <div className="flex flex-col items-center justify-center flex-grow w-2/5 h-full p-2 text-center">
            {parameters.map((item, index) => {
              return (
                <ParameterComponent
                  key={item.id}
                  name={item.description}
                  value={item.value}
                />
              );
            })}
          </div>
          <div className="flex flex-col w-2/5 p-2 text-2xl text-center justify-evenly">
            <div className="flex flex-grow w-full mb-5 text-2xl">
              <SendError
                name={"Error"}
                messages={errors.errors}
                color={"bg-red-500"}
              />
            </div>
            <div className="flex flex-grow w-full mt-5 text-2xl">
              <SendError
                name={"Warning"}
                messages={errors.warnings}
                color={"bg-orange-500"}
              />
            </div>
          </div>
          <div className="flex flex-grow w-1/5 p-2">
            <div className="flex items-center justify-center w-full h-full ml-10 mr-10">
              <div className="flex flex-col items-center justify-between w-full align-middle bg-white border border-black rounded-lg h-3/4">
                <div className="mt-5">
                  <IconQuitLock />
                </div>
                <button
                  className={`w-52 h-52 border border-black rounded-full mb-5 text-center pt-20 bg-red-500 font-medium`}
                  onClick={openModal}
                >
                  <span> Quittieren</span>
                </button>
                <Modal
                  isOpen={modalIsOpen}
                  onAfterOpen={afterOpenModal}
                  onRequestClose={closeModal}
                  style={customStyles}
                >
                  <h1 className="w-full font-bold">Authetification</h1>
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
        </div>
      </div>
    </div>
  );
}
export default MachineStatePage;