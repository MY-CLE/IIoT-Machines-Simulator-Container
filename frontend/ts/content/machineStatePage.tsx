import React, { useEffect, useState } from "react";
import StatusBar from "./statusbar/statusBar";
import SelectionBar from "./machineOrProgramBar/selectionBar";
import ParameterComponent from "./parameters/parameter";
import SendError from "./parameters/sendError";
import IconQuitLock from "../icons/iconQuitLock";
import { useLocation, useNavigate } from "react-router-dom";
import { authenticate, getErrors, getMachine } from "../api-service";
import { Errors, Machine } from "../interfaces";
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

const paramterDefault: Machine = {
  parameters: [
    { id: 0, description: "Kühlwassertemperatur", value: 0 },
    { id: 1, description: "Kühlwasserstand", value: 0 },
  ],
};
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
  const [parameters, setParameters] = useState<Machine>(paramterDefault); // Array mit Parametern
  const [errors, setErrors] = useState<Errors>({
    errors: [{ id: 0, name: "" }],
    warnings: [{ id: 0, name: "" }],
  });
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
      let newParameters = await getMachine(
        props.state.simulation_id ? props.state.simulation_id : 0
      );
      console.log(newParameters);

      setParameters(newParameters);
    }, 1000);
    return () => clearInterval(id);
  }, []);

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
      <div className="max-w-full flex flex-row items-center justify-start h-32 bg-gray-300">
        <div className="w-full text-2xl">
          <StatusBar />
        </div>
      </div>
      <div>
        <SelectionBar program={navigateToProgram} machine={null} />
      </div>
      <div className="flex flex-col justify-start h-full w-full text-2xl border border-black border-1 border-t-0 bg-gray-200 p-2">
        <div className="w-full h-auto text-4xl text-left">Maschinenzustand</div>
        <div className="flex flex-row w-full h-full flex-grow">
          <div className="text-center w-2/5 flex flex-col flex-grow h-full justify-center items-center p-2">
            {parameters.parameters.map((item, index) => {
              return (
                <ParameterComponent
                  key={item.id}
                  name={item.description}
                  value={item.value}
                />
              );
            })}
          </div>
          <div className=" w-2/5 flex flex-col justify-evenly text-center text-2xl p-2">
            <div className="w-full text-2xl flex flex-grow mb-5">
              <SendError
                name={"Error"}
                messages={errors.errors}
                color={"bg-red-500"}
              />
            </div>
            <div className="w-full text-2xl flex flex-grow mt-5">
              <SendError
                name={"Warning"}
                messages={errors.warnings}
                color={"bg-orange-500"}
              />
            </div>
          </div>
          <div className="w-1/5 flex flex-grow p-2">
            <div className="ml-10 mr-10 h-full w-full flex justify-center items-center">
              <div className="bg-white w-full h-3/4 border border-black rounded-lg flex flex-col justify-between items-center align-middle">
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
                    className=" border border-black rounded-lg w-full text-center"
                  />
                  <button
                    type="submit"
                    onClick={sendQuittieren}
                    className=" border border-black rounded-lg w-full mt-5 "
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
