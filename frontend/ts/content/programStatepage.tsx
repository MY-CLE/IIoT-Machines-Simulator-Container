import React from "react";
import StatusBar from "./statusbar/statusBar";
import SelectionBar from "./machineOrProgramBar/selectionBar";
import Parameter from "./parameters/paramter";
import IconArrowBack from "../icons/iconBackArrow";

function ProgramStatePage(props: any) {
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
      <div className="flex flex-col h-full w-full text-2xl border border-black border-1 border-t-0 bg-white p-4">
        <div className=" flex flex-row w-full items-center h-auto mb-4">
          <button>
            <IconArrowBack width={50}></IconArrowBack>
          </button>
          <span className="text-left text-4xl">
            Programm Übersicht: {props.program.description}
          </span>
        </div>
        <div className="w-full flex flex-row h-full flex-wrap justify-evenly">
          {props.program.parameters.map(
            (item: { id: number; description: string; value: number }) => {
              return (
                <Parameter
                  key={item.id}
                  name={item.description}
                  value={item.value}
                />
              );
            }
          )}
        </div>
      </div>
    </div>
  );
}
export default ProgramStatePage;
