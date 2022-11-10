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
                    <Cam/>
                </Grid>

                <Grid item xs={4} style={{backgroundColor:"rgba(228, 233, 237,0.5)" }}>
                    <Description />
                </Grid>
                
            </>
        }
    </Grid>
    
}

export default MainPage