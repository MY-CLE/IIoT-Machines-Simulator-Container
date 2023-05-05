import React from "react";

export function StatusDate() {
  return (
    <>
      <div className="flex-grow w-auto justify-center h-32 border flex items-center border-black border-1 border-l-0">
        <div>yyyy-mm-dd</div>
        <div>HH:MM:SS</div>
      </div>
    </>
  );
}

export default StatusDate;
