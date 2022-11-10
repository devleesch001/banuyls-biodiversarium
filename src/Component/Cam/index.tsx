import React from 'react'
import Webcam from 'react-webcam';
import node from 'node:stream/consumers';
import rxjs, { from } from 'rxjs';
import stream from 'node:stream';
import ReactDOM from 'react-dom';
import ReactHlsPlayer from 'react-hls-player';
import playerRef from 'react-hls-player';
import { useRef } from 'react';
import { width } from '@mui/system';
import html2canvas from 'html2canvas';


interface camProps {

}

const TempImage = window.Image
const Image = function() {
        const img = new TempImage()
        img.crossOrigin = 'anonymous'
        return img
 }
const onSelectFish = (sender: any) => {
        let canvas = document.querySelector('canvas');
        let video = document.querySelector('video');

        if (video) {
                video.crossOrigin = "anonymous";
        }
        

        if (video && canvas) {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;

                const ctx = canvas.getContext('2d');

                if (ctx && video) {
                        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                        html2canvas(canvas).then(function(canvas) {
                                console.log(canvas.toDataURL("image/jpg"));
                        });
                }
        }
}

const screenShot = () => {
        let canvas = document.querySelector('canvas');

        if(canvas) {
                const dataURL = canvas.toDataURL('image/png');
                console.log(dataURL);
                
        }
}

const Cam: React.FC<camProps> = ({}) => {
        const playerRef = useRef() as any  ;
        return (
                
                   <>                
                        <video  src="http://10.3.3.61:8080/stream.ogg"  controls={false} onClick={onSelectFish}
                        autoPlay={true} muted style={{backgroundColor: 'black' , width : '100%', height : '100%'}}/>
                        <canvas id="output" width="160" height="96"></canvas>
                        <button onClick={screenShot}>Capture</button>
                   </>
        );
}
export default Cam;