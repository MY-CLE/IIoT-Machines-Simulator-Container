// icon:alert-circle | Entypo https://feathericons.com/ | Cole Bemis
import * as React from "react";

function IconError(props: {hasElements: boolean}) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="48"
      height="48"
      viewBox="0 0 24 24"
      fill={props.hasElements ? "#ff0000" : "gray"}
      stroke={props.hasElements ? "#000000" : "gray"}
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      <circle cx="12" cy="12" r="10"></circle>
      <line x1="12" y1="8" x2="12" y2="12"></line>
      <line x1="12" y1="16" x2="12.01" y2="16"></line>
    </svg>
  );
}

export default IconError;
