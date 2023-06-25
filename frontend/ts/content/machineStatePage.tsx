import React, { useEffect, useState } from "react";
import ParameterComponent from "./parameters/parameter";
import SendError from "./parameters/sendError";
import IconQuitLock from "../icons/iconQuitLock";
import { authenticate, clearNotifications, getErrors } from "../api-service";
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
Modal.setAppElement("#root");

function MachineStatePage(props: { machine: Machine }) {
  const [errors, setErrors] = useState<Errors>({
    errors: [{ id: 0, name: "" }],
    warnings: [{ id: 0, name: "" }],
  });
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [listPopup, setListPopup] = useState(false);

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
    setListPopup(false);
    setModalIsOpen(true);
  }
  function afterOpenModal() {}
  function closeModal() {
    setModalIsOpen(false);
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

  function openListPopup() {
    setListPopup(true);
  }

  return (
    <div className="flex flex-col flex-grow flex-nowrap">
      <div className="flex flex-col justify-start w-full h-full p-4 text-2xl bg-gray-200 border border-t-0 border-black border-1">
        {listPopup && (
          <div className="fixed top-0 left-0 z-50 flex items-center justify-center w-full h-full bg-gray-800 bg-opacity-50">
            <div className="flex flex-col items-center justify-between w-1/2 h-full p-4 bg-white border border-gray-500">
              <div>
                {props.machine.errorState.errors.length > 0 && (
                  <>
                    <h1>Errors:</h1>
                    <br />
                    <table className="border-collapse">
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
              <div>
                {props.machine.errorState.warnings.length > 0 && (
                  <>
                    <br />
                    <h1>Warnings:</h1>
                    <br />
                    <table className="border-collapse">
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
                className="px-4 py-2 mt-4 border border-gray-500 rounded"
                onClick={openModal}
              >
                Acknowledge
              </button>
            </div>
          </div>
        )}
        <div className="w-full h-auto text-4xl text-left sm:text-base lg:text-xl xl:text-2xl 2xl:text-3xl 3xl:text-4xl">
          Machine State
        </div>
        <div className="flex flex-row justify-between w-full h-full py-5">
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
              <div className="flex flex-col items-center justify-between w-full h-full align-middle bg-white border border-black rounded-lg">
                <div className="mt-5">
                  <IconQuitLock />
                </div>

                <button
                  className={`flex items-center justify-center border border-black rounded-full mb-5 bg-red-500 text-black font-medium`}
                  style={{
                    width: "10vw",
                    height: "10vw",
                    minWidth: "50px",
                    minHeight: "50px",
                  }}
                  onClick={openListPopup}
                >
                  <span className="text-xs sm:text-base lg:text-xl">
                    {" "}
                    Acknowledge
                  </span>
                </button>

                <Modal
                  isOpen={modalIsOpen}
                  onAfterOpen={afterOpenModal}
                  onRequestClose={closeModal}
                  style={customStyles}
                >
                  <h1 className="w-full font-bold">Authentification</h1>
                  <span className="w-full">
                    Please enter the admin password
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
          <div className="flex flex-col justify-between w-1/3 h-full text-2xl text-center">
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
        </div>
      </div>
    </div>
  );
}
export default MachineStatePage;
