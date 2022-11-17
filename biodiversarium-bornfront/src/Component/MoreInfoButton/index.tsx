import React from 'react'
import Typography from '@mui/material/Typography';
import { Button } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { text } from 'node:stream/consumers';
import {Modal} from '@mui/material';
import Apropos from '../Apropos';


interface moreInfoButtonProps {

}

const MoreInfoButton: React.FC<moreInfoButtonProps> = ({}) => {
        const [isShowModal , setIsShowModal] = React.useState(false);

        const handleClickButton = () => {
                setIsShowModal(true);
        
        }

        return <> <Button onClick={handleClickButton} 
        variant="outlined"
        style={{
                marginTop: 50,
                marginLeft: 30,
                //borderRadius: 25,
                color:'white',
                backgroundColor:'rgba(173,216,230,0.5)',
        }}
       
        > <AddIcon/> </Button> 
        <Apropos
                onClose={() => setIsShowModal(false)}
                isVisible={isShowModal}
        />
        </>
        
}
export default MoreInfoButton;