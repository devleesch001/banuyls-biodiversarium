import React from 'react'
import { useState, useEffect } from 'react';
import axios from 'axios';
import ResultTable from '../Table';
import { Grid } from '@mui/material';
import { cameraChoiceEnum } from '../HomePageButton';
import TouchAppIcon from '@mui/icons-material/TouchApp';
import { config } from '../../config';

interface CamProps {
        fishResult: {
                certainty: number,
                detection: string,
                s_name: string,
                s_type: string,
                family: string,
                description: string,
                position: { 
                        bottomright: { x: number, y: number },
                        topleft: { x: number, y: number }
                }
        }[];
        setFishResult(value: {
                certainty: number,
                detection: string,
                s_name: string,
                s_type: string,
                family: string,
                description: string,
                position: { 
                        bottomright: { x: number, y: number },
                        topleft: { x: number, y: number }
                }
        }[]): void;

        cameraChoice: cameraChoiceEnum;
}

type detection = {
        x: number;
        y: number;
        width: number;
        height: number;
        label: string;
        s_name: string,
        s_type: string,
        family: string,
        description: string
        percentage: number;
};
      
const Cam: React.FC<CamProps> = (Props) => {

        const [counter, setCounter] = useState(0);
        const { fishResult, setFishResult, cameraChoice } = Props;
        let originalImage = React.useRef('');
        let detectionsArray = React.useRef<detection[]>([]);
        let isAnalysing = React.useRef(false);
        let hasSelected = React.useRef(false);

        const [isImageLoading, setIsImageLoading] = useState<boolean>(false);

        const getVideo = () => {
                let video = document.querySelector('video');
                let img = document.getElementById('videoDisplay') as HTMLImageElement;
                if(video && img) {
                        let canvas = document.createElement('canvas');
                        canvas.width = img.width;
                        canvas.height = img.height;
        
                        const ctx = canvas.getContext('2d');
                        if(ctx) ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                        const imageB64 = canvas.toDataURL('image/jpeg');
                        originalImage.current = imageB64;
                }
        };
        
        const displayRectVideo = () => {                
                let newImageRect = originalImage.current;
                if(!isImageLoading && newImageRect !== '') {
                        let videoDisplay = document.getElementById('videoDisplay') as HTMLImageElement;
                        // ------                
                        // traitement sur l'image (requette axios)
                        let canvas = document.createElement('canvas');
                        let img = new Image();
                        if(canvas && img) {
                                canvas.width = videoDisplay.clientWidth;
                                canvas.height = videoDisplay.clientHeight;
                                let ctx = canvas.getContext('2d');
                                if(ctx) {
                                        img.onload = function() {
                                                if(ctx) {
                                                        ctx.drawImage(img, 0, 0);
                                                        if(!isAnalysing.current) {
                                                                isAnalysing.current = true;
                                                                axios.post(config.IA_API_TABLET_ANALYZE, {
                                                                        content: newImageRect
                                                                })
                                                                .then((res) => {
                                                                        let detections = res?.data?.data?.detections as {
                                                                                certainty: number,
                                                                                detection: string,
                                                                                position: { 
                                                                                        bottomright: { x: number, y: number },
                                                                                        topleft: { x: number, y: number }
                                                                                }
                                                                        }[];

                                                                        let fishes = res?.data?.data?.fishes;

                                                                        let detectionArray: detection[] = [];
                                                                        
                                                                        detections?.map(c => {
                                                                                let tmpDetection = {} as detection;
                                                                                tmpDetection.x = c.position.topleft.x;
                                                                                tmpDetection.y = c.position.topleft.y;
                                                                                tmpDetection.label = c.detection;
                                                                                tmpDetection.percentage = parseInt((c.certainty*100).toFixed(2));
                                                                                tmpDetection.width = c.position.bottomright.x - c.position.topleft.x;
                                                                                tmpDetection.height = c.position.bottomright.y - c.position.topleft.y;
                                                                                tmpDetection.s_name = fishes[tmpDetection.label]?.s_name;
                                                                                tmpDetection.s_type = fishes[tmpDetection.label]?.type;
                                                                                tmpDetection.family = fishes[tmpDetection.label]?.family;
                                                                                tmpDetection.description = fishes[tmpDetection.label]?.description?.fr;
                                                                                
                                                                                detectionArray.push(tmpDetection);
                                                                        });

                                                                        detectionsArray.current = detectionArray;
                                                                        isAnalysing.current = false;
                                                                })
                                                                .catch((err) => isAnalysing.current = false);
                                                        }

                                                        detectionsArray.current.map(rect => {
                                                                if(ctx) {
                                                                        ctx.fillStyle = "#FF0000";                                                                        
                                                                        ctx.rect(rect.x, rect.y, rect.width, rect.height);
                                                                        ctx.fillText(rect.label + ' ' + rect.percentage.toString() + '%', rect.x, rect.y+rect.height+10);
                                                                        ctx.stroke();
                                                                }
                                                        });
                                                        
                                                        if(videoDisplay) {
                                                                videoDisplay.onload = () => {
                                                                        setIsImageLoading(false);
                                                                }
                                                                videoDisplay.src = canvas.toDataURL('image/jpeg');
                                                                setIsImageLoading(true);
                                                        }
                                                        
                                                }
                                        };
                                        img.src = newImageRect;
                                        
                                        
                                }
                        }
                }                
        };

        useEffect(() => {
                const interval = setInterval(() => {
                        getVideo();
                        displayRectVideo();
                        setCounter((prevCounter) => prevCounter);
                }, 1);

                return () => clearInterval(interval);
        }, []);

        const onSelectFish = (sender: any) => {
                hasSelected.current = true; // pour indiquer qu'un poisson a été sélectionné

                let canvas = document.querySelector('canvas');
                let img = document.createElement('img');

                if (img && canvas && originalImage.current !== '') {
                        img.onload = () => {
                                if(canvas) {
                                        let x = sender.pageX - img.offsetLeft;
                                        let y = sender.pageY - img.offsetTop;
                        
                                        canvas.width = 200;
                                        canvas.height = 200;
                        
                                        const ctx = canvas.getContext('2d');
                        
                                        if (ctx && img) {                              
                                                ctx.drawImage(img, x-(canvas.width/2), y-(canvas.height/2), canvas.width, canvas.height, 0, 0, canvas.width, canvas.height);
                                                const dataUrl = canvas.toDataURL("image/png");
                                                const xMin = x-(canvas.width/2);
                                                const xMax = xMin + canvas.width;
                                                const yMin = y-(canvas.height/2);
                                                const yMax = yMin + canvas.height;
                                                
                                                let result: {
                                                        certainty: number,
                                                        detection: string,
                                                        s_name: string,
                                                        s_type: string,
                                                        family: string,
                                                        description: string,
                                                        position: { 
                                                                bottomright: { x: number, y: number },
                                                                topleft: { x: number, y: number }
                                                        }
                                                }[] = [];
                                                detectionsArray.current.map(detected => {
                                                        const xMinDetected = detected.x;
                                                        const xMaxDetected = xMinDetected + detected.width;
                                                        const yMinDetected = detected.y;
                                                        const yMaxDetected = yMinDetected + detected.height;
                                                        if((xMinDetected >= xMin && xMaxDetected <= xMax) &&
                                                           (yMinDetected >= yMin && yMaxDetected <= yMax)) {                                                   
                                                                result.push({ 
                                                                        certainty: detected.percentage/100,
                                                                        detection: detected.label,
                                                                        s_name: detected.s_name,
                                                                        s_type: detected.s_type,
                                                                        family: detected.family,
                                                                        description: detected.description,
                                                                        position: { 
                                                                                bottomright: { 
                                                                                        x: 0,
                                                                                        y: 0
                                                                                },
                                                                                topleft: { 
                                                                                        x: 0,
                                                                                        y: 0
                                                                                }
                                                                        }
                                                                });
                                                        }
                                                });

                                                if(result.length) setFishResult(result);
                                                else {
                                                        // send image to server
                                                        axios.post(config.IA_API_TABLET_ANALYZE, {
                                                                content: dataUrl
                                                        })
                                                        .then((res) => {
                                                                let result: {
                                                                        certainty: number,
                                                                        detection: string,
                                                                        s_name: string,
                                                                        s_type: string,
                                                                        family: string,
                                                                        description: string,
                                                                        position: { 
                                                                                bottomright: { x: number, y: number },
                                                                                topleft: { x: number, y: number }
                                                                        }
                                                                }[] = [];
                                                                let detections = res?.data?.data?.detections as {
                                                                        certainty: number,
                                                                        detection: string,
                                                                        position: { 
                                                                                bottomright: { x: number, y: number },
                                                                                topleft: { x: number, y: number }
                                                                        }
                                                                }[];

                                                                let fishes = res?.data?.data?.fishes;
                                                                detections.map(detected => {
                                                                        result.push({
                                                                                certainty: detected.certainty,
                                                                                detection: detected.detection,
                                                                                s_name: fishes[detected.detection]?.s_name,
                                                                                s_type: fishes[detected.detection]?.type,
                                                                                family: fishes[detected.detection]?.family,
                                                                                description: fishes[detected.detection]?.description?.fr,
                                                                                position: detected.position
                                                                        })
                                                                });

                                                                setFishResult(result);
                                                        })
                                                        .catch((err) => {
                                                                let fakeResult: {
                                                                        certainty: number,
                                                                        detection: string,
                                                                        position: { 
                                                                                bottomright: { x: number, y: number },
                                                                                topleft: { x: number, y: number }
                                                                        }
                                                                }[] = [
                                                                        {
                                                                                certainty: 0.6,
                                                                                detection: 'FISH_1',
                                                                                position: {
                                                                                        bottomright: { x: 0, y: 0 },
                                                                                        topleft: { x: 0, y: 0 }
                                                                                }
                                                                        },
                                                                        {
                                                                                certainty: 0.6,
                                                                                detection: 'FISH_2',
                                                                                position: {
                                                                                        bottomright: { x: 0, y: 0 },
                                                                                        topleft: { x: 0, y: 0 }
                                                                                }
                                                                        }
                                                                ];
        
                                                                setFishResult([]);
                                                        });
                                                }
                                        }     
                                }                                
                        };
                        img.src = originalImage.current;                       
                }
        };
        
        return (       
                   <Grid container spacing={1}>
                        <Grid item xs={12}>
                                <img id="videoDisplay" style={{backgroundColor: 'black', width: '100%', height: `${window.screen.width/3}px`}} onClick={onSelectFish}></img>
                        </Grid>

                        <Grid item xs={2} sm={2} md={2} lg={2} xl={2} id='canvas'>
                                <canvas style={{width: '100%'}}></canvas>
                        </Grid>

                        <Grid item xs={10} sm ={10} md={10} lg={10} xl={10} id='result'>
                                {hasSelected.current ? <ResultTable fishResult={fishResult}/> : <h2><i>Selectionnez un spécimen <TouchAppIcon/></i></h2>}
                        </Grid>

                        <Grid item xs={12}>
                                {/*{cameraChoice.toString()}*/}                            
                                <video 
                                        crossOrigin="anonymous"
                                        src={cameraChoice.toString()}
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