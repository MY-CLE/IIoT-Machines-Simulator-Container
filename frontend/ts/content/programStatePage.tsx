import React from "react";
import ParameterComponent from "./parameters/parameter";
import IconArrowBack from "../icons/iconBackArrow";
import { Parameter, Program } from "../interfaces";
import { resetProgram, startProgram, stopProgram } from "../api-service";
import { useNavigate } from "react-router-dom";

const url = "/simulator";

function ProgramStatePage(props: {
  state: {
    simulation_id: number;
    program_id: number;
  };
  setState: React.Dispatch<
    React.SetStateAction<{
      simulation_id: number;
      program_id: number;
    }>
  >;
  program: Program;
}) {
  const navigation = useNavigate();
  return (
    <div className="flex flex-col flex-grow flex-nowrap">
      <div className="flex flex-col w-full h-full p-4 text-2xl bg-white border border-t-0 border-black border-1 ">
        <div className="flex flex-row items-center justify-between w-1/2 h-auto mb-4">
          <button
            onClick={() => {
              navigation(`${url}/programs`);
            }}
            className="w-1/8"
          >
            <IconArrowBack width={45} color={"#000"}></IconArrowBack>
          </button>
          <span className="flex flex-grow text-4xl text-left sm:text-base lg:text-xl xl:text-2xl 2xl:text-3xl 3xl:text-4xl ">
            Program Overview: {props.program.description}
          </span>
        </div>
        <div className="flex flex-row justify-between w-full h-full mb-4 ">
          <div className="flex flex-row flex-wrap w-1/2 h-full justify-evenly ">
            {props.program.parameters!.map((item: Parameter) => {
              return (
                <ParameterComponent
                  key={item.id}
                  name={item.description}
                  value={item.value}
                  id={item.id}
                  isAdminParameter={item.isAdminParameter}
                />
              );
            })}
          </div>
          <div className="flex flex-col items-center w-1/2 h-full justify-evenly">
            <button
              className="w-1/3 text-xl text-white bg-green-400 border-2 border-black rounded-md shadow h-14 lg:text-2xl xl:text-2xl 2xl:text-3xl 3xl:text-4xl"
              onClick={() => startProgram()}
            >
              Start
            </button>
            <button
              className="w-1/3 text-xl text-white bg-red-400 border-2 border-black rounded-md shadow h-14 lg:text-2xl xl:text-2xl 2xl:text-3xl 3xl:text-4xl"
              onClick={() => stopProgram()}
            >
              Stop
            </button>
            <button
              className="w-1/3 text-xl text-white bg-yellow-400 border-2 border-black rounded-md h-14 lg:text-2xl xl:text-2xl 2xl:text-3xl 3xl:text-4xl"
              onClick={() => resetProgram()}
            >
              Reset values
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
export default ProgramStatePage;
