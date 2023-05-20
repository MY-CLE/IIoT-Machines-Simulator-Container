import React from "react";
import LandingPage from "./content/landingpage";
import Header from "./header";
import MachineStatePage from "./content/machineStatePage";

function App() {
  return (
    <div className="flex flex-col flex-grow w-screen h-screen">
      <Header />
     {/*<LandingPage/>*/}
     <MachineStatePage/>
      
    </div>
  );
}
export default App;

