export interface Simulation {
  id: number;
  description: string;
  last_edited: Date;
  machine: Machine;
  program: Program;
}

export interface Machine {
  parameter: [
    {
      id: number;
      discription: string;
      value: number;
    }
  ];
}

export interface Program {
  description: string;
  parameter: [
    {
      id: number;
      discription: string;
      value: number;
    }
  ];
}

export interface Error {
  id: number;
  name: string;
}
