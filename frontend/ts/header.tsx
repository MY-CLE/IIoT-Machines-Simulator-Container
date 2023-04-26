import React from "react";
import "../src/css/header.css";
import IconLogin from "./icons/iconLogin";
import IconSettings from "./icons/iconSettings";

export function Header() {
  return (
    <header className="header">
      <h1>Lasercutter HMI</h1>
      <div className="save"></div>
      <div className="config"></div>
      <div className="login"></div>
    </header>
  );
} 

export default Header;