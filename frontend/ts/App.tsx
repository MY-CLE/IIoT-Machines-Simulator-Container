import React from "react";
import Header from "./header";
import ProgramStatePage from "./content/programStatepage";

function App() {
  return (
    <div className="flex flex-col flex-grow w-screen h-screen">
      <Header />
      <ProgramStatePage program={program} />
    </div>
  );
}
export default App;

const program = {
  description: "Zahnrad",
  parameters: [
    {
      id: "1",
      description: "current_amount",
      value: "50",
    },
    {
      id: "2",
      description: "target_amount",
      value: "100",
    },
    {
      id: "3",
      description: "uptime_in_s",
      value: "50",
    },
    {
      id: "4",
      description: "power_consumption_in_Wh",
      value: "5000",
    },
    {
      id: "5",
      description: "coolant_consumption_in_percent",
      value: "10",
    },
    {
      id: "6",
      description: "time_per_item_in_s",
      value: "1",
    },
    {
      id: "1",
      description: "current_amount",
      value: "50",
    },
    {
      id: "2",
      description: "target_amount",
      value: "100",
    },
    {
      id: "3",
      description: "uptime_in_s",
      value: "50",
    },
    {
      id: "4",
      description: "power_consumption_in_Wh",
      value: "5000",
    },
    {
      id: "5",
      description: "coolant_consumption_in_percent",
      value: "10",
    },
    {
      id: "6",
      description: "time_per_item_in_s",
      value: "1",
    },
  ],
};
