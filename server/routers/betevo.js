const {Router} = require('express');
const {BetevoRecord} = require('../records/betevo.record');
const {pool} = require('../utils/db');

const BetevoRouter = Router();

BetevoRouter.get('/test', async (req, res) => {
  const betevoList = await BetevoRecord.listAll();

  res.send(betevoList);
});

module.exports = {
  BetevoRouter,
};
