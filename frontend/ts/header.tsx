import React from "react";
import IconSettings from "./icons/iconSettings";
import IconArrowBack from "./icons/iconBackArrow";
import Modal from "react-modal";
import { setProtocol } from "./api-service";

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

export function Header() {
  const [openSettingsModal, setOpenSettingsModal] = React.useState(false);
  const [selectedProtocol, setSelectedProtocol] =
    React.useState<string>("None");
  function handleOpenSettingsModal() {
    setOpenSettingsModal(true);
  }
  function handleCloseSettingsModal() {
    setOpenSettingsModal(false);
  }
  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const protocol = data.get("protocol");
    console.log(protocol);
    setProtocol(data);
    setSelectedProtocol(protocol as string);
    handleCloseSettingsModal();
  }

  return (
    <header className="flex flex-row items-center justify-between w-screen h-20 text-white bg-header-red">
      <h1 className="justify-center pl-8 text-3xl font-semibold text-center">
        Lasercutter HMI
      </h1>
      <div className="flex flex-row justify-end basis-1/6">
        <button
          className="mx-3 w-10 h-10"
          onClick={() => {
            window.location.href = "/";
          }}
        >
          <IconArrowBack />
        </button>
        <button onClick={handleOpenSettingsModal}>
          <IconSettings className="mx-3" />
        </button>
        <Modal
          isOpen={openSettingsModal}
          onRequestClose={handleCloseSettingsModal}
          style={customStyles}
        >
          <h1 className="text-2xl font-semibold">Settings</h1>
          <h4 className="mt-4 text-xl font-semibold mb-2">Protocol</h4>
          <form onSubmit={handleSubmit}>
            <div className="flex flex-col items-start justify-start">
              <div className="flex flex-row items-center justify-start">
                <input
                  type="radio"
                  value="None"
                  name="protocol"
                  checked={selectedProtocol === "None"}
                  onChange={(e) => {
                    setSelectedProtocol(e.target.value);
                  }}
                />
                <span className="mx-2">None</span>
              </div>
              <div className="flex flex-row items-center justify-start">
                <input
                  type="radio"
                  value="Modbus/TCP"
                  name="protocol"
                  checked={selectedProtocol === "Modbus/TCP"}
                  onChange={(e) => {
                    setSelectedProtocol(e.target.value);
                  }}
                />
                <span className="mx-2">Modbus/TCP</span>
              </div>
              <div className="flex flex-row items-center justify-start">
                <input
                  type="radio"
                  value="OPCUA"
                  name="protocol"
                  checked={selectedProtocol === "OPCUA"}
                  onChange={(e) => {
                    setSelectedProtocol(e.target.value);
                  }}
                />
                <span className="mx-2">OPCUA</span>
              </div>
            </div>
            <div className="flex flex-row items-center justify-end">
              <button
                className="px-4 py-2 mt-4  rounded-md border-2 border-black "
                onClick={handleCloseSettingsModal}
              >
                Close
              </button>
              <button className="px-4 py-2 ml-1 mt-4 rounded-md border-2 border-black">
                Anwenden
              </button>
            </div>
          </form>
        </Modal>
      </div>
    </header>
  );
}

export default Header;
