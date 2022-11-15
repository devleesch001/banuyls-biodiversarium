import React from 'react'
import { useRef, useState, useEffect } from 'react';
import axios from 'axios';
import ResultTable from '../Table';

interface CamProps {
        fishResult: {
                id: number,
                scientific_name: string,
                name: string,
                family: string,
                description: { fr: string },
                s_type: string,
        }[];
        setFishResult(value: {
                id: number,
                scientific_name: string,
                name: string,
                family: string,
                description: { fr: string },
                s_type: string,
        }[]): void;
}

const Cam: React.FC<CamProps> = (Props) => {

        const [counter, setCounter] = useState(0);
        const { fishResult, setFishResult } = Props;

        const displayVideo = () => {
                let video = document.querySelector('video');
                let img = document.getElementById('videoDisplay') as HTMLImageElement;
                if(video && img) {
                        let canvas = document.createElement('canvas');
                        canvas.width = 800;
                        canvas.height = 600;
        
                        const ctx = canvas.getContext('2d');
                        if(ctx) ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                        img.src = canvas.toDataURL('image/jpeg');
                }
                else console.log('error');
        };
        
        useEffect(() => {
                const interval = setInterval(() => {
                        displayVideo();
                        setCounter((prevCounter) => prevCounter);
                }, 1);

                return () => clearInterval(interval);
        }, []);

        const onSelectFish = (sender: any) => {
                let canvas = document.querySelector('canvas');
                let img = document.getElementById('videoDisplay') as HTMLImageElement;
                
                if (img && canvas) {
                        let x = sender.pageX - img.offsetLeft;
                        let y = sender.pageY - img.offsetTop;
        
                        canvas.width = 100;
                        canvas.height = 100;
        
                        const ctx = canvas.getContext('2d');
        
                        if (ctx && img) {                              
                                ctx.drawImage(img, x-(canvas.width/2), y-(canvas.height/2), canvas.width, canvas.height, 0, 0, canvas.width, canvas.height);
                                const dataUrl = canvas.toDataURL("image/png");
                                // send image to server
                                axios.post('http://10.3.1.37:5000/api/tablet/analyze', {
                                        content: dataUrl
                                })
                                .then((res) => {        
                                        const result = (res?.data as unknown) as {
                                                id: number;
                                                scientific_name: string;
                                                name: string;
                                                family: string;
                                                description: {
                                                    fr: string;
                                                };
                                                s_type: string;
                                            }[];
                                                                
                                        setFishResult(result);
                                })
                                .catch((err) => console.log(err));
                        }
                } 
                
        };
        
        return (
                   <>
                        <div id="result">
                                <canvas></canvas>
                                <ResultTable fishResult={[]}/>
                                
                        </div>
                        <img id="videoDisplay" style={{backgroundColor: 'black', width: 800, height: 600}} onClick={onSelectFish} width={800}></img>
                        <video crossOrigin="anonymous" src="http://10.3.3.61:8000/video"  controls={false}
                        autoPlay={true} muted style={{visibility: 'hidden', backgroundColor: 'black' , width : '100%', height : '100%'}}
                        />
                   </>
        );
};

export default Cam;