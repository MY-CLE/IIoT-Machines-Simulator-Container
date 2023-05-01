import React from "react";
import LandingPage from "./content/landingpage";
import Header from "./header";

function App() {
  return (
    <div className="flex flex-col flex-grow w-screen h-screen ">
      <Header />
      <LandingPage />
    </div>
  );
}
export default App;
