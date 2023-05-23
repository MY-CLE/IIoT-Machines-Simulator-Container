import React, { useEffect, useState } from "react";
import StatusBar from "./statusbar/statusBar";
import SelectionBar from "./machineOrProgramBar/selectionBar";
import { useLocation, useNavigate } from "react-router-dom";
import { getPrograms } from "../api-service";
import { Program } from "../interfaces";

const programsdefault = [
  {
    description: "Kreis",
    id: "1",
  },
  {
    description: "Rechteck",
    id: "2",
  },
  {
    description: "Dreieck",
    id: "3",
  },
  {
    description: "",
    id: "3",
  },
  {
    description: "",
    id: "3",
  },
  {
    description: "",
    id: "3",
  },
];
function ChooseProgramPage(props: {
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
  const navigation = useNavigate();
  const [programs, setPrograms] = useState<Array<Program>>([
    { description: "", parameters: null, id: null },
  ]);

  useEffect(() => {
    (async () => {
      let progs = await getPrograms(props.state.simulation_id | 0).then(
        (programs) => {
          return programs.programs;
        }
      );
      setPrograms(progs);
    })();
  }, []);

  function navigateToMachineStatePage() {
    navigation("/machineStatePage");
  }

  function navigateToProgramStatePage(id: number) {
    props.setState({
      program_id: id,
      simulation_id: props.state.simulation_id,
    });
    navigation("/program/current");
  }

  return (
    <div className="flex flex-col flex-grow flex-nowrap">
      <div className="max-w-full flex flex-row items-center justify-start h-32 bg-gray-300">
        <div className="w-full text-2xl">
          <StatusBar />
        </div>
      </div>
      <div>
        <SelectionBar program={() => {}} machine={navigateToMachineStatePage} />
      </div>
      <div className="flex flex-col justify-start h-full w-full text-2xl border border-black border-1 border-t-0 bg-program-choose-grey">
        <div className=" w-full h-auto text-center text-5xl p-4 text-white">
          Programauswahl
        </div>
        <div className="w-full flex flex-row h-full flex-wrap justify-between">
          {programs.map((item: any) => {
            return (
              <ProgramCard
                key={item.id}
                name={item.description}
                id={item.id}
                func={navigateToProgramStatePage}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
}
export default ChooseProgramPage;

function ProgramCard(props: any) {
  return (
    <button
      className=" bg-slate-100 rounded-2xl w-1/4 h-1/3 flex justify-center items-center  m-6 drop-shadow-sm"
      onClick={() => props.func(props.key)}
    >
      <span className=" text-4xl">{props.name}</span>
    </button>
  );
}
