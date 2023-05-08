import React from "react";
import IconError from "../../icons/iconError";

export function StatusError() {
  return (
    <>
      <div className="flex-grow w-auto justify-center h-32 border flex flex-col flex-wrap items-center border-black border-1 border-l-0">
        <div className="mb-3"><IconError/></div>
        <div>value</div>
      </div>
    </>
  );
}

export default StatusError;
