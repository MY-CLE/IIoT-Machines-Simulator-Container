import React from "react";
import { useState } from "react";
import Modal, { Styles } from "react-modal";
import {
  createSimulation,
  getSimultions,
  loadSimulation,
  postSimulation,
} from "../api-service";
import { Simulation } from "../interfaces";
import { useNavigate } from "react-router-dom";

const url = "/simulator";
Modal.setAppElement("#root");
const customStyles: Styles = {
  content: {
    position: "absolute",
    width: "35%",
    top: "50%",
    left: "50%",
    right: "auto",
    bottom: "auto",
    marginRight: "-50%",
    transform: "translate(-50%, -50%)",
    backgroundColor: "#F2F2F2",
  },
};
function LandingPage(props: {
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
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [simulations, setSimulations] = useState<[Simulation]>([
    { id: 0, last_edited: new Date(), description: "" },
  ]);
  const navigate = useNavigate();

  async function openModal() {
    console.log("open modal");
    let sims = await getSimultions();
    console.log(sims.simulations);

    if (sims.simulations) {
      setSimulations(sims.simulations);
      setModalIsOpen(true);
    } else {
      console.log("no simulations found");
    }
  }
  function closeModal() {
    setModalIsOpen(false);
  }

  async function startSimulation() {
    console.log("create simulation");
    let simulation_id = await createSimulation();
    console.log(simulation_id);

    if (simulation_id.simulation_id) {
      props.setState({
        simulation_id: simulation_id.simulation_id,
        program_id: 1,
      });
      navigate(`${url}/machine`);
    }
  }
  return (
    <div className="flex flex-col flex-grow flex-nowrap">
      <div className="flex flex-row items-center justify-around flex-grow basis-2/5">
        <button
          className="w-1/5 px-3 text-3xl text-black rounded-lg h-2/4 bg-button-blue sm:text-base lg:text-xl xl:text-2xl 2xl:text-3xl 3xl:text-4xl"
          onClick={startSimulation}
        >
          Create simulation
        </button>
        <button
          className="w-1/5 px-3 text-3xl text-black rounded-lg h-2/4 bg-button-blue sm:text-base lg:text-xl xl:text-2xl 2xl:text-3xl 3xl:text-4xl"
          onClick={openModal}
        >
          Load simulation
        </button>
        <Modal
          isOpen={modalIsOpen}
          onRequestClose={closeModal}
          style={customStyles}
        >
          <div className="flex flex-col items-center justify-center flex-grow w-full h-fit flex-nowrap">
            {simulations.map((item: Simulation) => {
              return (
                <SimulationListElement
                  key={item.id}
                  simulation={item}
                  setState={props.setState}
                />
              );
            })}
            <button
              onClick={closeModal}
              className="w-1/2 px-4 py-2 border-2 border-black rounded-md shadow-md bg-slate-200 hover:bg-slate-500"
            >
              close
            </button>
          </div>
        </Modal>
      </div>
      <div className="w-full h-full bg-center bg-no-repeat bg-contain bg-lasercuter-img"></div>
    </div>
  );
}
export default LandingPage;

function SimulationListElement(props: any) {
  const navigate = useNavigate();
  let sim = props.simulation;
  async function handleLoadSimulation() {
    const response = await loadSimulation(sim.id);
    if (response.simulation_id) {
      props.setState({
        simulation_id: response.simulation_id,
        program_id: 0,
      });
      navigate(`/machine/state`);
    }
  }
  return (
    <button
      className="w-3/4 p-2 m-2 border-2 border-black rounded-lg h-fit"
      onClick={handleLoadSimulation}
    >
      <span>{sim.description} </span>
      <span>{sim.last_edited}</span>
    </button>
  );
}
