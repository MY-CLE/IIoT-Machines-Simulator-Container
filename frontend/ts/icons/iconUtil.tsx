//icon control_panel from nucleo app

import * as React from "react";

function IconUtil(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="48"
      height="48"
      viewBox="0 0 48 48"
    >
      <title>control-panel</title>
      <g stroke-width="3" fill="#212121" stroke="#212121">
        <line
          fill="none"
          stroke-miterlimit="10"
          x1="24"
          y1="7"
          x2="24"
          y2="12"
          stroke-linejoin="miter"
          stroke-linecap="butt"
        ></line>{" "}
        <line
          fill="none"
          stroke-miterlimit="10"
          x1="46"
          y1="29"
          x2="41"
          y2="29"
          stroke-linejoin="miter"
          stroke-linecap="butt"
        ></line>{" "}
        <line
          fill="none"
          stroke-miterlimit="10"
          x1="2"
          y1="29"
          x2="7"
          y2="29"
          stroke-linejoin="miter"
          stroke-linecap="butt"
        ></line>{" "}
        <line
          fill="none"
          stroke-miterlimit="10"
          x1="39.556"
          y1="13.444"
          x2="36.021"
          y2="16.979"
          stroke-linejoin="miter"
          stroke-linecap="butt"
        ></line>{" "}
        <line
          fill="none"
          stroke-miterlimit="10"
          x1="8.444"
          y1="13.444"
          x2="11.979"
          y2="16.979"
          stroke-linejoin="miter"
          stroke-linecap="butt"
        ></line>{" "}
        <line
          fill="none"
          stroke-miterlimit="10"
          x1="22.654"
          y1="25.232"
          x2="19"
          y2="15"
          stroke-linejoin="miter"
          stroke-linecap="butt"
        ></line>{" "}
        <path
          fill="none"
          stroke="#212121"
          stroke-linecap="square"
          stroke-miterlimit="10"
          d="M42.435,41 C44.687,37.548,46,33.429,46,29c0-12.15-9.85-22-22-22S2,16.85,2,29c0,4.429,1.313,8.548,3.565,12H42.435z"
          stroke-linejoin="miter"
        ></path>{" "}
        <circle
          fill="none"
          stroke-linecap="square"
          stroke-miterlimit="10"
          cx="24"
          cy="29"
          r="4"
          stroke-linejoin="miter"
        ></circle>
      </g>
    </svg>
  );
}

export default IconUtil;
