//icon lock from nucleo app

import * as React from "react";

function IconLock(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="48"
      height="48"
      viewBox="0 0 48 48"
    >
      <title>lock</title>
      <g stroke-width="4" fill="#212121" stroke="#212121">
        <path
          d="M34,16V12A10.029,10.029,0,0,0,24,2h0A10.029,10.029,0,0,0,14,12v4"
          fill="none"
          stroke-linecap="square"
          stroke-miterlimit="10"
        ></path>
        <rect
          x="6"
          y="21"
          width="36"
          height="25"
          rx="4"
          fill="none"
          stroke="#212121"
          stroke-linecap="square"
          stroke-miterlimit="10"
        ></rect>
        <circle
          cx="24"
          cy="31"
          r="4"
          fill="none"
          stroke-linecap="square"
          stroke-miterlimit="10"
        ></circle>
        <line
          x1="24"
          y1="35"
          x2="24"
          y2="40"
          fill="none"
          stroke-linecap="square"
          stroke-miterlimit="10"
        ></line>
      </g>
    </svg>
  );
}

export default IconLock;
