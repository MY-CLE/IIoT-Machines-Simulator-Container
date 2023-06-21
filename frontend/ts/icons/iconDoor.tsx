//icon sensor_door from nucleo app

import React, { useState, useEffect } from "react";

function IconDoor(props: {isOpen:boolean}) {
  const [text, setText] = useState<String>("closed");


  useEffect(()=>{
    if(props.isOpen){
      setText("opened")
    }
    else{
      setText("closed")
    }


  }, [props.isOpen])



  const doorStyles: React.CSSProperties = {
    width: "40px",
    height: "60px",
    transition: "transform 0.5s ease",
    transformOrigin: "right center",
    perspective: "1000px",
    position: "relative",
  };

  const doorFrameStyles: React.CSSProperties = {
    width: "100%",
    height: "100%",
    border: "2px solid black",
    boxSizing: "border-box",
    backgroundColor: !props.isOpen ? "green" : "red",
    position: "relative",
    transformStyle: "preserve-3d",
    borderRadius: "5px",
    overflow: "hidden",
  };

  const knobStyles: React.CSSProperties = {
    width: "8px",
    height: "8px",
    borderRadius: "50%",
    backgroundColor: "silver",
    position: "absolute",
    top: "50%",
    left: "3px",
    transform: "translateY(-50%)",
    zIndex: 1,
  };

  if (!props.isOpen) {
    doorStyles.transform = "rotateY(0)";
  } else {
    doorStyles.transform = "rotateY(-70deg)";
  }

  return (
    <div className="flex flex-col justify-between text-center items-center w-full h-full p-4">
      <div>
        <div style={{ perspective: "1000px" }}>
          <div style={doorStyles}>
            <div style={doorFrameStyles}>
              <div style={knobStyles}></div>
            </div>
          </div>
        </div>
      </div>
      <p  className="text-xs sm:text-base lg:text-xl xl:text2xl">{text}</p>
    </div>
  );
}

export default IconDoor;

