// icon:power | Feathericons https://feathericons.com/ | Cole Bemis
import * as React from "react";

function IconPower(props: {symbolColor: string}) {
  return (
    <svg
      fill="none"
      stroke={props.symbolColor}
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={3}
      viewBox="0 0 24 24"
      height="1em"
      width="1em"
      {...props}
    >
      <path d="M18.36 6.64a9 9 0 11-12.73 0M12 2v10" />
    </svg>
  );
}

export default IconPower;
