import React from "react";

export function Header() {
  return (
    <header className="flex flex-row justify-between w-screen text-white h-20Lasercutter HMI align-center bg-header-red">
      <h1 className="pl-8 ">Lasercutter HMI</h1>
      <div className="save"></div>
      <div className="config"></div>
      <div className="login "></div>
    </header>
  );
}

export default Header;
