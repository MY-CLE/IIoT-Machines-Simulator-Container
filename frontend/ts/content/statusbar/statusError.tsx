import React from "react";
import IconError from "../../icons/iconError";

export function StatusError(props: { value: number }) {
  return (
    <>
      <div className="flex flex-col flex-wrap items-center justify-center flex-grow w-auto h-32 border border-l-0 border-black border-1">
        <div className="mb-3">
          <IconError />
        </div>
        <div>{props.value}</div>
      </div>
    </>
  );
}

export default StatusError;
