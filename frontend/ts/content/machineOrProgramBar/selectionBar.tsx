import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
const url = "/simulator";

function SelectionBar(props: { whichPage: any; isProgramSelected: boolean }) {
  const [machineColor, setMachineColor] = useState<string>("");
  const [programColor, setProgramColor] = useState<string>("");
  const navigation = useNavigate();

  useEffect(() => {
    console.log(props.isProgramSelected);
    if (props.whichPage === "program") {
      setMachineColor("bg-unselectedbar-green");
      setProgramColor("bg-selectedbar-green");
    } else {
      setMachineColor("bg-selectedbar-green");
      setProgramColor("bg-unselectedbar-green");
    }
  }, []);

  const handleMachineClick = () => {
    navigation(`${url}/machine`);
  };

  const handleProgramClick = () => {
    if (props.isProgramSelected) {
      navigation(`${url}/program/current`);
    } else {
      navigation(`${url}/programs`);
    }
  };

  return (
    <div className="flex flex-row w-full h-10 flex-shrink-0">
      <button
        onClick={handleMachineClick}
        className={`w-1/2 border border-black border-t-0 font-medium text-xs ${machineColor} sm:text-base lg:text-xl xl:text-2xl`}
      >
        Machine State
      </button>
      <button
        onClick={handleProgramClick}
        className={`w-1/2 border border-black border-t-0 border-l-0 font-medium ${programColor} text-xs sm:text-base lg:text-xl xl:text-2xl`}
      >
        Program Overview
      </button>
    </div>
  );
}

export default SelectionBar;
