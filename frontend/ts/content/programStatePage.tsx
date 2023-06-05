import React, { useEffect, useState } from "react";
import StatusBar from "./statusbar/statusBar";
import SelectionBar from "./machineOrProgramBar/selectionBar";
import ParameterComponent from "./parameters/parameter";
import IconArrowBack from "../icons/iconBackArrow";
import { Machine, Program, StatusBarValues } from "../interfaces";
import { getMachine, getProgram } from "../api-service";
import { useNavigate } from "react-router-dom";

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
  const navigation = useNavigate();
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
      let machineState = await getMachine(
        props.state.simulation_id ? props.state.simulation_id : 0
      );
      console.log(machineState);

      let values: StatusBarValues = getStatusbarValues(machineState);
      setStatusBarValues(values);
    })();

    const id = setInterval(async () => {
      let machineState = await getMachine(
        props.state.simulation_id ? props.state.simulation_id : 0
      );
      console.log(machineState);

      let values: StatusBarValues = getStatusbarValues(machineState);
      setStatusBarValues(values);
    }, 5000);
    return () => clearInterval(id);
  }, []);

  function getStatusbarValues(machineState: Machine): StatusBarValues {
    let runtime = machineState.parameters[0].value;
    let errors = 0,
      warnings = 0;
    if (machineState.error_state) {
      errors = machineState.error_state.errors.length;
      warnings = machineState.error_state.warnings.length;
    }
    return {
      runtime: runtime,
      utilization: 5,
      warning: warnings,
      error: errors,
      safety_door: false,
      lock: false,
    };
  }
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
        <SelectionBar
          program={() => {}}
          machine={() => {
            navigation("/machine");
          }}
        />
      </div>
      <div className="flex flex-col w-full h-full p-4 text-2xl bg-white border border-t-0 border-black border-1">
        <div className="flex flex-row items-center w-full h-auto mb-4 ">
          <button
            onClick={() => {
              navigation("/programs");
            }}
          >
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
                <div key={item.id} className="w-1/3 m-2">
                  <ParameterComponent
                    simulation_id={props.state.simulation_id}
                    key={item.id}
                    name={item.description}
                    value={item.value}
                    id={item.id}
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
