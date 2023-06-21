import React, { useState } from "react";
import IconPen from "../../icons/iconPen";
import Modal from "react-modal";
import { patchMachineParameter } from "../../api-service";
Modal.setAppElement("#root");
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
export interface ParameterProps {
  name: string;
  id: number;
  value: number;
  simulation_id: number;
  isAdminParameter: boolean;
}
function ParameterComponent(props: ParameterProps) {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  async function openModal() {
    console.log("open modal");
    setModalIsOpen(true);
  }
  function afterOpenModal() {}
  function closeModal() {
    setModalIsOpen(false);
  }

  function postNewParameter() {
    const parameterInput = document.getElementById(
      "parameterInput"
    ) as HTMLInputElement;
    console.log(parameterInput.value);
    (async () => {
      let status = await patchMachineParameter(props.simulation_id, {
        id: props.id,
        value: parseInt(parameterInput.value),
        description: props.name,
        isAdminParameter: props.isAdminParameter,
      });
      console.log(status);
    })();
    closeModal();
  }

  return (
    <div className="flex flex-row items-center justify-start w-full h-16 bg-white border border-black rounded-xl">
      <div className="flex flex-wrap items-center justify-start flex-grow w-1/4 ml-1 mr-20 text-xs font-medium sm:text-base lg:text-xl xl:text2xl">
        {props.name}
      </div>
      <div className="flex flex-wrap items-center justify-center flex-grow w-1/6 mr-2 text-xs bg-gray-400 border border-black rounded-lg h-3/4 drop-shadow sm:text-base lg:text-xl xl:text2xl">
        {props.value}
      </div>
      <button
        onClick={openModal}
        className={`${
          props.isAdminParameter ? "bg-red-500" : "bg-slate-100"
        } flex flex-wrap items-center justify-center flex-grow w-0 mr-5 border border-black rounded-lg h-3/4 drop-shadow`}
      >
        <IconPen />
      </button>
      <Modal
        isOpen={modalIsOpen}
        onAfterOpen={afterOpenModal}
        onRequestClose={closeModal}
        style={customStyles}
      >
        <h1 className="w-full font-bold">{props.name}</h1>
        <span className="w-full"></span>
        <input
          placeholder={props.value.toString()}
          id="parameterInput"
          type="text"
          className="w-full text-center border border-black rounded-lg "
        />
        <button
          type="submit"
          onClick={postNewParameter}
          className="w-full mt-5 border border-black rounded-lg "
        >
          send
        </button>
      </Modal>
    </div>
  );
}

export default ParameterComponent;
