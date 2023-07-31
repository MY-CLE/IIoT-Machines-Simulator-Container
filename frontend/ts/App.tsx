import React, { useEffect, useRef } from "react";
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
import { enqueueSnackbar } from "notistack";

function App() {
  const location = useLocation();
  const hasUserBeenNotifiedForAmount = useRef<boolean>(false);
  const [refresh, setRefresh] = useState<number>(5000);
  const [selectionBarValue, setSelectionBarValue] = useState<string>("machine");
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
    console.log("useEffect", intervallId);

    clearInterval(intervallId);

    console.log(location.pathname);
    console.log("refresh: " + refresh);
    if (location.pathname === "/simulator/machine") {
      setSelectionBarValue("machine");
      getCurrentProgramData();
      getMachineStatePageData();
      console.log("refresh2: " + refresh);
      const id = setInterval(() => getMachineStatePageData(), refresh);
      setIntervallId(id);
    } else if (location.pathname === "/simulator/program/current") {
      setSelectionBarValue("program");
      getCurrentProgramData();
      console.log("refresh2: " + refresh);
      const id = setInterval(() => getCurrentProgramData(), refresh);
      setIntervallId(id);
    } else if (location.pathname === "/simulator/programs") {
      setSelectionBarValue("program");
      getProgramsPageData();
      console.log("refresh2: " + refresh);
      const id = setInterval(() => getProgramsPageData(), refresh);
      setIntervallId(id);
    }
    console.log("useEffect2", intervallId);
  }, [location, refresh]);

  async function getMachineStatePageData() {
    console.log("getMachineStatePageData", refresh);
    let machine = await getMachine();
    if (!machine) return;
    setMachine(machine);
    let values: StatusBarValues = getStatusbarValues(machine);
    setStatuesBarValues(values);
  }

  async function getCurrentProgramData() {
    console.log("getCurrentProgramData", refresh);
    let machine = await getMachine();
    let program = await getProgram();
    let currentAmount = undefined;
    let targetAmount = undefined;

    if (!machine) return;
    if (!program) return;
    setMachine(machine);
    if (program.parameters) {
      console.log(program.description);
      setProgram(program);

      for (let parameter of program.parameters) {
        if (parameter.description === "Current Amount") {
          currentAmount = parameter.value;
        }
        if (parameter.description === "Target Amount") {
          targetAmount = parameter.value;
        }
      }
    }

    if (currentAmount === undefined || targetAmount === undefined) return;
    if (
      currentAmount >= targetAmount &&
      !hasUserBeenNotifiedForAmount.current
    ) {
      enqueueSnackbar("Target amount reached!", { variant: "info" });
      hasUserBeenNotifiedForAmount.current = true;
    } else if (currentAmount < targetAmount) {
      hasUserBeenNotifiedForAmount.current = false;
    }

    let values: StatusBarValues = getStatusbarValues(machine);
    setStatuesBarValues(values);
  }

  async function getProgramsPageData() {
    console.log("getProgramsPageData", refresh);
    let machine = await getMachine();
    if (!machine) return;
    let values: StatusBarValues = getStatusbarValues(machine);
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
              <Header
                isLandingPage={true}
                setRefresh={setRefresh}
                refresh={refresh}
              />
              <LandingPage />
            </>
          }
        />
        <Route
          path="/simulator"
          element={
            <>
              <Header
                isLandingPage={false}
                setRefresh={setRefresh}
                refresh={refresh}
              />
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
                <ChooseProgramPage />
              </>
            }
          />
          <Route
            path="/simulator/program/current"
            element={
              <>
                <ProgramStatePage program={program} />
              </>
            }
          />
        </Route>
      </Routes>
    </div>
  );
}
export default App;
