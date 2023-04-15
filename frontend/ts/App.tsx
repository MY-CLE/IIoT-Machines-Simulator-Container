import React from "react";
import { useEffect, useState } from "react";
import "../src/css/App.css";
import Header from "./header";
import StatusBar from "./statusbar/statusBar";

function App() {
  return (
    <div className="App">
      <Header />
      <StatusBar />
    </div>
  );
}

export default App;
