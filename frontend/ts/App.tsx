import React from "react";
import LandingPage from "./content/landingpage";
import Header from "./header";
import MachineStatePage from "./content/machineStatePage";
import ChooseProgramPage from "./content/chooseProgramPage";

function App() {
  return (
    <div className="flex flex-col flex-grow w-screen h-screen">
      <Header />
      {/*<LandingPage/>*/}
      <ChooseProgramPage />
    </div>
  );
}
export default App;
