import React from "react";

export function StatusTime(props: { value: number }) {
  return (
    <>
      <div className="flex flex-col flex-wrap items-center justify-center w-1/10 h-32 border border-l-0 border-black border-1">
        <div className="mt-3 mb-4">Laufzeit</div>
        <div>{props.value}</div>
      </div>
    </>
  );
}

export default StatusTime;
