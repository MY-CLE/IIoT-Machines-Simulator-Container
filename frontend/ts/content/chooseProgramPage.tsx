import React, { useEffect, useState } from "react";
import StatusBar from "./statusbar/statusBar";
import SelectionBar from "./machineOrProgramBar/selectionBar";
import { useLocation, useNavigate } from "react-router-dom";
import { getMachine, getPrograms } from "../api-service";
import { Machine, Program, StatusBarValues } from "../interfaces";

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
  const [statusBarValues, setStatusBarValues] = useState({
    runtime: 0,
    utilization: 0,
    error: 0,
    warning: 0,
    safety_door: false,
    lock: false,
  });

  useEffect(() => {
    (async () => {
      let progs = await getPrograms(props.state.simulation_id | 0).then(
        (programs) => {
          return programs.programs;
        }
      );
      setPrograms(progs);
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
    }, 2000);
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

  function navigateToMachineStatePage() {
    navigation("/machine");
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
        <SelectionBar program={() => {}} machine={navigateToMachineStatePage} />
      </div>
      <div className="flex flex-col justify-start w-full h-full text-2xl border border-t-0 border-black border-1 bg-program-choose-grey">
        <div className="w-full h-auto p-4 text-5xl text-center text-white ">
          Programauswahl
        </div>
        <div className="flex flex-row flex-wrap justify-between w-full h-full">
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
      className="flex items-center justify-center w-1/4 m-6 bg-slate-100 rounded-2xl h-1/3 drop-shadow-sm"
      onClick={() => props.func(props.key)}
    >
      <span className="text-4xl ">{props.name}</span>
    </button>
  );
}
