import React from "react";

export function StatusDate() {
  return (
    <>
      <div className="flex-grow w-auto justify-center h-32 border flex items-center border-black border-1 border-l-0">
        <div className="px-5">yyyy-mm-dd</div>
        <div className="px-5">HH:MM:SS</div>
      </div>
    </>
  );
}

export default StatusDate;
