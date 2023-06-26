export interface Simulation {
  id: number;
  description: string;
  last_edited: Date;
  machine?: Machine;
  program?: Program;
}

export interface Machine {
  parameters: Array<Parameter>;
  errorState: Errors;
  isProgramRunning: boolean;
}

export interface Program {
  id: number | null;
  description?: string;
  parameters: Array<Parameter> | null;
}

export interface Error {
  id: number;
  name: string;
}

export interface Errors {
  errors: Array<Error>;
  warnings: Array<Error>;
}

export interface Parameter {
  id: number;
  description: string;
  value: number;
  isAdminParameter: boolean;
}

export interface StatusBarValues {
  runtime: number;
  utilization: number;
  error: number;
  warning: number;
  safety_door: boolean;
  coolantLevel: number;
  isProgramRunning: boolean;
}
