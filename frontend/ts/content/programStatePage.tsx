import React, { useEffect, useState } from "react";
import StatusBar from "./statusbar/statusBar";
import SelectionBar from "./machineOrProgramBar/selectionBar";
import ParameterComponent from "./parameters/parameter";
import IconArrowBack from "../icons/iconBackArrow";
import { Program } from "../interfaces";
import { getProgram } from "../api-service";

function ProgramStatePage(props: {
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
  const [program, setProgram] = useState<Program>({
    description: "",
    parameters: [{ id: 0, description: "", value: 0 }],
    id: null,
  });
  useEffect(() => {
    (async () => {
      let program = await getProgram(props.state.simulation_id | 0);
      if (program.parameters) {
        setProgram(program);
      }
    })();
  }, []);

  return (
    <div className="flex flex-col flex-grow flex-nowrap">
      <div className="max-w-full flex flex-row items-center justify-start h-32 bg-gray-300">
        <div className="w-full text-2xl">
          <StatusBar />
        </div>
      </div>
      <div>
        <SelectionBar program={() => {}} machine={() => {}} />
      </div>
      <div className="flex flex-col h-full w-full text-2xl border border-black border-1 border-t-0 bg-white p-4">
        <div className=" flex flex-row w-full items-center h-auto mb-4">
          <button>
            <IconArrowBack width={50}></IconArrowBack>
          </button>
          <span className="text-left text-4xl">
            Programm Übersicht: {program.description}
          </span>
        </div>
        <div className="w-full flex flex-row h-full flex-wrap justify-evenly">
          {program.parameters!.map(
            (item: { id: number; description: string; value: number }) => {
              return (
                <div className="w-1/3 m-2">
                  <ParameterComponent
                    key={item.id}
                    name={item.description}
                    value={item.value}
                  />
                </div>
              );
            }
          )}
        </div>
      </div>
    </div>
  );
}
export default ProgramStatePage;
