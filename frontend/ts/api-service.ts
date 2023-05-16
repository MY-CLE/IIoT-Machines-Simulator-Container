import { Machine, Program, Simulation } from "./interfaces";

export async function getSimultions(): Promise<[Simulation]> {
  return await fetch("/simulations", {
    method: "GET",
    redirect: "follow",
  })
    .then((response) => response.json())
    .catch((error) => console.log("error", error));
}

export async function getSimulationById(
  simulation_id: number
): Promise<Simulation> {
  return await fetch(`/simulations?simulation_id=${simulation_id}`, {
    method: "GET",
    redirect: "follow",
  })
    .then((response) => response.json())
    .catch((error) => console.log("error", error));
}

export async function postSimulation(simulation: Simulation) {
  return await fetch("/simulation", {
    method: "POST",
    redirect: "follow",
    body: JSON.stringify(simulation),
  })
    .then((response) => response.status)
    .catch((error) => console.log("error", error));
}

export async function deleteSimulationById(simulation_id: number) {
  return await fetch(`/simulations?simulation_id=${simulation_id}`, {
    method: "DELETE",
    redirect: "follow",
  })
    .then((response) => response.status)
    .catch((error) => console.log("error", error));
}

export async function getMachine(simulation_id: number): Promise<Machine> {
  return await fetch(`/simulations/${simulation_id}/machine`, {
    method: "GET",
    redirect: "follow",
  })
    .then((response) => response.json())
    .catch((error) => console.log("error", error));
}

export async function authenticate(simulation_id: number, password: string) {
  let formdata = new FormData();
  formdata.append("password", password);

  return await fetch(`/simulations/${simulation_id}/machine/auth`, {
    method: "PUT",
    body: formdata,
    redirect: "follow",
  })
    .then((response) => response.status)
    .catch((error) => console.log("error", error));
}

export async function patchMachineParameter(
  simulation_id: number,
  parameter: Machine
) {
  let myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  return await fetch(`/simulations/${simulation_id}/machine`, {
    method: "PUT",
    body: JSON.stringify(parameter),
    redirect: "follow",
  })
    .then((response) => response.status)
    .catch((error) => console.log("error", error));
}

export async function getErrors(simulation_id: number): Promise<Error> {
  return await fetch(`/simulations/${simulation_id}/machine/errors`, {
    method: "GET",
    redirect: "follow",
  })
    .then((response) => response.json())
    .catch((error) => console.log("error", error));
}

export async function sendError(simulation_id: number, error_id: number) {
  const formdata = new FormData();
  formdata.append("error_id", error_id.toString());
  return await fetch(`/simulations/${simulation_id}/machine/errors`, {
    method: "POST",
    redirect: "follow",
    body: formdata,
  })
    .then((response) => response.status)
    .catch((error) => console.log("error", error));
}

export async function getPrograms(simulation_id: number): Promise<[Program]> {
  return await fetch(`/simulations/${simulation_id}/machine/programs`, {
    method: "GET",
    redirect: "follow",
  })
    .then((response) => response.json())
    .catch((error) => console.log("error", error));
}

export async function postCurrentProgram(
  simulation_id: number,
  program_id: number
) {
  const formdata = new FormData();
  formdata.append("program_id", program_id.toString());
  return await fetch(
    `/simulations/${simulation_id}/machine/programs/current?program_id=${program_id}`,
    {
      method: "POST",
      redirect: "follow",
      body: formdata,
    }
  )
    .then((response) => response.status)
    .catch((error) => console.log("error", error));
}

export async function getProgram(simulation_id: number): Promise<[Program]> {
  return await fetch(`/simulations/${simulation_id}/machine/programs/current`, {
    method: "GET",
    redirect: "follow",
  })
    .then((response) => response.json())
    .catch((error) => console.log("error", error));
}

export async function sendProgramparameter(
  simulation_id: number,
  parameter: { parameter: [{ id: number; description: string; value: number }] }
) {
  let myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  return await fetch(`/simulations/${simulation_id}/machine/programs/current`, {
    method: "PATCH",
    headers: myHeaders,
    body: JSON.stringify(parameter),
    redirect: "follow",
  })
    .then((response) => response.status)
    .catch((error) => console.log("error", error));
}
