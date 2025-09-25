import React from 'react'
import Modal from '@mui/material/Modal';
import { Box } from '@mui/material';


interface ApropoProps {
    isVisible: boolean;
    onClose : any 
}

const Apropos: React.FC<ApropoProps> = ({
    isVisible , onClose 
}) => {

    const style = {
        position: 'absolute' as 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 400,
        bgcolor: 'white',
        border: '2px solid #000',
        borderRadius: 5,
        boxShadow: 24,
        p: 4,
      };

        return (
                <Modal
                onClose={onClose}
                open={isVisible}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
                >
                    <Box sx={style}>
                        <h2 id="modal-modal-title"  style={{textAlign: "center" , color:'black'}}>
                            À propos de Biodiversarium </h2>
                        <p id="modal-modal-description" style={{textAlign: "center" , color:'black'}}> 
                        Le Biodiversarium est constitué de deux sites complémentaires, l’Aquarium et le Jardin Méditerranéen du Mas de la Serre, associés pour présenter la biodiversité terrestre et marine des Pyrénées-Orientales, au travers d’une vision scientifique adaptée au plus grand nombre. À la fois centre de culture scientifique, écomusée et aquarium pédagogique, le Biodiversarium constitue, en tant que service de médiation scientifique de l’Observatoire Océanologique de Banyuls-sur-Mer, un lieu d’échanges entre le public et le monde de la recherche.
                        </p>
                </Box>
                </Modal>
        );
}

export default Apropos;