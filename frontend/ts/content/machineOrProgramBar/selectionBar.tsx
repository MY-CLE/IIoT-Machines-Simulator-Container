import React from "react";

function SelectionBar(props: { program: any; machine: any }) {
  return (
    <div className="flex flex-row w-full h-10">
      <button
        onClick={props.machine ? props.machine : () => {}}
        className="w-1/2 border border-black border-t-0 font-medium bg-selectedbar-green text-xs sm:text-base lg:text-xl xl:text2xl"
      >
        Maschinenzustand
      </button>
      <button
        onClick={props.program ? props.program : () => {}}
        className="w-1/2 border border-black border-t-0 border-l-0 font-medium bg-unselectedbar-green text-xs sm:text-base lg:text-xl xl:text2xl"
      >
        Programmübersicht
      </button>
    </div>
  );
}

export default SelectionBar;
