import React from "react";
import IconUtil from "../../icons/iconUtil";

export function StatusUtil(prop: { value: number }) {
  return (
    <>
      <div className="flex flex-col flex-wrap items-center justify-center w-1/10 h-32 border border-l-0 border-black border-1">
        <div className="mb-3">
          <IconUtil />
        </div>
        <div>{prop.value}</div>
      </div>
    </>
  );
}

export default StatusUtil;
