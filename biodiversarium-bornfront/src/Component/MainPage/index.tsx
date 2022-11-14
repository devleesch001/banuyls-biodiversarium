import React, { useState } from 'react'
import { Grid } from '@mui/material';
import { Cam, MoreInfoButton, Logo, Description, HomePageButton } from '../'
import { Opacity } from '@mui/icons-material';

interface mainPageProps {

}

const MainPage: React.FC<mainPageProps> = ({ }) => {

    const [isHomePage, setIsHomePage] = useState(true);
    const onClickCommencer = () => {
        setIsHomePage(false);
    }

    const fishResultHandler = (value: {
        id: number,
        scientific_name: string,
        name: string,
        family: string,
        description: { fr: string },
        s_type: string,
    }[]): void => {
        fishResultHandler(value);
    };

    return <Grid container spacing={1}>

        {isHomePage ?
     
            <Grid item xs={12}>
                <HomePageButton 
                    onClickCommencer={onClickCommencer}
                    
                />

            </Grid>
            :
            <>
                
                <Grid item xs={10}
                    style={{ borderBottom: '2px solid whitesmoke', height: '120px' }}>
                    
                    <Logo />
                </Grid>

                <Grid item xs={2}
                    style={{ borderBottom: '2px solid whitesmoke', height: '120px',backgroundColor:"rgba(228, 233, 237,0.5)" }}>
                    <MoreInfoButton />
                </Grid>

                <Grid item xs={8}
                style={{backgroundColor:"rgba(228, 233, 237,0.5)" }}>
                    <Cam
                    fishResult={[
                        {
                                id: 1,
                                scientific_name: 'scientific_name',
                                name: 'poisson 1',
                                family: 'family',
                                description: {
                                    fr: 'DESCRIPTION'
                                },
                                s_type: 'string'
                        },
                        {
                            id: 2,
                            scientific_name: 'scientific_name',
                            name: 'poisson 2',
                            family: 'family',
                            description: {
                                fr: 'DESCRIPTION'
                            },
                            s_type: 'string'
                        }
                    ]}
                    setFishResult={fishResultHandler}
                    />
                </Grid>

                <Grid item xs={4} style={{backgroundColor:"rgba(228, 233, 237,0.5)" }}>
                    <Description />
                </Grid>
                
            </>
        }
    </Grid>
    
}

export default MainPage