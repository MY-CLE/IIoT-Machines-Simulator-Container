import { Errors, Machine, Parameter, Program, Simulation } from "./interfaces";
import { enqueueSnackbar } from "notistack";
import axios from "axios";
const url = `${process.env.REACT_APP_SERVER_URL}`;

// export const client = axios.create({
//   baseURL: "http://localhost:5000",
// });

// client.interceptors.request.use(
//   (config) => {
//     console.log(config);
//     config.url = `${url}${config.url}`;
//     return config;
//   },
//   (error) => {
//     console.log(error.response);
//     if (error.response.status === 500) {
//       enqueueSnackbar("Internal Server Error", { variant: "error" });
//       return Promise.reject(error);
//     }
//     enqueueSnackbar(error.message, { variant: "error" });
//     return Promise.reject(error);
//   }
// );

// axios.interceptors.response.use(
//   (response) => {
//     console.log(response);
//     return response;
//   },
//   (error) => {
//     console.log(error.response);
//     if (error.response.status === 500) {
//       enqueueSnackbar("Internal Server Error", { variant: "error" });
//       return Promise.reject(error);
//     }
//     enqueueSnackbar(error.message, { variant: "error" });
//     return Promise.reject(error);
//   }
// );

export async function getSimulations(): Promise<{
  simulations: [Simulation];
} | null> {
  try {
    console.log("axios: getSimulations");
    const response = await axios.get(`${url}/simulations`);
    console.log("axios: res:", response);
    //return response;
    return null;
  } catch (error: any) {
    console.log("axios: error:", error);
    return null;
  }
}

export async function createSimulation(): Promise<Response | null> {
  let response;
  try {
    response = await fetch(`${url}/simulations/${1}`, {
      method: "PUT",
      redirect: "follow",
    });
    if (!response.ok) {
      await response.text().then((text) => {
        throw new Error(text);
      });
    }
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}

export async function saveSimulation(name: string): Promise<Response | null> {
  let formdata = new FormData();
  formdata.append("action", "save");
  formdata.append("name", name);
  console.log(`POST Request auf ${url}/simulations`);
  let response;
  try {
    response = await fetch(`${url}/simulations`, {
      method: "POST",
      redirect: "follow",
      body: formdata,
    });
    if (!response.ok) {
      await response.text().then((text) => {
        throw new Error(text);
      });
    }
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}

export async function loadSimulation(
  simulation_id: number
): Promise<Response | null> {
  console.log(`PUT Request auf ${url}/simulations with ${simulation_id}`);
  let response;
  try {
    response = await fetch(`${url}/simulations/${simulation_id}`, {
      method: "PUT",
      redirect: "follow",
    });
    if (!response.ok) {
      await response.text().then((text) => {
        throw new Error(text);
      });
    }
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}

export async function deleteSimulationById(
  simulation_id: number
): Promise<Response | null> {
  console.log(`DELETE Request auf ${url}/simulations/${simulation_id}`);
  let response;
  try {
    response = await fetch(`${url}/simulations/${simulation_id}`, {
      method: "DELETE",
      redirect: "follow",
    });
    if (!response.ok) {
      await response.text().then((text) => {
        throw new Error(text);
      });
    }
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}

export async function getMachine(): Promise<Response | null> {
  console.log(`GET Request auf ${url}/simulations/machine`);

  let response;
  try {
    response = await fetch(`${url}/simulations/machine`, {
      method: "GET",
      redirect: "follow",
    });
    if (!response.ok) {
      await response.text().then((text) => {
        throw new Error(text);
      });
    }
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}

export async function authenticate(password: string): Promise<any> {
  let formdata = new FormData();
  formdata.append("password", password);
  let response;
  try {
    response = await fetch(`${url}/simulations/machine/auth`, {
      method: "PUT",
      body: formdata,
      redirect: "follow",
    });
    if (!response.ok) {
      await response.text().then((text) => {
        throw new Error(text);
      });
    }
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}
export async function setProtocol(formdata: FormData) {
  let response;
  try {
    response = await fetch(`${url}/simulations/protocol`, {
      method: "PATCH",
      body: formdata,
      redirect: "follow",
    });
    if (!response.ok) {
      await response.text().then((text) => {
        throw new Error(text);
      });
    }
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}

export async function startProgram() {
  let response;
  try {
    response = await fetch(`${url}/simulations/machine/programs/current`, {
      method: "PATCH",
      redirect: "follow",
      body: JSON.stringify({
        id: 900,
        description: "program_status",
        value: "start",
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      await response.text().then((text) => {
        throw new Error(text);
      });
    }
    enqueueSnackbar(await response.text().then((text) => text), {
      variant: "success",
    });
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}
export async function stopProgram() {
  let response;
  try {
    response = await fetch(`${url}/simulations/machine/programs/current`, {
      method: "PATCH",
      redirect: "follow",
      body: JSON.stringify({
        id: 900,
        description: "program_status",
        value: "stop",
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      await response.text().then((text) => {
        throw new Error(text);
      });
    }
    enqueueSnackbar(await response.text().then((text) => text), {
      variant: "success",
    });
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}

export async function resetProgram() {
  let response;
  try {
    response = await fetch(`${url}/simulations/machine/programs/current`, {
      method: "PATCH",
      redirect: "follow",
      body: JSON.stringify({
        id: 900,
        description: "program_status",
        value: "reset",
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      await response.text().then((text) => {
        throw new Error(text);
      });
    }
    enqueueSnackbar(await response.text().then((text) => text), {
      variant: "success",
    });
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}

export async function patchMachineParameter(parameter: Parameter) {
  let myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  let response;
  try {
    response = await fetch(`${url}/simulations/machine`, {
      method: "PATCH",
      body: JSON.stringify(parameter),
      redirect: "follow",
      headers: myHeaders,
    });
    if (!response.ok) {
      await response.text().then((text) => {
        throw new Error(text);
      });
    }
    enqueueSnackbar(await response.text().then((text) => text), {
      variant: "success",
    });
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}

export async function getErrors(): Promise<Response | null> {
  let response;
  try {
    response = await fetch(`${url}/simulations/machine/notifications`, {
      method: "GET",
      redirect: "follow",
    });
    if (!response.ok) {
      await response.text().then((text) => {
        throw new Error(text);
      });
    }
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}

export async function sendError(error_id: number) {
  const formdata = new FormData();
  console.log(error_id);
  formdata.append("error_id", error_id.toString());
  formdata.append("warning_id", "");
  let response;
  try {
    response = await fetch(`${url}/simulations/machine/notifications`, {
      method: "POST",
      redirect: "follow",
      body: formdata,
    });
    if (!response.ok) {
      await response.text().then((text) => {
        throw new Error(text);
      });
    }
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}

export async function sendWarning(warning_id: number) {
  const formdata = new FormData();
  console.log(warning_id);
  formdata.append("warning_id", warning_id.toString());
  formdata.append("error_id", "");
  let response;
  try {
    response = await fetch(`${url}/simulations/machine/notifications`, {
      method: "POST",
      redirect: "follow",
      body: formdata,
    });
    if (!response.ok) {
      await response.text().then((text) => {
        throw new Error(text);
      });
    }
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}

export async function clearNotifications() {
  let response;
  try {
    response = await fetch(`${url}/simulations/machine/notifications`, {
      method: "PATCH",
      redirect: "follow",
    });
    if (!response.ok) {
      await response.text().then((text) => {
        throw new Error(text);
      });
    }
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}

export async function getPrograms(): Promise<Response | null> {
  console.log(`GET Request auf ${url}/simulations/machine/programs`);
  let response;
  try {
    response = await fetch(`${url}/simulations/machine/programs`, {
      method: "GET",
      redirect: "follow",
    });
    if (!response.ok) {
      await response.text().then((text) => {
        throw new Error(text);
      });
    }
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}

export async function setCurrentProgram(program_id: number) {
  console.log(`POST Request auf ${url}/simulations/machine/programs/current`);
  const formdata = new FormData();
  formdata.append("program_id", program_id.toString());
  let response;
  try {
    response = await fetch(`${url}/simulations/machine/programs/current`, {
      method: "PUT",
      redirect: "follow",
      body: formdata,
    });
    if (!response.ok) {
      await response.text().then((text) => {
        throw new Error(text);
      });
    }
    enqueueSnackbar(await response.text().then((text) => text), {
      variant: "success",
    });
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}

export async function getProgram(): Promise<Response | null> {
  let response;
  try {
    response = await fetch(`${url}/simulations/machine/programs/current`, {
      method: "GET",
      redirect: "follow",
    });
    if (!response.ok) {
      await response.text().then((text) => {
        throw new Error(text);
      });
    }
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}

export async function sendProgramparameter(
  id: number,
  description: string,
  value: number
) {
  let myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  let response;
  try {
    response = await fetch(`${url}/simulations/machine/programs/current`, {
      method: "PATCH",
      headers: myHeaders,
      body: JSON.stringify({ id: id, description: description, value: value }),
      redirect: "follow",
    });
    if (!response.ok) {
      await response.text().then((text) => {
        throw new Error(text);
      });
    }
    enqueueSnackbar(await response.text().then((text) => text), {
      variant: "success",
    });
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}
