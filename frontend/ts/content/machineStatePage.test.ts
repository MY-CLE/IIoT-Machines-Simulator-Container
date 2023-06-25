import { Machine } from "../interfaces";
import { render, screen } from "@testing-library/react";
import MachineStatePage from "./machineStatePage";

describe("MachineStatePage", () => {
  it("should render with no values", () => {
    const machine: Machine = {
      parameters: [],
      errorState: { errors: [], warnings: [] },
    };
    render(<MachineStatePage machine={machine} />);
    expect(screen.getByText("Machine State")).toBeInTheDocument();
  });
});
