import React from 'react'
import { useRef } from 'react';

interface camProps {

}

const onSelectFish = (sender: any) => {
        let canvas = document.querySelector('canvas');
        let video = document.querySelector('video');
        
        if (video && canvas) {
                let x = sender.pageX - video.offsetLeft;
                let y = sender.pageY - video.offsetTop;
                
                canvas.width = 100;
                canvas.height = 100;

                const ctx = canvas.getContext('2d');

                if (ctx && video) {
                        ctx.drawImage(video, x, y, 100, 100, 0, 0, 100, 100);
                        const dataUrl = canvas.toDataURL("image/png");
                        // send image to server
                        console.log(dataUrl);
                }
        }
};

const Cam: React.FC<camProps> = ({}) => {
        const playerRef = useRef() as any  ;
        return (
                
                   <>
                   <canvas id="result"></canvas>
                        <video crossOrigin="anonymous" src="http://localhost:8000/video"  controls={false} onClick={onSelectFish}
                        autoPlay={true} muted style={{objectFit: 'fill', backgroundColor: 'black' , width : '100%', height : '100%'}}
                        />
                   </>
        );
};

export default Cam;