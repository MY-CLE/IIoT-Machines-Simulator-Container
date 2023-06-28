import { Errors, Machine, Parameter, Program, Simulation } from "./interfaces";
import { enqueueSnackbar } from "notistack";
import axios, { Axios, AxiosResponse } from "axios";
const url = `${process.env.REACT_APP_SERVER_URL}`;

export const client = axios.create({
  baseURL: url,
});

client.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    //bug fix
    //if (error.response.status === 500)
    //  enqueueSnackbar("Internal Server Error", { variant: "error" });
    //  return Promise.reject(error);
    //}
    //enqueueSnackbar(error.message, { variant: "error" });
    return Promise.reject(error);
  }
);

client.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response.status === 500) {
      enqueueSnackbar("Internal Server Error", { variant: "error" });
      return Promise.reject(error);
    } else if (error.response.status >= 400) {
      enqueueSnackbar(error.response.data, { variant: "error" });
      return Promise.reject(error);
    }
    if (error.request) {
      enqueueSnackbar("Server not reachable", { variant: "error" });
      return Promise.reject(error);
    }

    enqueueSnackbar(error.response.data, { variant: "error" });
    return Promise.reject(error);
  }
);

export async function getSimulations(): Promise<{
  simulations: [Simulation];
} | null> {
  try {
    const response = await client.get(`/simulations`);
    //return response;
    return response.data;
  } catch (error: any) {
    return null;
  }
}

export async function createSimulation(): Promise<AxiosResponse | null> {
  let response;
  try {
    response = await client.put(`/simulations/${0}`);
    return response;
  } catch (error: any) {
    return null;
  }
}

export async function saveSimulation(
  name: string
): Promise<AxiosResponse | null> {
  let formdata = new FormData();
  formdata.append("action", "save");
  formdata.append("name", name);
  let response;
  try {
    response = await client.post(`/simulations`, formdata);
    enqueueSnackbar(response.data, { variant: "success" });
    return response;
  } catch (error: any) {
    return null;
  }
}

export async function loadSimulation(
  simulation_id: number
): Promise<AxiosResponse | null> {
  let response;
  try {
    response = await client.put(`/simulations/${simulation_id}`);
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}

export async function deleteSimulationById(
  simulation_id: number
): Promise<AxiosResponse | null> {
  let response;
  try {
    response = await client.delete(`/simulations/${simulation_id}`);
    enqueueSnackbar(response.data, { variant: "success" });
    return response;
  } catch (error: any) {
    return null;
  }
}

export async function getMachine(): Promise<Machine | null> {
  let response;
  try {
    response = await client.get(`/simulations/machine`);
    return await response.data;
  } catch (error: any) {
    return null;
  }
}

export async function authenticate(password: string): Promise<boolean | null> {
  let formdata = new FormData();
  formdata.append("password", password);
  let response;
  try {
    response = await client.put(`/simulations/machine/auth`, formdata);
    if (response.status === 200) return true;
    else return false;
  } catch (error: any) {
    return null;
  }
}
export async function setProtocol(
  formdata: FormData
): Promise<AxiosResponse | null> {
  let response;
  try {
    response = await client.patch(`/simulations/protocol`, formdata);
    enqueueSnackbar(response.data, { variant: "success" });
    return response;
  } catch (error: any) {
    return null;
  }
}

export async function startProgram(): Promise<AxiosResponse | null> {
  let response;
  try {
    response = await client.patch(`/simulations/machine/programs/current`, {
      id: 900,
      description: "program_status",
      value: "start",
    });
    enqueueSnackbar(response.data, { variant: "success" });
    return response;
  } catch (error: any) {
    return null;
  }
}

export async function stopProgram(): Promise<AxiosResponse | null> {
  let response;
  try {
    response = await client.patch(`/simulations/machine/programs/current`, {
      id: 900,
      description: "program_status",
      value: "stop",
    });
    enqueueSnackbar(response.data, { variant: "success" });
    return response;
  } catch (error: any) {
    return null;
  }
}
export async function resetMachine() {
  let response;
  try {
    response = await client.patch(`/simulations/machine/programs/current`, {
      id: 900,
      description: "program_status",
      value: "resetMachine",
    });
    enqueueSnackbar(response.data, { variant: "success" });
    return response;
  } catch (error: any) {
    return null;
  }
}

export async function resetProgram() {
  let response;
  try {
    response = await client.patch(`/simulations/machine/programs/current`, {
      id: 900,
      description: "program_status",
      value: "resetProgram",
    });
    enqueueSnackbar(response.data, { variant: "success" });
    return response;
  } catch (error: any) {
    return null;
  }
}

export async function patchMachineParameter(
  parameter: Parameter
): Promise<AxiosResponse | null> {
  let response;
  try {
    response = await client.patch(`/simulations/machine`, parameter);
    enqueueSnackbar(response.data, {
      variant: "success",
    });
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}

export async function getErrors(): Promise<AxiosResponse | null> {
  let response;
  try {
    response = await client.get(`/simulations/machine/notifications`);
    return response;
  } catch (error: any) {
    return null;
  }
}

export async function sendError(
  error_id: number
): Promise<AxiosResponse | null> {
  const formdata = new FormData();
  console.log(error_id);
  formdata.append("error_id", error_id.toString());
  formdata.append("warning_id", "");
  let response;
  try {
    response = await client.post(
      `/simulations/machine/notifications`,
      formdata
    );

    enqueueSnackbar(response.data, {
      variant: "success",
    });

    return response;
  } catch (error: any) {
    return null;
  }
}

export async function sendWarning(
  warning_id: number
): Promise<AxiosResponse | null> {
  const formdata = new FormData();
  console.log(warning_id);
  formdata.append("warning_id", warning_id.toString());
  formdata.append("error_id", "");

  let response;
  try {
    response = await client.post(
      `/simulations/machine/notifications`,
      formdata
    );
    enqueueSnackbar(response.data, {
      variant: "success",
    });
    return response;
  } catch (error: any) {
    return null;
  }
}

export async function clearNotifications(): Promise<AxiosResponse | null> {
  let response;
  try {
    response = await client.patch(`/simulations/machine/notifications`);
    enqueueSnackbar(response.data, {
      variant: "success",
    });

    return response;
  } catch (error: any) {
    return null;
  }
}

export async function getPrograms(): Promise<AxiosResponse | null> {
  console.log(`GET Request auf ${url}/simulations/machine/programs`);
  let response;
  try {
    response = await client.get(`/simulations/machine/programs`);
    return response;
  } catch (error: any) {
    return null;
  }
}

export async function setCurrentProgram(
  program_id: number
): Promise<AxiosResponse | null> {
  console.log(`POST Request auf ${url}/simulations/machine/programs/current`);
  const formdata = new FormData();
  formdata.append("program_id", program_id.toString());
  let response;
  try {
    response = await client.put(
      `/simulations/machine/programs/current`,
      formdata
    );
    enqueueSnackbar(await response.data, {
      variant: "success",
    });
    return response;
  } catch (error: any) {
    return null;
  }
}

export async function getProgram(): Promise<Program | null> {
  let response;
  try {
    response = await client.get(`/simulations/machine/programs/current`);
    return await response.data;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}

export async function sendProgramparameter(
  id: number,
  description: string,
  value: number
): Promise<AxiosResponse | null> {
  let myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  let response;
  try {
    response = await client.patch(`/simulations/machine/programs/current`, {
      id: id,
      description: description,
      value: value,
    });
    enqueueSnackbar(await response.data, {
      variant: "success",
    });
    return response;
  } catch (error: any) {
    enqueueSnackbar(error.message, { variant: "error" });
    return null;
  }
}
