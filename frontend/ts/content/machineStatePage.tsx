import React from "react";
import StatusBar from "./statusbar/statusBar";

function MachineStatePage() {
  return (
    <div className="flex flex-col flex-grow flex-nowrap">
      <div className="flex flex-row items-center justify-start flex-grow h-32 bg-gray-300">
        <div className="p-3 text-2xl"><StatusBar/></div>
      </div>
      <div className="w-full h-full"></div>
    </div>
  );
}
export default MachineStatePage;
