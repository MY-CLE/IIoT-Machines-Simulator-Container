//icon sensor_door from nucleo app

import * as React from "react";

function IconDoor(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="48"
      height="48"
      viewBox="0 0 24 24"
    >
      <title>sensor_door</title>
      <g fill="none">
        <path
          opacity=".3"
          d="M18 4v16H6V4h12zm-2.5 6.5c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5S17 12.83 17 12s-.67-1.5-1.5-1.5z"
          fill="none"
        ></path>
        <path
          stroke-width={2}
          d="M18 4v16H6V4h12zm0-2H6c-1.1 0-2 .9-2 2v18h16V4c0-1.1-.9-2-2-2zm-2.5 8.5c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5S17 12.83 17 12s-.67-1.5-1.5-1.5z"
          fill="#000000"
        ></path>
      </g>
    </svg>
  );
}

export default IconDoor;
