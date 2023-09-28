const express = require('express');
const cors = require('cors');
const {spawn} = require('child_process')
const {BetevoRouter} = require('./routers/betevo');
require('./utils/db');

const app = express();

app.use(cors());
app.use(express.json());

app.use('/', BetevoRouter);



// setInterval(() => {
//   const python = spawn("python", ["scrape_test.py"]);
//   console.log("start");
//   python.stdout.on('data', function (data) {
//     console.log('Pipe data from python script ...');
//     dataToSend = data.toString();
//    });
//    python.on('close', (code) => {
//     console.log(`child process close all stdio with code ${code}`);
//    });
     
// }, 3600*1000*24)
const PORT = process.env.PORT || 80;
app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});
