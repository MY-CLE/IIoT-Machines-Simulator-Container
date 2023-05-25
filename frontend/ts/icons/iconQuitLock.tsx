//icon lock from nucleo app

import * as React from "react";

function IconQuitLock(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="128"
      height="128"
      viewBox="0 0 64 64"
    >
      <title>lock</title>
      <g fill="#212121">
        <path d="M45,25H43V14a11,11,0,0,0-22,0V25H19V14a13,13,0,0,1,26,0Z"></path>
        <path
          d="M53,27H11a4,4,0,0,0-4,4V59a4,4,0,0,0,4,4H53a4,4,0,0,0,4-4V31A4,4,0,0,0,53,27ZM33,47.91V54a1,1,0,0,1-2,0V47.91a6,6,0,1,1,2,0Z"
          fill="#212121"
        ></path>
      </g>
    </svg>
  );
}

export default IconQuitLock;
