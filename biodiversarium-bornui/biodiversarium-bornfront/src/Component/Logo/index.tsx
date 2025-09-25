import React from 'react'
import { Grid } from '@mui/material';
import { MoreInfoButton } from '../';

interface logoProps {

}

const Logo: React.FC<logoProps> = ({}) => {
        return (
            <>
                <Grid container spacing={2}>
                    <Grid item xs={11} md={11}>
                        <img src={require('./Logo-Biodiversarium.png')} alt="No Found" 
                            style={{marginLeft: "5",  width: '30%'}}/>             
                        <img/>
                    </Grid>
                    
                    <Grid item xs={1}  md={1} justifyContent="center">
                        <MoreInfoButton/>
                    </Grid>
                </Grid>
            </>
        );
}

export default Logo;