import React from "react";
import StatusStatus from "./statusStatus";
import StatusPower from "./statusPower";
import StatusTime from "./statusTime";
import StatusUtil from "./statusUtilization";
import StatusError from "./statusError";
import StatusWarning from "./statusWarning";
import StatusSafetyDoor from "./statusSafetyDoor";
import StatusDate from "./statusDate";
import StatusCoolantLevel from "./statusCoolantLevel";

export function StatusBar(props: {
  runtime: number;
  utilization: number;
  error: number;
  warning: number;
  safety_door: boolean;
  coolantLevel: number;
  isProgramRunning: boolean;
}) {
  let date = new Date();
  return (
    <header>
      <div className="flex flex-row items-center justify-start w-full flex-nowrap h-fit">
        <StatusStatus />
        <StatusPower isProgramRunning={props.isProgramRunning} errors={props.error}/>
        <StatusTime value={props.runtime} />
        <StatusUtil value={props.utilization} />
        <StatusCoolantLevel value={props.coolantLevel} />
        <StatusWarning value={props.warning} />
        <StatusError value={props.error} />
        <StatusSafetyDoor value={props.safety_door} />
        <StatusDate value={date} />
      </div>
    </header>
  );
}

export default StatusBar;
