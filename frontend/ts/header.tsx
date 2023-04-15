import React from "react";
import "../src/css/header.css";

export function Header() {
  return (
    <header className="header">
      <h1>Lasercutter HMI</h1>
      <div className="settings"></div>
      <div className="login"></div>
    </header>
  );
}

export default Header;
