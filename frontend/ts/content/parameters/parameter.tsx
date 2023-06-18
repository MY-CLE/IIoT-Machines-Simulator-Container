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
interface ParameterProps {
  name: string;
  id: number;
  value: number;
  simulation_id: number;
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
      });
      console.log(status);
    })();
    closeModal();
  }

  return (
    <div className="flex flex-row border border-black w-full h-16 justify-start items-center bg-white rounded-xl">
      <div className=" ml-1 justify-start items-center flex flex-grow w-1/4 flex-wrap mr-20 font-medium text-xs sm:text-base lg:text-xl xl:text2xl">
        {props.name}
      </div>
      <div className="justify-center items-center flex flex-grow flex-wrap bg-gray-400 h-3/4 w-1/6 rounded-lg border border-black mr-2 drop-shadow text-xs sm:text-base lg:text-xl xl:text2xl">
        {props.value}
      </div>
      <button
        onClick={openModal}
        className="justify-center items-center flex flex-grow flex-wrap bg-white mr-5 w-0 h-3/4 border border-black rounded-lg drop-shadow"
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
