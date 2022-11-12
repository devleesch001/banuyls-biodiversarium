// +--------------+
// | CLASSE PROXY |
// +--------------+
// Permet de diffuser un flux video avec les cors nécessaire.

require('dotenv').config();

const port = process.env.PORT || 8000
const url = process.env.URL || 'http://localhost:8080/stream.ogg'
const express = require('express');
const axios = require('axios');
const app = express();
const cors = require('cors');

app.use(cors());

app.get('/video', (req, res) => {
    axios.get(url, {
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
