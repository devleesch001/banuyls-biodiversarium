import React, { useState } from 'react'
import { Grid } from '@mui/material';
import { Cam, Logo, Description, HomePageButton } from '../'
import { cameraChoiceEnum } from '../HomePageButton';

interface mainPageProps {
}

const MainPage: React.FC<mainPageProps> = ({ }) => {

    const [isHomePage, setIsHomePage] = useState(true);
    const [fishResult, setFishResult] = useState<{
        detections: {
            certainty: number,
            detection: string,
            position: {
                bottomright: {
                    x: number,
                    y: number
                },
                topleft: {
                    x: number,
                    y: number
                }
            }
        }[],
        fishes: any
    }>({ detections: [], fishes: {} });
    

    const onClickCommencer = () => {
        setIsHomePage(false);
    }

    const fishResultHandler = (value: {
        detections: {
            certainty: number,
            detection: string,
            position: {
                bottomright: {
                    x: number,
                    y: number
                },
                topleft: {
                    x: number,
                    y: number
                }
            }
        }[],
        fishes: any
    }): void => {
        setFishResult(value);
    };

    const [cameraChoice, setCameraChoice] = useState<cameraChoiceEnum>(cameraChoiceEnum.OUT);

    const cameraChoiceHandler = (value: cameraChoiceEnum) => {
        setCameraChoice(value);
    };

    return <Grid container spacing={1}>

        {isHomePage ?
     
            <Grid item xs={12}>
                <HomePageButton onCameraChoice={cameraChoiceHandler} onClickCommencer={onClickCommencer} />
            </Grid>
            :
            <>                
                {/*<Grid item xs={12}
                    style={{ borderBottom: '2px solid whitesmoke', height: '120px' }}>                    
                    <Logo />
                </Grid>*/}

                <Grid item xs={12}
                style={{backgroundColor:"rgba(228, 233, 237,0.5)" }}>
                    <Cam
                    cameraChoice={cameraChoice}
                    fishResult={fishResult}
                    setFishResult={fishResultHandler}
                    />
                </Grid>            
            </>
        }
    </Grid>
    
}

export default MainPage