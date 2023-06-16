import React from "react";

export function StatusDate(props: { value: Date }) {
  const parseDateTime = (dateTimeString: Date) => {
    const dateObj = new Date(dateTimeString);
    const hours = dateObj.getHours().toString().padStart(2, "0");
    const minutes = dateObj.getMinutes().toString().padStart(2, "0");
    const seconds = dateObj.getSeconds().toString().padStart(2, "0");
    const day = dateObj.getDate().toString().padStart(2, "0");
    const month = (dateObj.getMonth() + 1).toString().padStart(2, "0");
    const year = dateObj.getFullYear().toString();
    return `${hours}:${minutes}:${seconds} ${day}.${month}.${year}`;
  };

  const date = parseDateTime(props.value);
  return (
    <>
      <div className="flex items-center justify-center w-1/5 h-32 border border-l-0 border-black border-1 text-xs sm:text-base lg:text-xl xl:text2xl">
        <div className="px-5">{date}</div>
      </div>
    </>
  );
}

export default StatusDate;
