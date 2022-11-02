import React from "react";
import Webcam from "react-webcam";

interface cameraProps {

}

const WebcamComponent = () => <Webcam />;

const Camera : React.FC<cameraProps> = React.memo(({}) => {
    return <>
        <Webcam />
    </>;
});

export default Camera