import React from "react";

function LandingPage() {
  return (
    <div className="flex flex-col flex-grow flex-nowrap">
      <div className="flex flex-row items-center justify-around flex-grow basis-2/5">
        <button className="w-1/5 px-3 text-3xl text-black rounded-lg h-2/4 bg-button-blue">
          Simulation starten
        </button>
        <button className="w-1/5 px-3 text-3xl text-black rounded-lg h-2/4 bg-button-blue">
          Simulation laden
        </button>
      </div>
      <div className="w-full h-full bg-center bg-no-repeat bg-contain bg-lasercuter-img"></div>
    </div>
  );
}
export default LandingPage;
