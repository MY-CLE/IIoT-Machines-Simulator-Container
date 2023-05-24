import React from "react";
import IconDoor from "../../icons/iconDoor";

export function StatusSafetyDoor(props: { value: boolean }) {
  return (
    <>
      <div className="flex flex-col flex-wrap items-center justify-center flex-grow w-auto h-32 border border-l-0 border-black border-1">
        <div className="mb-3">
          <IconDoor />
        </div>
        <div>{props.value}</div>
      </div>
    </>
  );
}

export default StatusSafetyDoor;
