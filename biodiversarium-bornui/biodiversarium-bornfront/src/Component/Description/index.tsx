import React from 'react'
import Typography from '@mui/material/Typography';


interface DescriptionProps {

}

const Description: React.FC<DescriptionProps> = ({}) => {
        return (
            
            <Typography
            style={{
                    marginTop: 0,
                    marginRight: 10,
                    borderRadius: 25,
                    border : '10px solid white',
                    width: 350,    
                    textAlign: 'center',  
                    backgroundColor: 'white', 
                }}  
            >                            
                {"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla tellus tellus, sagittis at sapien eget, mattis iaculis odio. Integer luctus eros sit amet vulputate efficitur. Vestibulum quis facilisis velit. Fusce volutpat non lectus vel finibus. Cras vitae augue fermentum, sodales dolor in, blandit ipsum. Aliquam vulputate, augue non efficitur fringilla, turpis mauris venenatis ipsum, vel euismod nibh velit eleifend nisl. Morbi quis sem vitae ligula posuere ornare. Proin vestibulum est tempor, sagittis nibh vitae, posuere lectus. Praesent ac velit odio. Donec aliquam a risus sed scelerisque.  "}          
            </Typography>
        );
}
export default Description;