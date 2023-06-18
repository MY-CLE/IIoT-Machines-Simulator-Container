import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function SelectionBar(props: { whichPage: any }) {
  const [machineColor, setMachineColor] = useState<string>("");
  const [programColor, setProgramColor] = useState<string>("");
  const navigation = useNavigate();

  useEffect(() => {
    if (props.whichPage === "program") {
      setMachineColor("bg-unselectedbar-green");
      setProgramColor("bg-selectedbar-green");
    } else {
      setMachineColor("bg-selectedbar-green");
      setProgramColor("bg-unselectedbar-green");
    }
  }, []);

  const handleMachineClick = () => {
    if (props.whichPage !== "machine") {
      navigation("/machine");
    }
  };

  const handleProgramClick = () => {
    if (props.whichPage !== "program") {
      navigation("/program/current");
    }
  };

  return (
    <div className="flex flex-row w-full h-10">
      <button
        onClick={handleMachineClick}
        className={`w-1/2 border border-black border-t-0 font-medium text-xs ${machineColor} sm:text-base lg:text-xl xl:text-2xl`}
      >
        Maschinenzustand
      </button>
      <button
        onClick={handleProgramClick}
        className={`w-1/2 border border-black border-t-0 border-l-0 font-medium ${programColor} text-xs sm:text-base lg:text-xl xl:text-2xl`}
      >
        Programmübersicht
      </button>
    </div>
  );
}

export default SelectionBar;
