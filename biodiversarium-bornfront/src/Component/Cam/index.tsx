import React from 'react'
import { useRef, useState, useEffect } from 'react';
import axios from 'axios';
import ResultTable from '../Table';
import { Grid } from '@mui/material';

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
                                axios.post('', {//http://10.3.1.37:5000/api/tablet/analyze
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
                   <Grid container spacing={1}>
                        <Grid item xs={12}>
                                <img id="videoDisplay" style={{backgroundColor: 'black', width: '100%', height: `${window.screen.width/3}px`}} onClick={onSelectFish}></img>
                        </Grid>


                        <Grid item xs={2} sm={2} md={2} lg={2} xl={2} id='canvas'>
                                <canvas></canvas>
                        </Grid>

                        <Grid item xs={10} sm ={10} md={10} lg={10} xl={10} id='result'>
                                <ResultTable fishResult={[]}/>
                        </Grid>

                        <Grid item xs={12}>                                
                                <video 
                                        crossOrigin="anonymous"
                                        src="https://upload.wikimedia.org/wikipedia/commons/transcoded/c/c0/Big_Buck_Bunny_4K.webm/Big_Buck_Bunny_4K.webm.720p.webm"
                                        controls={false}
                                        autoPlay={true}
                                        muted
                                        style={{backgroundColor: 'black' , width : '1px', height : '1px'}}
                                        />
                        </Grid>
                   </Grid>
        );
};

export default Cam;