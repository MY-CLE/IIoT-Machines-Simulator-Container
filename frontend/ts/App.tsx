import React, { useEffect } from "react";
import Header from "./header";
import ProgramStatePage from "./content/programStatePage";
import { Outlet, Route, Routes, useLocation } from "react-router-dom";
import LandingPage from "./content/landingpage";
import MachineStatePage from "./content/machineStatePage";
import ChooseProgramPage from "./content/chooseProgramPage";

import { useState } from "react";
import StatusBar from "./content/statusbar/statusBar";
import SelectionBar from "./content/machineOrProgramBar/selectionBar";
import { getMachine, getProgram } from "./api-service";
import { Machine, Program, StatusBarValues } from "./interfaces";

function App() {
  const location = useLocation();

  const [selectionBarValue, setSelectionBarValue] = useState<string>("machine");
  const [state, setState] = useState({ simulation_id: 0, program_id: -1 });
  const [statuesBarValues, setStatuesBarValues] = useState({
    runtime: 0,
    utilization: 0,
    error: 0,
    warning: 0,
    safety_door: false,
    coolantLevel: 0,
    isProgramRunning: false,
  });
  const [program, setProgram] = useState({
    description: "",
    id: -1,
    parameters: [],
  } as Program);
  const [machine, setMachine] = useState({
    parameters: [],
    errorState: { errors: [], warnings: [] },
    isProgramRunning: false,
  } as Machine);

  const [intervallId, setIntervallId] = useState<any>(0);

  useEffect(() => {
    clearInterval(intervallId);
    console.log(location.pathname);
    if (location.pathname === "/simulator/machine") {
      setSelectionBarValue("machine");
      getCurrentProgramData();
      getMachineStatePageData();
      const id = setInterval(() => getMachineStatePageData(), 5000);
      setIntervallId(id);
    } else if (location.pathname === "/simulator/program/current") {
      setSelectionBarValue("program");
      getCurrentProgramData();
      const id = setInterval(() => getCurrentProgramData(), 5000);
      setIntervallId(id);
    } else if (location.pathname === "/simulator/programs") {
      setSelectionBarValue("program");
      getProgramsPageData();
      const id = setInterval(() => getProgramsPageData(), 5000);
      setIntervallId(id);
    }
  }, [location]);

  async function getMachineStatePageData() {
    let machineStateRes = await getMachine();
    if (!machineStateRes) return;
    let machineState = (await machineStateRes.json()) as Machine;
    let values: StatusBarValues = getStatusbarValues(machineState);
    setMachine(machineState);
    setStatuesBarValues(values);
  }

  async function getCurrentProgramData() {
    let machineStateRes = await getMachine();
    let programRes = await getProgram();

    if (!machineStateRes) return;
    let machineState = (await machineStateRes.json()) as Machine;

    if (!programRes) return;
    let program = (await programRes.json()) as Program;

    if (program.parameters) {
      console.log(program.description)
      setProgram(program);
    }

    let values: StatusBarValues = getStatusbarValues(machineState);
    setStatuesBarValues(values);
  }

  async function getProgramsPageData() {
    let machineStateRes = await getMachine();
    if (!machineStateRes) return;
    let machineState = (await machineStateRes.json()) as Machine;
    let values: StatusBarValues = getStatusbarValues(machineState);
    setStatuesBarValues(values);
  }

  function getStatusbarValues(machineState: Machine): StatusBarValues {
    let runtime = machineState.parameters[0].value;
    let coolantLevel = machineState.parameters[2].value;
    let laserModuleCapacity = machineState.parameters[4].value;
    let isProgramRunning = machineState.isProgramRunning;
    let errors = 0,
      warnings = 0,
      safetyDoorStatus = false;
    if (machineState.errorState) {
      errors = machineState.errorState.errors.length;
      warnings = machineState.errorState.warnings.length;
      for (const err of machineState.errorState.errors) {
        if (err.name[1] === "Safety door is open! Close it.") {
          safetyDoorStatus = true;
        }
      }
    }
    return {
      runtime: runtime,
      utilization: laserModuleCapacity,
      warning: warnings,
      error: errors,
      safety_door: safetyDoorStatus,
      coolantLevel: coolantLevel,
      isProgramRunning: isProgramRunning,
    };
  }

  return (
    <div className="flex flex-col w-screen h-screen">
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
                  coolantLevel={statuesBarValues.coolantLevel}
                  isProgramRunning={statuesBarValues.isProgramRunning}
                />
              </div>
              {selectionBarValue === "program" && (
                <SelectionBar
                  whichPage={"program"}
                  isProgramSelected={program.description !== ""}
                />
              )}
              {selectionBarValue === "machine" && (
                <SelectionBar
                  whichPage={"machine"}
                  isProgramSelected={program.description !== ""}
                />
              )}

              <Outlet />
            </>
          }
        >
          <Route
            path="/simulator/machine"
            element={
              <>
                <MachineStatePage
                  state={state}
                  setState={setState}
                  machine={machine}
                  getProgramState={getCurrentProgramData}
                />
              </>
            }
          />
          <Route
            path="/simulator/programs"
            element={
              <>
                <ChooseProgramPage state={state} setState={setState} />
              </>
            }
          />
          <Route
            path="/simulator/program/current"
            element={
              <>
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
