import React from "react";

function IconSave(props: { title?: string }) {
  const title = props.title || "floppy disk";

  return (
    <svg
      height="auto"
      width="auto"
      viewBox="0 0 12 12"
      xmlns="http://www.w3.org/2000/svg"
    >
      <title>{title}</title>
      <g fill="#fff" stroke="#fff" strokeWidth="1">
        <path
          d="M2,.5H8.567L11.5,3.433V10A1.5,1.5,0,0,1,10,11.5H2A1.5,1.5,0,0,1,.5,10V2A1.5,1.5,0,0,1,2,.5Z"
          fill="none"
          stroke="#fff"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <polyline
          fill="none"
          points="2.5 9.5 2.5 6.5 9.5 6.5 9.5 9.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <line
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
          x1="7.5"
          x2="7.5"
          y1="2.5"
          y2="4.5"
        />
      </g>
    </svg>
  );
}

export default IconSave;
