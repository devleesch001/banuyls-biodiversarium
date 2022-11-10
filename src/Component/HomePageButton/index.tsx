import React from 'react'
import Typography from '@mui/material/Typography';
import { Button } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { text } from 'node:stream/consumers';
import {Modal} from '@mui/material';
import Apropos from '../Apropos';
import {Logo} from '../'
import { Grid } from '@mui/material';


interface homePageButtonProps {
        onClickCommencer: () => void;
}

const HomePageButton: React.FC<homePageButtonProps> = ({
        onClickCommencer
}) => {
        return <Grid container spacing={1}>             
                     <video
            autoPlay
            loop
            muted
            style={{
                position: "absolute",
                width: "100%",
                left: "50%",
                top: "50%",
                height: "100%",
                objectFit: "cover",
                transform: "translate(-50%, -50%)",
                zIndex: -1
            }}
        >
            <source src={require('../../IMG-8758.mp4')} type="video/mp4"/>
        </video>
                <Logo/>
        <Button
                        style={{
                        position: 'absolute',
                        left: '50%',
                        top: '50%',
                        transform: 'translate(-50%, -50%)',
                        color:'white',
                        fontWeight:"bold" ,
                        fontSize: '30px',
                        fontFamily: 'italic',
                        backgroundColor: 'rgba(189,195,199,0.5)',
                        borderRadius:'10px' ,
                }}
                variant='outlined'
                onClick={onClickCommencer}
        >
                Commencer l'expérience
        </Button>
        </Grid>
}

export default HomePageButton;