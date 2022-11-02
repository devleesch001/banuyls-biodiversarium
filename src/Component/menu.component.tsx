import React from "react";

// bootstrap
import { Nav, Button } from 'react-bootstrap';

interface menuProps {

};

const Menu : React.FC<menuProps> = React.memo(({}) => {
    return <>
        <Nav className="navbar navbar-expand-lg navbar-light bg-light">
            <img style={{ width: "15rem" }} className="navbar-brand" src={require('../Assets/Logo-Biodiversarium.png')} alt="" />
            <Button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
            </Button>
            <div className="collapse navbar-collapse" id="navbarNav">
                <ul className="navbar-nav">
                    <li className="nav-item active">
                        <a className="nav-link" href="#">PAGE_1</a>
                    </li>
                    <li className="nav-item">
                        <a className="nav-link" href="#">PAGE_2</a>
                    </li>
                    <li className="nav-item">
                        <a className="nav-link" href="#">PAGE_3</a>
                    </li>
                </ul>
            </div>
        </Nav>
    </>;
});

export default Menu