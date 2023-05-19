import React from "react";
import StatusBar from "./statusbar/statusBar";
import SelectionBar from "./machineOrProgramBar/selectionBar";
import Parameter from "./parameters/parameter";
import SendError from "./parameters/sendError";

const paramterNames = [
  "Laufzeit",
  "Kühlwasserstand",
  "Stromverbrauch",
  "Leistung Lasermodul",
  "Stillstandzeit",
];

const warningMessages = [
  "Kühlwasser zu sauer",
  "Hohe Laufzeit",
  "Kühlwasserstand niedrig",
];

const errorMessages = [
  "Sicherheitstüre offen",
  "Leistung Lasermodul unzureichend",
  "Programmfehler",
]

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
      <div className="flex flex-col justify-start h-full w-full text-2xl border border-black border-1 border-t-0 bg-gray-200">
        <div className="w-full h-auto text-4xl text-left">Maschinenzustand</div>
        <div className="flex flex-row w-full flex-grow">
        <div className="text-center w-1/3 flex flex-col h-full justify-center">
          <div className="text-lg flex-grow ml-10 mr-10 justify-center flex flex-col space-y-10">
            {paramterNames.map((item, index) => {
              return <Parameter key={index} name={item} />;
            })}
          </div>
        </div>
        <div className=" w-1/3 flex-grow flex flex-col justify-center items-center space-y-7 text-center text-2xl">
          <div className="w-full text-2xl"><SendError name={"Error"} messages={errorMessages} color={"bg-red-500"}/></div>
          <div className="w-full text-2xl"><SendError name={"Warning"} messages={warningMessages} color={"bg-orange-500"}/></div>
        </div>
        <div className="w-1/3 flex flex-grow"></div>
        </div>
        
      </div>
    </div>
  );
}
export default MachineStatePage;
