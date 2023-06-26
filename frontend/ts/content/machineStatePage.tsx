import React, { useEffect, useState } from "react";
import ParameterComponent from "./parameters/parameter";
import SendError from "./parameters/sendError";
import IconQuitLock from "../icons/iconQuitLock";
import { authenticate, clearNotifications, getErrors, getProgram, resetMachine } from "../api-service";
import { Errors, Machine, Parameter } from "../interfaces";
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

const listModalStyles = {};
Modal.setAppElement("#root");

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
  machine: Machine,
  getProgramState: any;
}) {
  const [errors, setErrors] = useState<Errors>({
    errors: [{ id: 0, name: "" }],
    warnings: [{ id: 0, name: "" }],
  });
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [listModal, setListModal] = useState(false);

  useEffect(() => {
    let errorsValues: Errors | null = null;
    (async () => {
      // when the page is loaded the first time, the errors are fetched
      let newErrors: Response | null = await getErrors();
      if (newErrors) {
        errorsValues = (await newErrors.json()) as Errors;
        setErrors(errorsValues);
        return;
      }
    })();
  }, []);

  async function openModal() {
    console.log("open modal");
    setModalIsOpen(true);
  }
  function afterOpenModal() {}
  function closeModal() {
    setModalIsOpen(false);
    closeListModal();
  }

  async function sendQuittieren() {
    let inputfield = document.getElementById(
      "inputPassword"
    ) as HTMLInputElement;
    let password = inputfield.value;
    let response: any = null;
    response = await authenticate(password);

    if (response.status == 200) {
      let clearErrors = await clearNotifications();
      if (clearErrors && clearErrors.status == 200) {
        closeModal();
      }
    }
  }

  function openListModal() {
    setListModal(true);
  }

  function closeListModal() {
    setListModal(false);
  }

  async function resetMachineValues(){
      const response = await resetMachine();
      props.getProgramState();
  }

  return (
    <div className="flex flex-col flex-nowrap h-full justify-start text-2xl p-4 bg-gray-200 border border-t-0 border-black border-1">
      <div className="w-full h-auto text-4xl text-left sm:text-base mb-2 lg:text-xl xl:text-2xl 2xl:text-3xl 3xl:text-4xl">
        Machine State
      </div>
      <div className="flex flex-row justify-between h-full">
        <div className="flex flex-col items-center justify-between w-1/3 h-full text-center">
          {props.machine.parameters.map((item: Parameter, index) => {
            return (
              <ParameterComponent
                key={item.id}
                name={item.description}
                value={item.value}
                id={item.id}
                isAdminParameter={item.isAdminParameter}
              />
            );
          })}
        </div>
        <div className="flex justify-center h-full w-3/20">
          <div className="flex items-center justify-center w-full h-full">
            <div className="grid w-full h-full bg-white border border-black rounded-lg grid-rows-3">
              <div className="flex justify-center items-center">
                <IconQuitLock />
              </div>

              <div className="flex justify-center items-center">
                <button className="w-2/3 bg-yellow-400 border border-black rounded-md shadow h-14 text-xs sm:text-base lg:text-sm xl:text-lg 2xl:text-xl 3xl:text-2xl"
                onClick={resetMachineValues}
                >
                  Reset Machine
                </button>
              </div>

              <div className="flex justify-center items-center p-2">
                <button
                  className={`flex items-center justify-center border border-black rounded-full bg-red-500 text-black font-normal`}
                  style={{
                    width: "50%",
                    height: "100%",
                    minWidth: "50px",
                    minHeight: "50px",
                  }}
                  onClick={openListModal}
                >
                  <span className="text-xs sm:text-base lg:text-sm xl:text-lg 2xl:text-xl 3xl:text-2xl">
                    {" "}
                    Acknowledge
                  </span>
                </button>
              </div>
              <Modal
                isOpen={listModal}
                onAfterOpen={afterOpenModal}
                onRequestClose={closeListModal}
                style={{
                  overlay: {
                    position: "fixed",
                    top: "0",
                    left: "0",
                    right: "0",
                    bottom: "0",
                  },
                  content: {
                    width: "50%",
                    height: "80%",
                    top: "50%",
                    left: "50%",
                    transform: "translate(-50%, -50%)",
                    backgroundColor: "#F2F2F2",
                    padding: "0",
                  },
                }}
              >
                
                  <div className="flex flex-col items-center justify-between w-full h-full bg-white border border-gray-500">
                    <h1 className="mt-5 text-xl font-medium">Acknowledge Errors & Warnings </h1>
                    <div className="w-3/4">
                      {props.machine.errorState.errors.length > 0 && (
                        <>
                          <h1 className="text-lg">Errors:</h1>
                          <br />
                          <table className="border-collapse w-full">
                            <thead>
                              <tr>
                                <th className="w-1/4 px-4 py-2 border border-gray-500">
                                  Time
                                </th>
                                <th className="w-3/4 px-4 py-2 border border-gray-500">
                                  Description
                                </th>
                              </tr>
                            </thead>
                            <tbody>
                              {props.machine.errorState.errors.map(
                                (error: { id: number; name: string }) => (
                                  <tr key={error.id}>
                                    <td className="w-1/4 px-4 py-2 border border-gray-500">
                                      {error.name[0]}
                                    </td>
                                    <td className="w-3/4 px-4 py-2 border border-gray-500">
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
                    <div className="w-3/4">
                      {props.machine.errorState.warnings.length > 0 && (
                        <>
                          <br />
                          <h1 className="text-lg">Warnings:</h1>
                          <br />
                          <table className="border-collapse w-full">
                            <thead>
                              <tr>
                                <th className="w-1/4 px-4 py-2 border border-gray-500">
                                  Time
                                </th>
                                <th className="w-3/4 px-4 py-2 border border-gray-500">
                                  Description
                                </th>
                              </tr>
                            </thead>
                            <tbody>
                              {props.machine.errorState.warnings.map(
                                (warning: { id: number; name: string }) => (
                                  <tr key={warning.id}>
                                    <td className="w-1/4 px-4 py-2 border border-gray-500">
                                      {warning.name[0]}
                                    </td>
                                    <td className="w-3/4 px-4 py-2 border border-gray-500">
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
                      className="px-4 py-2 mt-4 border border-gray-500 rounded mb-5 text-lg font-medium"
                      onClick={openModal}
                    >
                      Acknowledge
                    </button>
                  </div>
              </Modal>

              <Modal
                isOpen={modalIsOpen}
                onAfterOpen={afterOpenModal}
                onRequestClose={closeModal}
                style={customStyles}
              >
                <h1 className="w-full font-bold">Authentification</h1>
                <span className="w-full">Please enter the admin password</span>
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
                  Send
                </button>
              </Modal>
            </div>
          </div>
        </div>
        <div className="flex flex-col justify-between w-1/3 h-full text-2xl text-center">
          <div className="flex w-full text-2xl h-2/5">
            <SendError
              name={"Error"}
              messages={errors.errors}
              color={"bg-red-500"}
            />
          </div>
          <div className="flex w-full h-2/5 text-2xl">
            <SendError
              name={"Warning"}
              messages={errors.warnings}
              color={"bg-orange-500"}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
export default MachineStatePage;
