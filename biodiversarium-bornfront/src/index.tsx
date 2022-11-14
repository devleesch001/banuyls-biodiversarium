import React , {useState} from 'react';
import ReactDOM from 'react-dom/client';
import reportWebVitals from './reportWebVitals';
import Webcam from "react-webcam";
import { useRef } from "react";
import { text } from 'node:stream/consumers';
import { Cam, MoreInfoButton, Logo, Description, MainPage } from './Component';
import { Grid } from '@mui/material';


const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);


root.render(
  <React.StrictMode>
    <MainPage />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
