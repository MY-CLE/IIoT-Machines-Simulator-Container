import React from "react";
import IconUtil from "../../icons/iconUtil";

export function StatusUtil() {
  return (
    <>
      <div className="flex-grow w-auto justify-center h-32 border flex flex-col items-center border-black border-1 border-l-0 flex-wrap">
        <div className="mb-3"><IconUtil/></div>
        <div>value</div>
      </div>
    </>
  );
}

export default StatusUtil;
