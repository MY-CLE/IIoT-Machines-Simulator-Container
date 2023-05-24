import React, { useEffect, useState } from "react";
import StatusBar from "./statusbar/statusBar";
import SelectionBar from "./machineOrProgramBar/selectionBar";
import ParameterComponent from "./parameters/parameter";
import IconArrowBack from "../icons/iconBackArrow";
import { Program, StatusBarValues } from "../interfaces";
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
  const [statusBarValues, setStatusBarValues] = useState<StatusBarValues>({
    runtime: 0,
    utilization: 0,
    error: 0,
    warning: 0,
    safety_door: false,
    lock: false,
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
      <div className="flex flex-row items-center justify-start h-32 max-w-full bg-gray-300">
        <div className="w-full text-2xl">
          <StatusBar
            runtime={statusBarValues.runtime}
            utilization={statusBarValues.utilization}
            error={statusBarValues.error}
            warning={statusBarValues.warning}
            safety_door={statusBarValues.safety_door}
            lock={statusBarValues.lock}
          />
        </div>
      </div>
      <div>
        <SelectionBar program={() => {}} machine={() => {}} />
      </div>
      <div className="flex flex-col w-full h-full p-4 text-2xl bg-white border border-t-0 border-black border-1">
        <div className="flex flex-row items-center w-full h-auto mb-4 ">
          <button>
            <IconArrowBack width={50}></IconArrowBack>
          </button>
          <span className="text-4xl text-left">
            Programm Übersicht: {program.description}
          </span>
        </div>
        <div className="flex flex-row flex-wrap w-full h-full justify-evenly">
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