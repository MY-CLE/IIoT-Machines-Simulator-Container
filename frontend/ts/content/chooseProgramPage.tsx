import React from "react";
import StatusBar from "./statusbar/statusBar";
import SelectionBar from "./machineOrProgramBar/selectionBar";

const programs = [
  {
    description: "Kreis",
    id: "1",
  },
  {
    description: "Rechteck",
    id: "2",
  },
  {
    description: "Dreieck",
    id: "3",
  },
  {
    description: "",
    id: "3",
  },
  {
    description: "",
    id: "3",
  },
  {
    description: "",
    id: "3",
  },
];
function ChooseProgramPage() {
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
      <div className="flex flex-col justify-start h-full w-full text-2xl border border-black border-1 border-t-0 bg-program-choose-grey">
        <div className=" w-full h-auto text-center text-5xl p-4 text-white">
          Programauswahl
        </div>
        <div className="w-full flex flex-row h-full flex-wrap justify-between">
          {programs.map((item: any) => {
            return <ProgramCard key={item.id} name={item.description} />;
          })}
        </div>
      </div>
    </div>
  );
}
export default ChooseProgramPage;

function ProgramCard(props: any) {
  return (
    <button className=" bg-slate-100 rounded-2xl w-1/4 h-1/3 flex justify-center items-center  m-6 drop-shadow-sm">
      <span className=" text-4xl">{props.name}</span>
    </button>
  );
}
