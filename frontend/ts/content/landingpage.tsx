import React from "react";
import { useState } from "react";
import Modal from "react-modal";
import { getSimultions, postSimulation } from "../api-service";
import { Simulation } from "../interfaces";
import { useNavigate } from "react-router-dom";

Modal.setAppElement("#root");

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

  async function createSimulation() {
    console.log("create simulation");
    let simulation_id = await postSimulation();
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
          onClick={createSimulation}
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
        >
          {simulations!.map((item: Simulation) => {
            return <SimulationListElement key={item.id} simulation={item} />;
          })}
          <button onClick={closeModal}>close</button>
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
    <div>
      <span>{sim.description}</span>
    </div>
  );
}
