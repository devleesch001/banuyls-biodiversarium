import React from 'react'



interface logoProps {

}

const Logo: React.FC<logoProps> = ({}) => {
        return (
            <>
                <img src={require('./Logo-Biodiversarium.png')} alt="No Found" 
                    style={{marginLeft: "5",  width: 300, height: 100}}/>             
                <img/>
            </>
        );
}

export default Logo;