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
    const [results] = await pool.execute('SELECT id, category, team, spread_odd, spread_standard, money_line, game_id, game_date, game_title FROM `tbl_betevo88`');
    let listData = [];
    for(var i=0;i<results.length;i+=2){
      const data = {
        game_id: results[i].game_id,
        game_title: results[i].game_title,
        game_date: results[i].game_date,
        category: results[i].category,
        details: [
          {
            team_name: results[i].team,
            spread_odd: results[i].spread_odd,
            spread_standard: results[i].spread_standard,
            money_line: results[i].money_line
          },
          {
            team_name: results[i+1].team,
            spread_odd: results[i+1].spread_odd,
            spread_standard: results[i+1].spread_standard,
            money_line: results[i+1].money_line
          }
        ]
      };
      listData.push(data);
    }
    return listData;//results.map((obj) => new BetevoRecord(obj));
  }
}

module.exports = {
  BetevoRecord,
};
