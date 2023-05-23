import React from "react";
import IconSendError from "../../icons/iconSendError";
import { Error } from "../../interfaces";

interface sendErrorProps {
  name: string;
  messages: Array<Error>;
  color: string;
}

function SendError(props: sendErrorProps) {
  return (
    <div className="flex flex-col bg-white h-full w-full border justify-start items-center border-black rounded-lg drop-shadow-sm space-y-7 pb-5">
      <div className="mt-5 font-medium">{props.name}</div>
      <select
        className="w-3/4 h-1/5 border border-black rounded-lg bg-gray-400 text-center text-xl"
        name={props.name}
        id={props.name}
      >
        {props.messages.map((item) => {
          return (
            <option key={item.id} value={item.name}>
              {item.name}
            </option>
          );
        })}
      </select>
      <button
        className={`${props.color} flex justify-center items-center w-1/5 h-1/4 border border-black rounded-lg pt-2 pb-2`}
      >
        <IconSendError />
      </button>
    </div>
  );
}

export default SendError;
