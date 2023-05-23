export interface Simulation {
  id: number;
  description: string;
  last_edited: Date;
  machine?: Machine;
  program?: Program;
}

export interface Machine {
  parameters: Array<Parameter>;
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
}
