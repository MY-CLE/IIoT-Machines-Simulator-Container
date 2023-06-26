import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getPrograms, setCurrentProgram } from "../api-service";
import { Program } from "../interfaces";

const url = "/simulator";

function ChooseProgramPage(props: {
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
}) {
  const navigation = useNavigate();
  const [programs, setPrograms] = useState<Array<Program>>([
    { description: "", parameters: null, id: null },
  ]);

  useEffect(() => {
    (async () => {
      let progs: { programs: Array<Program> } | null = null;
      let progsRes = await getPrograms();
      if (progsRes) {
        progs = (await progsRes.data) as { programs: Array<Program> };
      }
      console.log(progs);
      if (!progs) return;
      setPrograms(progs.programs);
    })();
  }, []);

  async function navigateToProgramStatePage(id: number) {
    console.log(id);
    const response = await setCurrentProgram(id);
    if (!response) {
      return;
    } else {
      props.setState({
        program_id: id,
        simulation_id: props.state.simulation_id,
      });

      navigation(`${url}/program/current`);
    }
  }

  return (
    <div className="flex flex-col flex-grow flex-nowrap">
      <div className="flex flex-col justify-start w-full h-full text-2xl bg-white border border-t-0 border-black border-1">
        {" "}
        {/*bg-program-choose-grey*/}
        <div className="w-full h-auto p-4 text-2xl text-center text-black sm:text-xl md:text-2xl lg:text-3xl xl:text-4xl 2xl:text-4xl 3xl:text-6xl 4xl:text-8xl">
          Program Selection
        </div>
        <div className="flex items-center justify-center flex-grow ">
          <div className="flex flex-row flex-wrap items-center justify-between w-full h-full mb-4p ">
            {programs.map((item: any) => {
              return (
                <ProgramCard
                  key={item.id}
                  name={item.description}
                  id={item.id}
                  func={navigateToProgramStatePage}
                />
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
export default ChooseProgramPage;

function ProgramCard(props: any) {
  return (
    <button
      className="flex items-center justify-center w-1/4 mx-6 border border-black bg-unselectedbar-green hover:bg-selectedbar-green rounded-2xl h-1/3 drop-shadow-sm"
      onClick={() => props.func(props.id)}
    >
      <span className="text-2xl sm:text-base lg:text-xl xl:text-3xl 2xl:text-3xl 3xl:text-4xl">
        {props.name}
      </span>
    </button>
  );
}
