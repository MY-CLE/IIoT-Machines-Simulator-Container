import { useEffect, useState } from "react";
import logo from "./logo.svg";
import "./App.css";

function App() {
  const [time, setTime] = useState([]);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = () => {
    // Where we're fetching data from
    return (
      fetch("/api/time")
        // We get the API response and receive data in JSON format
        .then((response) => response.json())
        .then((data) => setTime(data.time))
        .catch((error) => console.error(error))
    );
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          TIME: {time} <code>src/App.js</code> and save to reload.
        </p>
        <p></p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
