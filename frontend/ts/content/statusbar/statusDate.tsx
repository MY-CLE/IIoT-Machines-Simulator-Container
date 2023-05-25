import React from "react";

export function StatusDate(props: { value: Date }) {
  return (
    <>
      <div className="flex items-center justify-center flex-grow w-auto h-32 border border-l-0 border-black border-1">
        <div className="px-5">{props.value.toISOString()}</div>
      </div>
    </>
  );
}

export default StatusDate;
