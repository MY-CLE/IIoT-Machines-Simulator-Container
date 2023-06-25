import React from "react";
import ReactDOM from "react-dom/client";
import App from "./ts/App";
import "./css/output.css";
import { BrowserRouter } from "react-router-dom";
import { SnackbarProvider } from "notistack";

const root = ReactDOM.createRoot(document.getElementById("root")!);
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <SnackbarProvider>
        <App />
      </SnackbarProvider>
    </BrowserRouter>
  </React.StrictMode>
);
