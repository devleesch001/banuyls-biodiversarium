// +--------------+
// | CLASSE PROXY |
// +--------------+
// Permet de diffuser un flux video avec les cors nécessaire.

require('dotenv').config();

const port = process.env.SERVER_PORT
const inUrl = process.env.IN_URL
const outUrl = process.env.OUT_URL
const express = require('express');
const axios = require('axios');
const app = express();
const cors = require('cors');

app.use(cors());

app.get('/in', (req, res) => {
    axios.get(inUrl, {
        responseType: 'stream'
    })
    .then((stream) => {
        res.writeHead(stream.status, stream.headers);
        stream.data.pipe(res);
    })
    .catch(err => console.error(err.message));
});

app.get('/out', (req, res) => {
    axios.get(outUrl, {
        responseType: 'stream'
    })
    .then((stream) => {
        res.writeHead(stream.status, stream.headers);
        stream.data.pipe(res);
    })
    .catch(err => console.error(err.message));
});

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
