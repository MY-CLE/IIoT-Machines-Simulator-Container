import React from "react";

function IconArrowBack(props: {
  width?: number;
  height?: number;
  title?: string;
}) {
  const width = props.width || "100%";
  const height = props.height || "100%";
  const title = props.title || "arrow back";

  return (
    <svg
      height={height}
      width={width}
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <title>{title}</title>
      <g fill="none">
        <path
          d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"
          fill="#fff"
        />
      </g>
    </svg>
  );
}

export default IconArrowBack;
