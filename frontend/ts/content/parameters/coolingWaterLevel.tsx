import React from "react";
import IconPen from "../../icons/iconPen";

function CoolingWaterLevel(){
    return(
        <div className="flex flex-row border border-black w-full h-16 justify-start items-center bg-white rounded-xl">
            <div className="justify-center items-center flex flex-grow w-1/4 flex-wrap mr-20 font-medium">
                Kühlwasserstand
            </div>
            <div className="justify-center items-center flex flex-grow flex-wrap bg-gray-400 h-3/4 w-1/6 rounded-lg border border-black mr-2 drop-shadow">
                
            </div>
            <button className="justify-center items-center flex flex-grow flex-wrap bg-white mr-5 w-0 h-3/4 border border-black rounded-lg drop-shadow">
                <IconPen/>
            </button>
        </div>
    );
}

export default CoolingWaterLevel;
