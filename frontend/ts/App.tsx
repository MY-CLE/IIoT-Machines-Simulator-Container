import React from "react";
import { useEffect, useState } from "react";
import "../src/css/App.css";
import "../src/css/button.css";
import Header from "./header";
import StatusBar from "./statusbar/statusBar";

function App() {
  /*
  let [time, setTime] = useState([]);

  useEffect(() => {
    fetchTime();
  }, []);

  const fetchTime = () => {
    // Where we're fetching data from
    return (
      fetch("/api/time")
        // We get the API response and receive data in JSON format
        .then((response) => response.json())
        .then((data) => setTime(data.time))
        .catch((error) => console.error(error))
    );
  };
  */

  
    return (
      <div className="App">
        <Header />
        <div className="buttoncontainer">
          <button className="button">Simulation starten</button>
          <button className="button">Simulation laden</button>
        </div>
      </div>
    );
  }

export default App;
