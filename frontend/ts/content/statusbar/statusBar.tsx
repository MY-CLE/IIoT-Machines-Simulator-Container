import React from "react";
import StatusStatus from "./statusStatus";
import StatusPower from "./statusPower";
import StatusTime from "./statusTime";
import StatusUtil from "./statusUtilization";
import StatusError from "./statusError";
import StatusWarning from "./statusWarning";
import StatusSafetyDoor from "./statusSafetyDoor";
import StatusDate from "./statusDate";
import StatusLock from "./statusLock";

export function StatusBar() {
  return (
    <header>
      <div className="flex flex-row items-center justify-start flex-nowrap w-full">
      <StatusStatus />
      <StatusPower />
      <StatusTime />
      <StatusUtil />
      <StatusWarning />
      <StatusError />
      <StatusSafetyDoor />
      <StatusDate />
      <StatusLock />
      </div>
      
    </header>
  );
}

export default StatusBar;
