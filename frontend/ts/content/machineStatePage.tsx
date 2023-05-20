import React from "react";
import StatusBar from "./statusbar/statusBar";
import SelectionBar from "./machineOrProgramBar/selectionBar";
import Parameter from "./parameters/parameter";
import SendError from "./parameters/sendError";
import IconQuitLock from "../icons/iconQuitLock";

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
      <div className="flex flex-col justify-start h-full w-full text-2xl border border-black border-1 border-t-0 bg-gray-200 p-2">
        <div className="w-full h-auto text-4xl text-left">Maschinenzustand</div>
        <div className="flex flex-row w-full h-full flex-grow">
          <div className="text-center w-2/5 flex flex-col flex-grow h-full justify-center items-center p-2">
            {paramterNames.map((item, index) => {
              return <Parameter key={index} name={item} />;
            })}
          </div>
          <div className=" w-2/5 flex flex-col justify-evenly text-center text-2xl p-2">
            <div className="w-full text-2xl flex flex-grow mb-5">
              <SendError
                name={"Error"}
                messages={errorMessages}
                color={"bg-red-500"}
              />
            </div>
            <div className="w-full text-2xl flex flex-grow mt-5">
              <SendError
                name={"Warning"}
                messages={warningMessages}
                color={"bg-orange-500"}
              />
            </div>
          </div>
          <div className="w-1/5 flex flex-grow p-2">
            <div className="ml-10 mr-10 h-full w-full flex justify-center items-center">
              <div className="bg-white w-full h-3/4 border border-black rounded-lg flex flex-col justify-between items-center align-middle">
                <div className="mt-5">
                  <IconQuitLock />
                </div>

                <div
                  className={`w-52 h-52 border border-black rounded-full mb-5 text-center pt-20 bg-red-500 font-medium`}
                >
                  <p>Quittieren!</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
export default MachineStatePage;
