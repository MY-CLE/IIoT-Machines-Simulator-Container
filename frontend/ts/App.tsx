import React from "react";
import Header from "./header";

function App() {
  return (
    <div className="flex flex-col items-center justify-center w-full h-full flex-nowrap align-center">
      <Header />
      <div className="flex flex-row buttoncontainer w-fit h-fit">
        <button className="button">Simulation starten</button>
        <button className="button">Simulation laden</button>
      </div>
    </div>
  );
}
export default App;
