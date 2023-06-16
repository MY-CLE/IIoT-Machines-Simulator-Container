import React from "react";

export function StatusTime(props: { value: number }) {
  return (
    <>
      <div className="flex flex-col flex-wrap items-center justify-center w-1/10 h-32 border border-l-0 border-black border-1">
        <div className="mt-3 mb-4 text-xs sm:text-base lg:text-xl xl:text2xl">Laufzeit</div>
        <div className="text-xs sm:text-base lg:text-xl xl:text2xl">{props.value}</div>
      </div>
    </>
  );
}

export default StatusTime;
