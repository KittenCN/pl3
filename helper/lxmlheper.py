import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup as bs
import helper.SqliteHelper as sh
import helper.init as init

def get_page(pl=3):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        # url = "http://www.lottery.gov.cn/historykj/history_" + str(i) + ".jspx?_ltype=pls"
        if pl == 3:
            url = "https://datachart.500.com/pls/history/inc/history.php?limit=15116&start=04001&end=99999"
        else:
            url = "https://datachart.500.com/plw/history/inc/history.php?limit=15116&start=04001&end=99999"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.text
        else:
            print("return code is %s" % (str(response.status_code)))
            return None

    except RequestException:
        print("访问异常")

def parse_html(html):
    soup = bs(html, 'lxml')  # 创建网页解析器对象
    i = 0
    #查找网页里的tr标签,从第4个tr读到倒数第2个tr,因为通过对网页分析,前三个和最后一个tr没用
    for item in soup.select('tr')[3:-1]:  # 把查到的tr组成一个列表,item是列表指针,for每循环一次,item就选下一个tr,读完列表本循环结束,函数就结束,
        try:   # 不加try和except有的值是&nbsp,是网页里的空白键,会出错,加上调试命令忽略错误,后边统一处理             
            yield{  # yield作用是得到数据立即返回给调用函数,但不退出本循环本函数
                    'issue':item.select('td')[i].text,  # item查到的第0个td是开奖期号,写到time列
                    'WinningNumbers':item.select('td')[i + 1].text,  # 0+1个td是中奖号码
                    'sum':item.select('td')[i + 2].text,  # 总和数
                    'Totalsales':item.select('td')[i + 3].text,  # 总销售额
                    'Direct':item.select('td')[i + 4].text,  # 直选中奖注数
                    'Direct_bonus':item.select('td')[i + 5].text,  # 直选总奖金
                    'three_selection':item.select('td')[i + 6].text,  # 组选3中奖注数
                    'three_selection_bonus':item.select('td')[i + 7].text,  # 组选3总奖金
                    'six__selection':item.select('td')[i + 8].text,  # 组选6中奖数
                    'six__selection_bonus':item.select('td')[i + 9].text,  # 组选6总奖金
                    'time':item.select('td')[i + 10].text  # 开奖日期
                    #一组数据读完马上把值返回给调用函数,但没有退出本函数和本循环,
                    #调用函数得到数据,写到excel对象里,然后又回到这里,本次循环结束,开始下一次循环,item列表指针
            }
        except IndexError:
            pass             

def parse_one_page(get_html, pl=3):
    _db = sh.Connect(init.db_file)
    plsData = []
    if get_html is not None:
        print("正在写入...")
        for item in parse_html(get_html):
            pls = {}
            #下边的if是为了去掉列表里的乱码&nbsp,在网页里显示为空白,用0代替
            if item['three_selection'] == '&nbsp':
                item['three_selection'] = '0'
                item['three_selection_bonus'] = '0'
            else:
                item['six__selection'] = '0'
                item['six__selection_bonus'] = '0'
            if pl == 3:
                strData = "".join(item['WinningNumbers'].split())
                pls["OriIndex"] = item['issue']
                pls["OriDate"] = item['time']
                pls["OriData"] = strData
                pls["SortData"] = getSortData(strData)
                pls["SumData"] = getSumData(strData)
                pls["OE"] = getOE(strData)
                pls["BS"] = getBS(strData)
                pls["TS"] = getTS(strData)
                pls["BSS"] = getBSS(strData)
                pls["OES"] = getOES(strData)
            elif pl == 5:
                strData = "".join(item['WinningNumbers'].split())
                pls["Pl5OriData"] = strData
                pls["Pl5SortData"] = getSortData(strData)
                pls["Pl5SumData"] = getSumData(strData)
            plsData.append(pls)
    _db.table('pl3').data(plsData).add()
    _db.close()
    print("写入完成")

def getOES(_data):
    listData = list(_data)
    intans = 0
    strans = ""
    if int(listData[0]) % 2 == 1:
        intans += 100
    if int(listData[1]) % 2 == 1:
        intans += 10
    if int(listData[2]) % 2 == 1:
        intans += 1
    strans = str(intans)
    if len(strans) == 1:
        strans = "00" + strans
    elif len(strans) == 2:
        strans = "0" + strans
    return str(strans)   

def getBSS(_data):
    listData = list(_data)
    intans = 0
    strans = ""
    if int(listData[0]) > 4:
        intans += 100
    if int(listData[1]) > 4:
        intans += 10
    if int(listData[2]) > 4:
        intans += 1
    strans = str(intans)
    if len(strans) == 1:
        strans = "00" + strans
    elif len(strans) == 2:
        strans = "0" + strans
    return str(strans)  

def getTS(_data):
    listData = list(_data)
    listnum = [0] * 10
    for i in range(3):
        listnum[int(listData[i])] += 1
    for i in range(10):
        if listnum[i] == 3:
            return 0
        elif listnum[i] == 2:
            return 3
    return 6

def getOE(_data, index=3):
    listData = list(_data)
    odd = 0
    even = 0
    for i in range(index):
        if int(listData[i]) % 2 == 0:
            even += 1
        else:
            odd += 1
    return str(odd) + ":" + str(even)

def getBS(_data, index=3):
    listData = list(_data)
    big = 0
    small = 0
    for i in range(index):
        if int(listData[i]) < 5:
            small += 1
        else:
            big += 1
    return str(big) + ":" + str(small)

def getSortData(_data):
    listData = list(_data)
    listData.sort()
    return "".join(listData)

def getSumData(_data, index=3):
    listData = list(_data)
    SumData = 0
    for i in range(index):
        SumData += int(listData[i])
    return SumData

def getMaxPage(get_html):
    data = bs(get_html, "lxml")
    ans = data.select("option ")
    return len(ans)