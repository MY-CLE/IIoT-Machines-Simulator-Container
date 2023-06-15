import React from "react";
import Header from "./header";
import ProgramStatePage from "./content/programStatePage";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import LandingPage from "./content/landingpage";
import MachineStatePage from "./content/machineStatePage";
import ChooseProgramPage from "./content/chooseProgramPage";

import { useState } from "react";

function App() {
  const [state, setState] = useState({ simulation_id: 0, program_id: -1 });
  const router = createBrowserRouter([
    {
      path: "/",
      element: (
        <>
          <Header isLandingPage={true} />
          <LandingPage state={state} setState={setState} />
        </>
      ),
    },
    {
      path: "/machine",
      element: (
        <>
          <Header isLandingPage={false} />
          <MachineStatePage state={state} setState={setState} />
        </>
      ),
    },
    {
      path: "/programs",
      element: (
        <>
          <Header isLandingPage={false} />
          <ChooseProgramPage state={state} setState={setState} />
        </>
      ),
    },
    {
      path: "/program/current",
      element: (
        <>
          <Header isLandingPage={false} />
          <ProgramStatePage state={state} setState={setState} />
        </>
      ),
    },
  ]);
  return (
    <div className="flex flex-col flex-grow w-screen h-screen">
      <RouterProvider router={router}></RouterProvider>
    </div>
  );
}
export default App;
