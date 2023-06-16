import React from "react";
import IconDoor from "../../icons/iconDoor";

export function StatusSafetyDoor(props: { value: boolean }) {
  return (
    <>
      <div className="flex flex-col flex-wrap items-center justify-center w-1/10 h-32 border border-l-0 border-black border-1">
        <div className=" w-full h-full">
          <IconDoor />
        </div>
        <div>{props.value}</div>
      </div>
    </>
  );
}

export default StatusSafetyDoor;
