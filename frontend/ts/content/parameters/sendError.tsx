import React, {useState} from "react";
import IconSendError from "../../icons/iconSendError";
import { Error } from "../../interfaces";
import { sendError, sendWarning } from "../../api-service";

interface sendErrorProps {
  simulationID: number;
  name: string;
  messages: Array<Error>;
  color: string;
}

function SendError(props: sendErrorProps) {
  const [selectedID, setSelectedID] = useState<number | null> (null);

  const handleSendError = () => {
    if(selectedID === null){
      console.log(`No ${props.name} selected`);
      return;
    }
    console.log(props.name)
    if(props.name === "Error"){

      sendError(props.simulationID, selectedID).then((response) => {
        console.log(`${props.name} ${selectedID} sent successfully`)
      }).catch((error) => {
        console.log(`Error sending ${props.name} ${selectedID}`, error);
      });
    }
    else{
      sendWarning(props.simulationID, selectedID)
    }
  }

  const handleSelectChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const errorID = parseInt(event.target.value, 10);
    setSelectedID(errorID);
    console.log(`${errorID} selected`);
  }
  return (
    <div className="flex flex-col bg-white h-full w-full border justify-start items-center border-black rounded-lg drop-shadow-sm space-y-7 py-5">
      <div className="mt-5 font-medium text-xs sm:text-base lg:text-xl xl:text2xl">Send {props.name}</div>
      <select
        className="w-3/4 h-1/5 border border-black rounded-lg bg-gray-400 text-center text-xs sm:text-base lg:text-xl xl:text2xl"
        name={props.name}
        id={props.name}
        onChange={handleSelectChange}
      >
        <option value="">Select {props.name}</option>
        {props.messages.map((item) => {
          return (
            <option key={item.id} value={item.id}>
              {item.name}
            </option>
          );
        })}
      </select>
      <button
        className={`${props.color} flex justify-center items-center w-1/5 h-1/4 border border-black rounded-lg pt-2 pb-2`}
        onClick={handleSendError}
      >
        <IconSendError />
      </button>
    </div>
  );
}

export default SendError;
