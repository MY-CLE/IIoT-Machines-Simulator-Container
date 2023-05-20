import React from "react";
import ReactDOM from "react-dom/client";
import App from "./ts/App";
import "./css/output.css";

const root = ReactDOM.createRoot(document.getElementById("root")!);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
