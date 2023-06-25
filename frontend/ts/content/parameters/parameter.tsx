import React, { useState } from "react";
import IconPen from "../../icons/iconPen";
import Modal from "react-modal";
import { authenticate, patchMachineParameter } from "../../api-service";
import { enqueueSnackbar } from "notistack";
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
  isAdminParameter: boolean;
  maxValue: number;
}
function ParameterComponent(props: ParameterProps) {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  async function openModal() {
    console.log("open modal");
    setModalIsOpen(true);
  }
  function closeModal() {
    setModalIsOpen(false);
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formdata = new FormData(event.currentTarget);
    closeModal();

    if (props.isAdminParameter) {
      let res = await authenticate(formdata.get("password")?.toString()!);
      if (res.status !== 200) {
        return;
      }
    }
    if (!typeCheck(formdata)) {
      return;
    }

    let status = await patchMachineParameter({
      id: props.id,
      value: parseInt(formdata.get("value")?.toString()!),
      description: props.name,
      isAdminParameter: props.isAdminParameter,
      maxValue: props.maxValue,
    });
    console.log(status);
  }

  function typeCheck(formdata: FormData) {
    if (formdata.get("value")?.toString() === "") {
      enqueueSnackbar("Please enter a value", { variant: "error" });
      return false;
    } else if (isNaN(parseInt(formdata.get("value")?.toString()!))) {
      enqueueSnackbar("Please enter a number", { variant: "error" });
      return false;
    } else if (
      parseInt(formdata.get("value")?.toString()!) > props.maxValue ||
      parseInt(formdata.get("value")?.toString()!) < 0
    ) {
      enqueueSnackbar("Please enter a number between 0 and " + props.maxValue, {
        variant: "error",
      });
      return false;
    }
    return true;
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
          props.isAdminParameter ? "bg-red-300" : "bg-slate-100"
        } flex flex-wrap items-center justify-center flex-grow w-0 mr-5 border border-black rounded-lg h-3/4 drop-shadow`}
      >
        <IconPen />
      </button>
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        style={customStyles}
      >
        <form className="w-full" onSubmit={handleSubmit}>
          <h1 className="w-full font-bold">{props.name}</h1>
          <span className="w-full"></span>
          <label className="w-full " htmlFor="parameterInput">
            New Value:{" "}
          </label>
          <input
            placeholder={props.value.toString()}
            id="parameterInput"
            name="value"
            type="text"
            className="w-full text-center border border-black rounded-lg "
          />
          {props.isAdminParameter ? (
            <>
              <label className="w-full" htmlFor="paswordInput">
                Admin Password:{" "}
              </label>
              <input
                placeholder={"password"}
                id="paswordInput"
                name="password"
                type="password"
                className="w-full text-center border border-black rounded-lg "
              />
            </>
          ) : (
            <></>
          )}
          <button
            type="submit"
            className="w-full mt-5 border border-black rounded-lg"
          >
            submit
          </button>
        </form>
      </Modal>
    </div>
  );
}

export default ParameterComponent;
