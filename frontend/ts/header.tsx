import React from "react";
import IconSettings from "./icons/iconSettings";
import IconArrowBack from "./icons/iconBackArrow";
import IconSave from "./icons/iconSave";
import Modal from "react-modal";
import { saveSimulation, setProtocol } from "./api-service";
import { useNavigate } from "react-router-dom";
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

export function Header(props: {
  isLandingPage: boolean;
  setRefresh: React.Dispatch<React.SetStateAction<number>>;
  refresh: number;
}) {
  const navigation = useNavigate();
  const [openSettingsModal, setOpenSettingsModal] = React.useState(false);
  const [selectedProtocol, setSelectedProtocol] =
    React.useState<string>("None");
  const [selectedRefreshTime, setSelectedRefreshTime] = React.useState<string>(
    (props.refresh / 1000).toString()
  );

  const [openSaveSimulationModal, setOpenSaveSimulationModal] =
    React.useState(false);

  const [returnToLandingPageModal, setReturnToLandingPageModal] =
    React.useState(false);

  function handleOpenSettingsModal() {
    setOpenSettingsModal(true);
  }
  function handleCloseSettingsModal() {
    setOpenSettingsModal(false);
  }
  function handleOpenSaveSimulationModal() {
    setOpenSaveSimulationModal(true);
  }
  function handleCloseSaveSimulationModal() {
    setOpenSaveSimulationModal(false);
  }
  function handleOpenReturnToLandingPageModal() {
    setReturnToLandingPageModal(true);
  }
  function handleCloseReturnToLandingPageModal() {
    setReturnToLandingPageModal(false);
  }

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const protocol = data.get("protocol");
    const refreshTime = data.get("refreshRate");
    console.log(protocol);
    setProtocol(data);
    setSelectedProtocol(protocol as string);
    setSelectedRefreshTime(refreshTime as string);
    enqueueSnackbar("refresh time set to " + refreshTime + " seconds", {
      variant: "success",
    });
    let time = parseInt(selectedRefreshTime) * 1000;
    console.log(time);
    props.setRefresh(time);
    handleCloseSettingsModal();
  }
  async function handleSaveSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const saveName = data.get("Simname");
    console.log("save simulation");
    const response = await saveSimulation(saveName as string);
    console.log(response);
    if (!response) {
      return;
    }
    handleCloseSaveSimulationModal();
  }

  function returnToLandingPage() {
    handleCloseReturnToLandingPageModal();
    navigation("/");
  }

  return (
    <div className="flex flex-row flex-shrink-0 items-center justify-between w-screen h-20 text-white bg-header-red">
      <h1 className="justify-center pl-8 text-3xl font-semibold text-center">
        Lasercutter HMI
      </h1>
      {props.isLandingPage ? null : (
        <div className="flex flex-row justify-end basis-1/6">
          <>
            <button
              className="w-10 h-10 mx-5"
              onClick={handleOpenReturnToLandingPageModal}
            >
              <IconArrowBack />
            </button>
            <Modal
              isOpen={returnToLandingPageModal}
              onRequestClose={handleCloseReturnToLandingPageModal}
              style={customStyles}
            >
              <h1 className="mb-3 text-2xl font-semibold">
                Leaving Simulation
              </h1>
              <p className="mb-3">
                You are about to leave the current Simulation. This Simulation
                will be lost if you haven't saved it.
              </p>
              <div className="flex justify-between">
                <button
                  onClick={handleCloseReturnToLandingPageModal}
                  className="px-4 py-2 mt-4 ml-1 border-2 border-black rounded-md"
                >
                  Cancel
                </button>
                <button
                  onClick={returnToLandingPage}
                  className="px-4 py-2 mt-4 ml-1 border-2 border-black rounded-md"
                >
                  Leave
                </button>
              </div>
            </Modal>
          </>
          <>
            <button
              className="w-10 h-10 mx-5"
              onClick={handleOpenSaveSimulationModal}
            >
              <IconSave />
            </button>
            <Modal
              isOpen={openSaveSimulationModal}
              onRequestClose={handleCloseSaveSimulationModal}
              style={customStyles}
            >
              <h1 className="mb-3 text-2xl font-semibold">Save Simulation</h1>
              <form onSubmit={handleSaveSubmit}>
                <label className="block" htmlFor="Simname">
                  <span className="text-gray-700">Name of Simulation</span>
                </label>
                <input
                  id="Simname"
                  type="text"
                  name="Simname"
                  placeholder="e.g. Simulation 1"
                  className="w-full px-2 py-1 mb-2 border-2 border-gray-400 rounded-lg"
                />
                <div className="flex justify-between">
                  <button
                    onClick={handleCloseSaveSimulationModal}
                    className="px-4 py-2 mt-4 ml-1 border-2 border-black rounded-md"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 mt-4 ml-1 border-2 border-black rounded-md"
                  >
                    Save
                  </button>
                </div>
              </form>
            </Modal>
            <button onClick={handleOpenSettingsModal}>
              <IconSettings className="mx-5" />
            </button>
            <Modal
              isOpen={openSettingsModal}
              onRequestClose={handleCloseSettingsModal}
              style={customStyles}
            >
              <h1 className="text-2xl font-semibold">Settings</h1>
              <form onSubmit={handleSubmit}>
                <div className="flex flex-row justify-between flex-wrap ">
                  <div className="w-1/2">
                    <h4 className="mt-4 mb-2 text-xl font-semibold">
                      Protocol
                    </h4>
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
                  </div>
                  <div className="w-1/2">
                    <h4 className="mt-4 mb-2 text-xl font-semibold">
                      Refresh Time
                    </h4>
                    <div className="flex flex-row items-center justify-between">
                      <div className="flex flex-col items-start justify-start">
                        <div className="flex flex-row items-center justify-start">
                          <input
                            type="radio"
                            value="3"
                            name="refreshRate"
                            checked={selectedRefreshTime === "3"}
                            onChange={(e) => {
                              setSelectedRefreshTime(e.target.value);
                            }}
                          />
                          <span className="mx-2">3s</span>
                        </div>
                        <div className="flex flex-row items-center justify-start">
                          <input
                            type="radio"
                            value="5"
                            name="refreshRate"
                            checked={selectedRefreshTime === "5"}
                            onChange={(e) => {
                              setSelectedRefreshTime(e.target.value);
                            }}
                          />
                          <span className="mx-2">5s</span>
                        </div>
                        <div className="flex flex-row items-center justify-start">
                          <input
                            type="radio"
                            value="10"
                            name="refreshRate"
                            checked={selectedRefreshTime === "10"}
                            onChange={(e) => {
                              setSelectedRefreshTime(e.target.value);
                            }}
                          />
                          <span className="mx-2">10s</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <button
                    className="px-4 py-2 mt-4 border-2 border-black rounded-md "
                    onClick={handleCloseSettingsModal}
                  >
                    Close
                  </button>
                  <button className="px-4 py-2 mt-4 ml-1 border-2 border-black rounded-md">
                    Apply
                  </button>
                </div>
              </form>
            </Modal>
          </>
        </div>
      )}
    </div>
  );
}

export default Header;
