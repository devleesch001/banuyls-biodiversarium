import React from 'react'
import { useRef } from 'react';
import html2canvas from 'html2canvas';

interface camProps {

}

const onSelectFish = (sender: any) => {
        let canvas = document.createElement('canvas');
        let video = document.querySelector('video');        

        if (video && canvas) {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;

                const ctx = canvas.getContext('2d');

                if (ctx && video) {
                        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                        console.log(canvas.toDataURL("image/png"));
                }
        }
};

const Cam: React.FC<camProps> = ({}) => {
        const playerRef = useRef() as any  ;
        return (
                
                   <>
                        <video crossOrigin="anonymous" src="http://localhost:8000/video"  controls={false} onClick={onSelectFish}
                        autoPlay={true} muted style={{backgroundColor: 'black' , width : '100%', height : '100%'}}
                        />
                   </>
        );
};

export default Cam;