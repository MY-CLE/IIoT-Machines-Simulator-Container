import React, { useEffect } from "react";
import Header from "./header";
import ProgramStatePage from "./content/programStatePage";
import {
  createBrowserRouter,
  Outlet,
  Route,
  RouterProvider,
  Routes,
  useLocation,
  useNavigate,
} from "react-router-dom";
import LandingPage from "./content/landingpage";
import MachineStatePage from "./content/machineStatePage";
import ChooseProgramPage from "./content/chooseProgramPage";

import { useState } from "react";
import StatusBar from "./content/statusbar/statusBar";
import SelectionBar from "./content/machineOrProgramBar/selectionBar";
import { getMachine, getProgram } from "./api-service";
import { Machine, Program, StatusBarValues } from "./interfaces";
import { clear } from "console";

function App() {
  const location = useLocation();
  const navigation = useNavigate();
  const [state, setState] = useState({ simulation_id: 0, program_id: -1 });
  const [statuesBarValues, setStatuesBarValues] = useState({
    runtime: 0,
    utilization: 0,
    error: 0,
    warning: 0,
    safety_door: false,
    lock: false,
  });
  const [program, setProgram] = useState({
    description: "",
    id: -1,
    parameters: [],
  } as Program);
  const [machine, setMachine] = useState({
    parameters: [],
    error_state: { errors: [], warnings: [] },
  } as Machine);

  const [intervallId, setIntervallId] = useState<any>(0);
  useEffect(() => {
    clearInterval(intervallId);
    console.log(location.pathname);
    if (location.pathname === "/simulator/machine/") {
      getMachineStatePageData();
      const id = setInterval(() => getMachineStatePageData(), 5000);
      setIntervallId(id);
    } else if (location.pathname === "/simulator/program/current") {
      getCurrentPrograData();
      const id = setInterval(() => getCurrentPrograData(), 5000);
      setIntervallId(id);
    } else if (location.pathname === "/simulator/programs") {
      getProgramsPageData();
      const id = setInterval(() => getProgramsPageData(), 5000);
      setIntervallId(id);
    }
  }, [location]);

  async function getMachineStatePageData() {
    let machineState = await getMachine(
      state.simulation_id ? state.simulation_id : 0
    );
    let values: StatusBarValues = getStatusbarValues(machineState);
    setMachine(machineState);
    setStatuesBarValues(values);
  }

  async function getCurrentPrograData() {
    let machineState = await getMachine(
      state.simulation_id ? state.simulation_id : 0
    );
    //setTimeout(() => {}, 500);
    let program = await getProgram(state.simulation_id | 0);
    if (program.description === "") {
      navigation(`simulator/programs`);
    }
    if (program.parameters) {
      setProgram(program);
    }

    let values: StatusBarValues = getStatusbarValues(machineState);
    setStatuesBarValues(values);
  }

  async function getProgramsPageData() {
    let machineState = await getMachine(
      state.simulation_id ? state.simulation_id : 0
    );
    console.log(machineState);

    let values: StatusBarValues = getStatusbarValues(machineState);
    setStatuesBarValues(values);
  }

  function getStatusbarValues(machineState: Machine): StatusBarValues {
    let runtime = machineState.parameters[0].value;
    let errors = 0,
      warnings = 0,
      safetyDoorStatus = false;
    if (machineState.error_state) {
      errors = machineState.error_state.errors.length;
      warnings = machineState.error_state.warnings.length;
      for (const err of machineState.error_state.errors) {
        if (err.name[1] === "Safety door is open! Close it.") {
          safetyDoorStatus = true;
        }
      }
    }
    return {
      runtime: runtime,
      utilization: 5,
      warning: warnings,
      error: errors,
      safety_door: safetyDoorStatus,
      lock: false,
    };
  }

  return (
    <div className="flex flex-col flex-grow w-screen h-screen">
      <Routes>
        <Route
          path="/"
          element={
            <>
              <Header isLandingPage={true} />
              <LandingPage state={state} setState={setState} />
            </>
          }
        />
        <Route
          path="/simulator"
          element={
            <>
              <Header isLandingPage={false} />
              <div className="w-full text-2xl">
                <StatusBar
                  runtime={statuesBarValues.runtime}
                  utilization={statuesBarValues.utilization}
                  error={statuesBarValues.error}
                  warning={statuesBarValues.warning}
                  safety_door={statuesBarValues.safety_door}
                  lock={statuesBarValues.lock}
                />
              </div>
              <Outlet />
            </>
          }
        >
          <Route
            path="/simulator/machine"
            element={
              <>
                <SelectionBar whichPage="machine" />
                <MachineStatePage
                  state={state}
                  setState={setState}
                  machine={machine}
                />
              </>
            }
          />
          <Route
            path="/simulator/programs"
            element={
              <>
                <SelectionBar whichPage="program" />
                <ChooseProgramPage state={state} setState={setState} />
              </>
            }
          />
          <Route
            path="/simulator/program/current"
            element={
              <>
                <SelectionBar whichPage="program" />
                <ProgramStatePage
                  state={state}
                  setState={setState}
                  program={program}
                />
              </>
            }
          />
        </Route>
      </Routes>
    </div>
  );
}
export default App;
