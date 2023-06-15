import React from "react";
import IconDoor from "../../icons/iconDoor";
import IconLock from "../../icons/iconLock";

export function StatusLock(props: { value: boolean }) {
  return (
    <>
      <div className="flex items-center justify-center w-1/10 h-32 border border-l-0 border-black border-1">
        <div>{props.value ? <IconDoor /> : <IconLock />}</div>
      </div>
    </>
  );
}

export default StatusLock;
