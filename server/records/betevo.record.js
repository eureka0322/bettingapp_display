const {v4: uuid} = require('uuid');
const {pool} = require('../utils/db');

class BetevoRecord {
  constructor(obj) {
    if (!obj.category || !obj.team ) {
      throw new Error(
        'Betevo Data Validation Error'
      );
    }

    this.id = obj.id;
    this.category = obj.category;
    this.team = obj.team;
    this.spread_odd = obj.spread_odd;
    this.spread_standard = obj.spread_standard;
    this.money_line = obj.money_line;
    this.game_id = obj.game_id;
    this.game_date = obj.game_date;
    this.game_title = obj.game_title;
    this.game_datetime = obj.game_datetime;
  }

  static async listAll() {
    const currentTime = Date.now();
    const currentDate = new Date(currentTime);
    const tomorrowDate = new Date(currentTime);

    const year = currentDate.getFullYear();
    const month = currentDate.getMonth(); // Months are zero-based, so we add 1
    const day = currentDate.getDate();

    tomorrowDate.setDate(currentDate.getDate() + 1);

    const tomorrowYear = tomorrowDate.getFullYear();
    const tomorrowMonth = tomorrowDate.getMonth(); // Months are zero-based, so we add 1
    const tomorrowDay = tomorrowDate.getDate();

    const startTime = new Date(Date.UTC(year, month, day, 0, 0, 0, 0));
    const endTime = new Date(Date.UTC(tomorrowYear, tomorrowMonth, tomorrowDay, 0, 0, 0, 0));

    console.log(startTime, endTime);

    const [results] = await pool.execute(`SELECT id, category, team, spread_odd, spread_standard, money_line, game_id, game_date, game_title, game_datetime FROM tbl_betevo88 WHERE game_datetime>='${startTime.toISOString()}' AND game_datetime<='${endTime.toISOString()};'`);

    let listData = [];
    for(var i=0;i<results.length;i+=2){
      const data = {
        game_id: results[i].game_id,
        game_title: results[i].game_title,
        game_date: results[i].game_date,
        category: results[i].category,
        game_datetime: results[i].game_datetime,
        details: [
          {
            id: results[i].id,
            team_name: results[i].team,
            spread_odd: results[i].spread_odd,
            spread_standard: results[i].spread_standard,
            money_line: results[i].money_line
          },
          {
            id: results[i+1].id,
            team_name: results[i+1].team,
            spread_odd: results[i+1].spread_odd,
            spread_standard: results[i+1].spread_standard,
            money_line: results[i+1].money_line
          }
        ]
      };
      if((results[i].spread_odd !="" || results[i].spread_standard !="") && results[i].money_line!="")
        listData.push(data);
    }
    return listData;
  }
}

module.exports = {
  BetevoRecord,
};
