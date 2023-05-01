import React from "react";
import StatusPower from "./statusPower";
import "../src/css/statusBar.css";

export function StatusBar() {
  return (
    <header className="statusBar">
      <StatusPower />
    </header>
  );
}

export default StatusBar;
