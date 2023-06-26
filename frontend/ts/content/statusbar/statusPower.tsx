import React, {useState, useEffect} from "react";
import IconPower from "../../icons/iconPower";

export function StatusPower(props: {isProgramRunning: boolean, errors: number}) {

  const [color, setColor] = useState<string>("");
  
  useEffect (() => {
    if(props.errors != 0){
      setColor("#ff0000"); //red
    }
    else if (props.isProgramRunning && props.errors === 0) {
      setColor("#16A34A");	//green
    }
    else {
      setColor("#FACC15") //yellow
    }
  }, [props.isProgramRunning, props.errors])

  return (
    <>
      <div className="flex items-center justify-center w-1/10 h-32 border border-l-0 border-black border-1 text-xs sm:text-base lg:text-xl xl:text2xl">
        <div>
          <IconPower symbolColor={color}/>
        </div>
      </div>
    </>
  );
}

export default StatusPower;
