import React from "react";

function SelectionBar(){
    return(
        <div className="flex flex-row w-full h-10">
            <button className="w-1/2 border border-black border-t-0 font-medium bg-selectedbar-green">
                Maschinenzustand
            </button>
            <button className="w-1/2 border border-black border-t-0 border-l-0 font-medium bg-unselectedbar-green">
                Programmübersicht
            </button>
        </div>
    );
}

export default SelectionBar;