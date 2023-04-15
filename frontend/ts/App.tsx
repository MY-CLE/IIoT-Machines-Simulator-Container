import React from "react";
import { useEffect, useState } from "react";
import "../src/css/App.css";
import Header from "./header";

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
    </div>
  );
}

export default App;
