import React from "react";
import { useState } from "react";
import Modal, { Styles } from "react-modal";
import {
  createSimulation,
  getSimultions,
  postSimulation,
} from "../api-service";
import { Simulation } from "../interfaces";
import { useNavigate } from "react-router-dom";

Modal.setAppElement("#root");
const customStyles: Styles = {
  content: {
    position: "absolute",
    width: "50%",
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
  function afterOpenModal() {}
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
      navigate(`/machine`);
    }
  }
  return (
    <div className="flex flex-col flex-grow flex-nowrap">
      <div className="flex flex-row items-center justify-around flex-grow basis-2/5">
        <button
          className="w-1/5 px-3 text-3xl text-black rounded-lg h-2/4 bg-button-blue"
          onClick={startSimulation}
        >
          Simulation erzeugen
        </button>
        <button
          className="w-1/5 px-3 text-3xl text-black rounded-lg h-2/4 bg-button-blue"
          onClick={openModal}
        >
          Simulation laden
        </button>
        <Modal
          isOpen={modalIsOpen}
          onAfterOpen={afterOpenModal}
          onRequestClose={closeModal}
          style={customStyles}
        >
          <div className="flex flex-col flex-grow flex-nowrap w-full h-full">
            {simulations.map((item: Simulation) => {
              return <SimulationListElement key={item.id} simulation={item} />;
            })}
            <button onClick={closeModal}>close</button>
          </div>
        </Modal>
      </div>
      <div className="w-full h-full bg-center bg-no-repeat bg-contain bg-lasercuter-img"></div>
    </div>
  );
}
export default LandingPage;

function SimulationListElement(params: any) {
  let sim = params.simulation;
  return (
    <div className="w-full h-fit border rounded-lg m-2 p-2">
      <span>{sim.description} </span>
      <span>{sim.last_edited}</span>
    </div>
  );
}
