// icon pen from nucleo app
import * as React from "react";

function IconPen(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="32"
      height="32"
      viewBox="0 0 32 32"
    >
      <title>pen</title>
      <g fill="#212121">
        <path
          d="M18.086,5.5,3.293,20.293a1.008,1.008,0,0,0-.27.49l-2,9A1,1,0,0,0,2,31a1.067,1.067,0,0,0,.217-.023l9-2a1.008,1.008,0,0,0,.49-.27L26.5,13.914Z"
          fill="#212121"
        ></path>{" "}
        <path d="M30.121,6.051,25.949,1.878a3.006,3.006,0,0,0-4.242,0L19.5,4.086,27.914,12.5l2.208-2.207A3.007,3.007,0,0,0,30.121,6.051Z"></path>
      </g>
    </svg>
  );
}

export default IconPen;
