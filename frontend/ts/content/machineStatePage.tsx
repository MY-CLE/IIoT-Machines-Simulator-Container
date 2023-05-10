import React from "react";
import StatusBar from "./statusbar/statusBar";
import SelectionBar from "./machineOrProgramBar/selectionBar";
import Parameter from "./parameters/paramter";

const paramterNames = [
  "Laufzeit",
  "Kühlwasserstand",
  "Stromverbrauch",
  "Leistung Lasermodul",
  "Stillstandzeit",
];

function MachineStatePage() {
  return (
    <div className="flex flex-col flex-grow flex-nowrap">
      <div className="max-w-full flex flex-row items-center justify-start h-32 bg-gray-300">
        <div className="w-full text-2xl">
          <StatusBar />
        </div>
      </div>
      <div>
        <SelectionBar />
      </div>
      <div className="flex flex-row justify-start h-full w-full text-2xl border border-black border-1 border-t-0 bg-gray-200">
        <div className="text-center w-1/3 flex flex-col h-full justify-center">
          <div className="text-lg h-3/4 ml-10 justify-center flex flex-col space-y-10">
            {paramterNames.map((item, index) => {
              return <Parameter key={index} name={item} />;
            })}
          </div>
        </div>
        <div className="w-1/3 h-full flex flex-col justify-top items-center align-middle space-y-10">
          <div className="h-auto mt-10">Maschinenzustand</div>
        </div>
      </div>
    </div>
  );
}
export default MachineStatePage;
