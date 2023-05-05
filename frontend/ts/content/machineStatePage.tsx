import React from "react";
import StatusBar from "./statusbar/statusBar";

function MachineStatePage() {
  return (
    <div className="flex flex-col flex-grow flex-nowrap">
      <div className="max-w-full flex flex-row items-center justify-start h-32 bg-gray-300">
        <div className="w-full text-2xl"><StatusBar/></div>
      </div>
      <div className="w-full h-full"></div>
    </div>
  );
}
export default MachineStatePage;
