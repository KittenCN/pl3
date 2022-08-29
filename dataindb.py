# 导入需要用到的模块
import time
import requests
import json
import helper.SqliteHelper as sh
from tqdm import tqdm

if __name__ == "__main__":
    basecontent = ["leagueId", "allAwayTeam", "homeTeamId", "allHomeTeam", "awayTeamId", "a", "d", "h", "goalLine", "matchDate", "sectionsNo999", "winFlag"]
    db_file = r"D:/workstation/GitHub/pl3/database/football.db"
    days = ['0', '31', '28', '31', '30', '31', '30', '31', '31', '30', '31', '30', '31']
    months = ['0', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    _db = sh.Connect(db_file)
    pbar = tqdm(total=8, leave=False)
    for year in range(2015, 2023):
        subpar = tqdm(total=12, leave=True)
        pbar.update(1)
        for month in range(1, 13):   
            subpar.update(1)    
            url = 'https://webapi.sporttery.cn/gateway/jc/football/getMatchResultV1.qry?matchPage=1&matchBeginDate=' + str(year) + '-' + months[month] + '-01&matchEndDate=' + str(year) + '-' + months[month] + '-' + days[month] + '&leagueId=&pageSize=10000&pageNo=1&isFix=0&pcOrWap=1'
            # requests模块会自动解码来自服务器的内容，可以使用res.encoding来查看编码
            res = requests.get(url) 
            results = json.loads(res.text)['value']['matchResult']
            # print(results[0]['a'])
            data = []
            for i in range(len(results)):
                _data = {}
                for item in basecontent:     
                    if item != 'matchDate':  
                        _data[item] = results[i][item]
                    else:
                        _date_list = results[i][item].split('-')
                        _date = int(_date_list[0] + _date_list[1] + _date_list[2])
                        _data[item] = _date
                data.append(_data)
            _db.table('oridata').data(data).add()
            time.sleep(0.5)
        subpar.close()
    pbar.close()
    _db.close()