import React from "react";
import IconWarning from "../../icons/iconWarning";

export function StatusWarning() {
  return (
    <>
      <div className="flex-grow w-auto justify-center h-32 border flex items-center border-black border-1 border-l-0">
        <div>
          <IconWarning />
        </div>
      </div>
    </>
  );
}

export default StatusWarning;
