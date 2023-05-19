//icon send_message from nucleo app

import * as React from "react";

function IconSendError(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="48"
      height="48"
      viewBox="0 0 48 48"
    >
      <title>send-message</title>
      <g stroke-width="3" fill="#212121" stroke="#212121">
        <line
          fill="none"
          stroke-miterlimit="10"
          x1="45"
          y1="3"
          x2="20"
          y2="28"
          stroke-linejoin="miter"
          stroke-linecap="butt"
        ></line>{" "}
        <polygon
          fill="none"
          stroke="#212121"
          stroke-linecap="square"
          stroke-miterlimit="10"
          points="45,3 28,45 20,28 3,20 "
          stroke-linejoin="miter"
        ></polygon>
      </g>
    </svg>
  );
}

export default IconSendError;
