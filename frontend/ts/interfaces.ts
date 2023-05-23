export interface Simulation {
  id: number;
  description: string;
  last_edited: Date;
  machine?: Machine;
  program?: Program;
}

export interface Machine {
  parameter: [Parameter];
}

export interface Program {
  description?: string;
  parameter: [Parameter];
}

export interface Error {
  id: number;
  name: string;
}

export interface Parameter {
  id: number;
  description: string;
  value: number;
}
