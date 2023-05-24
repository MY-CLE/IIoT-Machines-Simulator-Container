import { Errors, Machine, Program, Simulation } from "./interfaces";

const url = `${process.env.REACT_APP_SERVER_URL}`;
// ? `${process.env.REACT_APP_SERVER_URL}`
// : "";
export async function getSimultions(): Promise<{ simulations: [Simulation] }> {
  console.log(`GET Request auf ${url}/simulations`);

  return await fetch(url + "/simulations", {
    method: "GET",
    redirect: "follow",
  })
    .then((response) => {
      return response.json();
    })
    .catch((error) => console.log("error", error));
}

export async function getSimulationById(
  simulation_id: number
): Promise<Simulation> {
  return await fetch(`${url}/simulations?simulation_id=${simulation_id}`, {
    method: "GET",
    redirect: "follow",
  })
    .then((response) => response.json())
    .catch((error) => console.log("error", error));
}

export async function postSimulation(
  simulation?: Simulation
): Promise<{ simulation_id: number }> {
  console.log(`POST Request auf ${url}/simulations`);

  return await fetch(`${url}/simulations`, {
    method: "POST",
    redirect: "follow",
    body: JSON.stringify(simulation ? simulation : {}),
  })
    .then((response) => response.json())
    .catch((error) => console.log("error", error));
}

export async function deleteSimulationById(simulation_id: number) {
  return await fetch(`${url}/simulations?simulation_id=${simulation_id}`, {
    method: "DELETE",
    redirect: "follow",
  })
    .then((response) => response.status)
    .catch((error) => console.log("error", error));
}

export async function getMachine(simulation_id: number): Promise<Machine> {
  console.log(`GET Request auf ${url}/simulations/${simulation_id}/machine`);

  return await fetch(`${url}/simulations/${simulation_id}/machine`, {
    method: "GET",
    redirect: "follow",
  })
    .then((response) => response.json())
    .catch((error) => console.log("error", error));
}

export async function authenticate(simulation_id: number, password: string) {
  let formdata = new FormData();
  formdata.append("password", password);

  return await fetch(`${url}/simulations/${simulation_id}/machine/auth`, {
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
  return await fetch(`${url}/simulations/${simulation_id}/machine`, {
    method: "PUT",
    body: JSON.stringify(parameter),
    redirect: "follow",
  })
    .then((response) => response.status)
    .catch((error) => console.log("error", error));
}

export async function getErrors(simulation_id: number): Promise<Errors> {
  console.log(
    `GET Request auf ${url}/simulations/${simulation_id}/machine/errors`
  );

  return await fetch(`${url}/simulations/${simulation_id}/machine/errors`, {
    method: "GET",
    redirect: "follow",
  })
    .then((response) => response.json())
    .catch((error) => console.log("error", error));
}

export async function sendError(simulation_id: number, error_id: number) {
  const formdata = new FormData();
  formdata.append("error_id", error_id.toString());
  return await fetch(`${url}/simulations/${simulation_id}/machine/errors`, {
    method: "POST",
    redirect: "follow",
    body: formdata,
  })
    .then((response) => response.status)
    .catch((error) => console.log("error", error));
}

export async function getPrograms(
  simulation_id: number
): Promise<{ programs: Array<Program> }> {
  return await fetch(`${url}/simulations/${simulation_id}/machine/programs`, {
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
    `${url}/simulations/${simulation_id}/machine/programs/current?program_id=${program_id}`,
    {
      method: "POST",
      redirect: "follow",
      body: formdata,
    }
  )
    .then((response) => response.status)
    .catch((error) => console.log("error", error));
}

export async function getProgram(simulation_id: number): Promise<Program> {
  return await fetch(
    `${url}/simulations/${simulation_id}/machine/programs/current`,
    {
      method: "GET",
      redirect: "follow",
    }
  )
    .then((response) => response.json())
    .catch((error) => console.log("error", error));
}

export async function sendProgramparameter(
  simulation_id: number,
  parameter: { parameter: [{ id: number; description: string; value: number }] }
) {
  let myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  return await fetch(
    `${url}/simulations/${simulation_id}/machine/programs/current`,
    {
      method: "PATCH",
      headers: myHeaders,
      body: JSON.stringify(parameter),
      redirect: "follow",
    }
  )
    .then((response) => response.status)
    .catch((error) => console.log("error", error));
}
