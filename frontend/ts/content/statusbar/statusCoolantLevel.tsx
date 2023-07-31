import React from "react";
import IconDrop from "../../icons/iconDrop";
import IconDropEmpty from "../../icons/iconDropEmpty";
import IconDropHalf from "../../icons/iconDropHalf";

export function statusCoolantLevel(props: { value: number }) {
  return (
    <>
      <div className="flex flex-col flex-wrap items-center justify-center w-1/10 h-32 border border-l-0 border-black border-1">
        <div className="mb-3">
          {props.value >= 60 && <IconDrop />}
          {props.value < 60 && props.value > 20 && <IconDropHalf />}
          {props.value <= 20 && <IconDropEmpty />}


        </div>
        <div className="text-xs sm:text-base lg:text-xl xl:text2xl">{props.value} %</div>
      </div>
    </>
  );
}

export default statusCoolantLevel;
