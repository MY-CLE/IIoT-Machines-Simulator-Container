import React from "react";
import IconLock from "../../icons/iconLock";

export function StatusLock() {
  return (
    <>
      <div className="flex-grow w-auto justify-center h-32 border flex items-center border-black border-1 border-l-0">
        <div><IconLock/></div>
      </div>
    </>
  );
}

export default StatusLock;
