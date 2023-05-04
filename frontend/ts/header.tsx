import React from "react";
import IconLogin from "./icons/iconLogin";
import IconSettings from "./icons/iconSettings";

export function Header() {
  return (
    <header className="flex flex-row items-center justify-between w-screen h-20 text-white bg-header-red">
      <h1 className="justify-center pl-8 text-3xl font-semibold text-center">
        Lasercutter HMI
      </h1>
      <div className="flex flex-row justify-end basis-1/6">
        <IconLogin className="mx-3" />
        <IconSettings className="mx-3" />
      </div>
    </header>
  );
}

export default Header;
