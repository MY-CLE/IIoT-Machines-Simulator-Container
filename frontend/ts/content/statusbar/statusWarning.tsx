import React from "react";
import IconWarning from "../../icons/iconWarning";

export function StatusWarning(props: { value: number }) {
  return (
    <>
      <div className="flex flex-col flex-wrap items-center justify-center flex-grow w-auto h-32 border border-l-0 border-black border-1">
        <div className="mb-3">
          <IconWarning />
        </div>
        <div>{props.value}</div>
      </div>
    </>
  );
}

export default StatusWarning;
