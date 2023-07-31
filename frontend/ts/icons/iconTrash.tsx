import React from "react";

function IconTrash(props: {
  fill?: string;
  secondaryfill?: string;
  title?: string;
}) {
  const fill = props.fill || "black";
  const secondaryfill = props.secondaryfill || fill;
  const title = props.title || "trash can";

  return (
    <svg
      height="28"
      width="28"
      viewBox="0 0 64 64"
      xmlns="http://www.w3.org/2000/svg"
    >
      <title>{title}</title>
      <g fill={fill} stroke={fill} strokeWidth="2">
        <path
          d="M22,13V3H42V13"
          fill="black"
          strokeLinecap="square"
          strokeMiterlimit="10"
        />
        <path
          d="M53,19,50.332,56.356A5,5,0,0,1,45.345,61H18.655a5,5,0,0,1-4.987-4.644L11,19"
          fill="black"
          stroke={fill}
          strokeLinecap="square"
          strokeMiterlimit="10"
        />
        <line
          fill="none"
          strokeLinecap="square"
          strokeMiterlimit="10"
          x1="59"
          x2="5"
          y1="13"
          y2="13"
        />
      </g>
    </svg>
  );
}

export default IconTrash;
