import requests
from requests.exceptions import RequestException
import csv
from bs4 import BeautifulSoup as bs
import helper.SqliteHelper as sh
from decimal import Decimal
import random
import math
import helper.AlgorithmHelper as ah

db_file = "database\pl3.db"

def write_to_file(item):
    file_name = "tempfile\PLS.csv"
    # "a"为追加模式（添加）
    # utf_8_sig格式导出csv不乱码
    with open(file_name, "a", encoding="utf_8_sig", newline="") as f:
        fieldnames = ["期号", "中奖号码", "开奖日期"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writerow(item)

def get_page():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        # url = "http://www.lottery.gov.cn/historykj/history_" + str(i) + ".jspx?_ltype=pls"
        url = "https://datachart.500.com/pls/history/inc/history.php?limit=15116&start=04001&end=99999"
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

def parse_one_page(get_html):
    _db = sh.Connect(db_file)
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

def getOE(_data):
    listData = list(_data)
    odd = 0
    even = 0
    for i in range(3):
        if int(listData[i]) % 2 == 0:
            even += 1
        else:
            odd += 1
    return str(odd) + ":" + str(even)

def getBS(_data):
    listData = list(_data)
    big = 0
    small = 0
    for i in range(3):
        if int(listData[i]) < 5:
            small += 1
        else:
            big += 1
    return str(big) + ":" + str(small)

def getSortData(_data):
    listData = list(_data)
    listData.sort()
    return "".join(listData)

def getSumData(_data):
    listData = list(_data)
    SumData = 0
    for i in range(3):
        SumData += int(listData[i])
    return SumData

def getMaxPage(get_html):
    data = bs(get_html, "lxml")
    ans = data.select("option ")
    return len(ans)

def crawler():
    _db = sh.Connect(db_file)
    _db.table('pl3').delete()
    _db.table("sqlite_sequence").save({"seq": '0'})
    _db.close()
    parse_one_page(get_page())

def replaceCount(begin=0, index=0, step=1, ai=0, col="SortData"):
    _db = sh.Connect(db_file)
    _data = _db.table('pl3').findAll()
    _pridata = [0] * 1000
    sumcount = 0
    if step == -1:
        index -= 1
    for i in range(begin, index, step):
        _pridata[int(_data[i][col])] += 1
    for i in range(1000):
        if _pridata[i] > 1:
            sumcount += _pridata[i]
    # for i in range(begin, index, step):
    #     print( _data[i]['SortData'],  _pridata[int(_data[i]['SortData'])])
    # print("---------------------------------------------")
    _db.close()
    # str(Decimal((scnt[i] / (cnt * 3)) * 100).quantize(Decimal("0.00")))
    if ai == 0:
        return str(Decimal((sumcount / abs(index - begin)) * 100).quantize(Decimal("0.00")))
    else:
        return sumcount / abs(index - begin) * 100
    

def CalBSaOE(begin=0, index=0, step=1, strChose="BS", ai=0):
    _db = sh.Connect(db_file)
    _data = _db.table('pl3').findAll()
    ans = [0] * 4
    if step == -1:
        index -= 1
    for i in range(begin, index, step):
        tmp = _data[i][strChose].split(':')
        # print(tmp)
        if tmp[0] == '0':
            ans[0] += 1
        elif tmp[0] == '1':
            ans[1] += 1
        elif tmp[0] == '2':
            ans[2] += 1
        else:   
            ans[3] += 1
    # Decimal(ans[0] / index * 100).quantize(Decimal("0.00"))
    strans = ("0:3 占比 " + str(Decimal(ans[0] / abs(index - begin) * 100).quantize(Decimal("0.00"))) + "%" + ", 1:2 占比 " + str(Decimal(ans[1] / abs(index - begin) * 100).quantize(Decimal("0.00"))) + "%" + ", 2:1 占比 " + str(Decimal(ans[2] / abs(index - begin) * 100).quantize(Decimal("0.00"))) + "%" + ", 3:0 占比 " + str(Decimal(ans[3] / abs(index - begin) * 100).quantize(Decimal("0.00"))) + "%")
    _db.close()
    if ai == 0:
        return strans
    else:
        strans = [ans[0] / abs(index - begin) * 100, ans[1] / abs(index - begin) * 100, ans[2] / abs(index - begin) * 100, ans[3] / abs(index - begin) * 100]
        return strans

def DtoB(num):
    i = 0
    ans = 0
    while num > 0:
        ans += (num % 10) * int(math.pow(2, i))
        i += 1
        num //= 10
    return ans

def BtoD(num):
    ans = ""
    while num > 0:
        ans = str(num % 2) + ans
        num //= 2
    if len(ans) == 0:
        ans = "000"
    elif len(ans) == 1:
        ans = "00" + ans
    elif len(ans) == 2:
        ans = "0" + ans
    return ans

def CalBSSaOES(begin, index, strChose="BSS"):
    _db = sh.Connect(db_file)
    _data = _db.table("pl3").findAll()
    ans = [0] * 8
    strans = ""
    for i in range(begin, index):
        ans[DtoB(int(_data[i][strChose]))] += 1
    for i in range(8):
        # if i == 4:
        #     strans += '\r\n'
        strans += BtoD(i) + "占比: " + str(Decimal(ans[i] / (index - begin) * 100).quantize(Decimal("0.00"))) + "%"
        if i != 7:
            strans += ", "
    return strans

def CalTS(begin=0, index=0):
    _db = sh.Connect(db_file)
    _data = _db.table('pl3').findAll()
    ans = [0] * 3
    for i in range(begin, index):
        if _data[i]['TS'] == 0:
            ans[0] += 1
        elif _data[i]['TS'] == 3:
            ans[1] += 1
        else:
            ans[2] += 1
    strans = ("豹子占比 " + str(Decimal(ans[0] / (index - begin) * 100).quantize(Decimal("0.00"))) + "%" + ", 组合3占比 " + str(Decimal(ans[1] / (index - begin) * 100).quantize(Decimal("0.00"))) + "%" + ", 组合6占比 " + str(Decimal(ans[2] / (index - begin) * 100).quantize(Decimal("0.00"))) + "%")
    _db.close()
    return strans

def smartCount():
    smartList = [27,35,37,38,45,47,56,57,58,67,78,126,129,136,138,156,167,236,238,239,249,256,259,267,269,346,347,348,349,356]
    _db = sh.Connect(db_file)
    _data = _db.table('pl3').findAll()
    sumcount = 0
    for i in range(len(_data)):
        if int(_data[i]['SortData']) in smartList:
            sumcount += 1
    _db.close()
    return round(sumcount / len(_data), 4) * 100

def CalCurrent(n):
    _db = sh.Connect(db_file)
    _data = _db.table('pl3').findAll()
    currentdata = _data[n]
    sortcnt = 0
    bsp = [0] * 4
    oep = [0] * 4
    tsp = [0] * 3
    bssans = [0] * 8
    oesans = [0] * 8
    for i in range(len(_data) - 1, n, -1):
        if int(_data[i]['SortData']) == int(currentdata['SortData']):
            sortcnt += 1
            bsp[int(_data[i + 1]['BS'].split(':')[0])] += 1
            oep[int(_data[i + 1]['OE'].split(':')[0])] += 1
            bssans[DtoB(int(_data[i + 1]["BSS"]))] += 1
            oesans[DtoB(int(_data[i + 1]["OES"]))] += 1
            if _data[i + 1]['TS'] == 0:
                tsp[0] += 1
            elif _data[i + 1]['TS'] == 3:
                tsp[1] += 1
            else:
                tsp[2] += 1
    print("第" + str(n + 1) + "期数值： " + currentdata["OriData"])
    print("上期数据为:" + str(_data[n + 1]['OriData']))
    print("往期共出现" + str(sortcnt) + "次，相邻期分析如下:")
    print("大小比： " + "0:3 占比 " + str(Decimal(bsp[0] / sortcnt * 100).quantize(Decimal("0.00"))) + "%" + ", 1:2 占比 " + str(Decimal(bsp[1] / sortcnt * 100).quantize(Decimal("0.00"))) + "%" + ", 2:1 占比 " + str(Decimal(bsp[2] / sortcnt * 100).quantize(Decimal("0.00"))) + "%" + ", 3:0 占比 " + str(Decimal(bsp[3] / sortcnt * 100).quantize(Decimal("0.00"))) + "%")
    print("奇偶比： " + "0:3 占比 " + str(Decimal(oep[0] / sortcnt * 100).quantize(Decimal("0.00"))) + "%" + ", 1:2 占比 " + str(Decimal(oep[1] / sortcnt * 100).quantize(Decimal("0.00"))) + "%" + ", 2:1 占比 " + str(Decimal(oep[2] / sortcnt * 100).quantize(Decimal("0.00"))) + "%" + ", 3:0 占比 " + str(Decimal(oep[3] / sortcnt * 100).quantize(Decimal("0.00"))) + "%")
    print("36比:" + "豹子占比 " + str(Decimal(tsp[0] / sortcnt * 100).quantize(Decimal("0.00"))) + "%" + ", 组合3占比 " + str(Decimal(tsp[1] / sortcnt * 100).quantize(Decimal("0.00"))) + "%" + ", 组合6占比 " + str(Decimal(tsp[2] / sortcnt * 100).quantize(Decimal("0.00"))) + "%")
    strans = "按位大小比: "
    for i in range(8):
        strans += BtoD(i) + "占比: " + str(Decimal(bssans[i] / sortcnt * 100).quantize(Decimal("0.00"))) + "%"
        if i != 7:
            strans += ", "   
    print(strans)
    strans = "按位奇偶比: "
    for i in range(8):
        strans += BtoD(i) + "占比: " + str(Decimal(oesans[i] / sortcnt * 100).quantize(Decimal("0.00"))) + "%"
        if i != 7:
            strans += ", "   
    print(strans)    
    _db.close()

def Guess(begin=0, index=-1, replace=10, bsp=[0,1,2], oep=[1,2], tsp=[2], sorted=0, st=[], nd=[], rd=[], bss=[], oes=[]):
    # 容错处理
    for i in range(len(tsp)):
        if tsp[i] == 3:
            tsp[i] = 1
        elif tsp[i] == 6:
            tsp[i] = 2
    _data = [1] * 1000
    if replace > 0:
        _db = sh.Connect(db_file)
        _used = _db.table('pl3').findAll()
        if index == -1:
            index = len(_used)
        for i in range(begin, index):
            if _data[int(_used[i]["OriData"])] == 1:
                tmpran = random.randint(0, 100)
                if tmpran <= replace:
                    _data[int(_used[i]["OriData"])] = 0
        _db.close()
    for i in range(1000):
        if _data[i] == 1:
            if sorted == 1:
                if(i // 100 > i // 10 % 10 or i // 10 % 10 > i % 10 or i // 100 > i % 10):
                    _data[i] = 0
                    continue
            num = i
            bscnt = 0
            oecnt = 0
            tscnt = [0] * 10
            first = num // 100
            second = num // 10 % 10
            third = num % 10
            bsscnt = ""
            oescnt = ""
            if first > 4:
                bsscnt += "1"
            else:
                bsscnt += "0"
            if second > 4:
                bsscnt += "1"
            else:
                bsscnt += "0"
            if third > 4:
                bsscnt += "1"
            else:
                bsscnt += "0"
            if first % 2 == 1:
                oescnt += "1"
            else:
                oescnt += "0"
            if second % 2 == 1:
                oescnt += "1"
            else:
                oescnt += "0"
            if third % 2 == 1:
                oescnt += "1"
            else:
                oescnt += "0"
            if first in st or second in nd or third in rd or bsscnt in bss or oescnt in oes:
                _data[i] = 0
                continue
            while num > 0:
                tmp = num % 10
                tscnt[tmp] += 1
                if tmp >= 5:
                    bscnt += 1
                if tmp % 2 == 1:
                    oecnt += 1
                num //= 10
            if bscnt not in bsp or oecnt not in oep:
                _data[i] = 0
                continue
            check = False
            for j in range(10):
                if tscnt[j] == 3 and 0 not in tsp:
                    check = True
                    _data[i] = 0
                    break
                if tscnt[j] == 2 and 1 not in tsp:
                    check = True
                    _data[i] = 0
                    break
            if (check is False and 2 not in tsp) or (1 not in tsp and i < 10):
                _data[i] = 0
    strans = ""
    cnt = 0
    cnts = [0] * 3
    scnt = [0] * 10
    stranss = [""] * 3
    for i in range(1000):
        if _data[i] == 1:
            scnt[i // 100] += 1
            scnt[i // 10 % 10] += 1
            scnt[i % 10] += 1
            strans += str(i) + " "
            if intCheck36(i) == 0:
                stranss[0] += str(i) + " "
                cnts[0] += 1
            elif intCheck36(i) == 1:
                stranss[1] += str(i) + " "
                cnts[1] += 1
            elif intCheck36(i) == 2:
                stranss[2] += str(i) + " "
                cnts[2] += 1
            cnt += 1
    if sorted == 1:
        for ci in tsp:
            strci = ""
            if ci == 0:
                strci = "豹子"
            elif ci == 1:
                strci = "组合3"
            elif ci == 2:
                strci = "组合6"
            print("组选" + strci + "推荐：")
            print("猜测结果共：" + str(cnts[ci]) + "个:")
            print(stranss[ci])
            
    else:     
        print("猜测结果共：" + str(cnt) + "个:")
        print(strans)
    # if sorted == 1:
    #     scnt.sort(reverse=True)
    #     for i in range(10):
    #         if scnt[i] > 0:
    #             print(str(i) + " " + str(scnt[i]) + " " + str(Decimal((scnt[i] / (cnt * 3)) * 100).quantize(Decimal("0.00"))) + "%")

def intCheck36(num):
    strnum = str(num)
    if len(strnum) == 1:
        strnum = "00" + strnum
    elif len(strnum) == 2:
        strnum = "0" + strnum
    ans = [0] * 10
    for i in range(3):
        ans[int(strnum[i])] += 1
    for i in range(3):
        if ans[i] == 3:
            return 0
        elif ans[i] == 2:
            return 1
    return 2

def ProcessData(begin=0):
    print("-------------------------------------------")
    print("近100期原始重复率:" + str(replaceCount(begin, begin + 100, 1, 0, "OriData")) + "%")
    print("近50期原始重复率:" + str(replaceCount(begin, begin + 50, 1, 0, "OriData")) + "%")
    print("近30期原始重复率:" + str(replaceCount(begin, begin + 30, 1, 0, "OriData")) + "%")
    print("近10期原始重复率:" + str(replaceCount(begin, begin + 10, 1, 0, "OriData")) + "%")
    print("")
    print("近100期有序重复率:" + str(replaceCount(begin, begin + 100)) + "%")
    print("近50期有序重复率:" + str(replaceCount(begin, begin + 50)) + "%")
    print("近30期有序重复率:" + str(replaceCount(begin, begin + 30)) + "%")
    print("近10期有序重复率:" + str(replaceCount(begin, begin + 10)) + "%")
    print("")
    # print("总智能重复率:" + str(smartCount()) + "%")
    # print("")
    # 大：小
    print("近100期大小比：" + str(CalBSaOE(begin, begin + 100, 1, "BS", 0)))
    print("近50期大小比：" + str(CalBSaOE(begin, begin + 50, 1, "BS", 0)))
    print("近30期大小比：" + str(CalBSaOE(begin, begin + 30, 1, "BS", 0)))
    print("近10期大小比：" + str(CalBSaOE(begin, begin + 10, 1, "BS", 0)))
    print("")
    print("近100期奇偶比：" + str(CalBSaOE(begin, begin + 100, 1, "BS", 0)))
    print("近50期奇偶比：" + str(CalBSaOE(begin, begin + 50, 1, "BS", 0)))
    print("近30期奇偶比：" + str(CalBSaOE(begin, begin + 30, 1, "BS", 0)))
    print("近10期奇偶比：" + str(CalBSaOE(begin, begin + 10, 1, "BS", 0)))
    print("")
    print("近100期36比：" + str(CalTS(begin, begin + 100)))
    print("近50期36比：" + str(CalTS(begin, begin + 50)))
    print("近30期36比：" + str(CalTS(begin, begin + 30)))
    print("近10期36比：" + str(CalTS(begin, begin + 10)))
    print("")
    # 0小 1大
    print("近100期按位大小比: " + str(CalBSSaOES(begin, begin + 100, "BSS")))
    print("近50期按位大小比: " + str(CalBSSaOES(begin, begin + 50, "BSS")))
    print("近30期按位大小比: " + str(CalBSSaOES(begin, begin + 30, "BSS")))
    print("近10期按位大小比: " + str(CalBSSaOES(begin, begin + 10, "BSS")))
    print("")
    print("近100期按位奇偶比: " + str(CalBSSaOES(begin, begin + 100, "OES")))
    print("近50期按位奇偶比: " + str(CalBSSaOES(begin, begin + 50, "OES")))
    print("近30期按位奇偶比: " + str(CalBSSaOES(begin, begin + 30, "OES")))
    print("近10期按位奇偶比: " + str(CalBSSaOES(begin, begin + 10, "OES")))
    print("")
    CalCurrent(begin)
    print("")
    # CalCurrent(2)
    # print("")
    # CalCurrent(3)
    print("")

def ForecastData(begin=0):
    print("-------------------------------------------")
    print("输入预测参数")
    # list(map(int, results))
    repeace = input("重复率：")
    bigsmall = list(map(int, input("大小比：").split(",")))
    oddeven = list(map(int, input("奇偶比：").split(",")))
    ts = list(map(int, input("36比：").split(",")))
    st = list(map(int, input("杀百位：").split(",")))
    nd = list(map(int, input("杀十位：").split(",")))
    rd = list(map(int, input("杀个位：").split(",")))
    bss = list(map(str, input("杀大小比: ").split(",")))
    oes = list(map(str, input("杀奇偶比: ").split(",")))
    print("预测直选结果：")
    Guess(begin, begin + 100, int(repeace), bigsmall, oddeven, ts, 0, st, nd, rd, bss, oes)
    print("预测组选结果：")
    Guess(begin, begin + 100, int(repeace), bigsmall, oddeven, ts, 1, st, nd, rd, bss, oes)

def CalMK():
    _db = sh.Connect(db_file)
    _data = _db.table('pl3').findAll()
    maxlength = len(_data)
    if maxlength % 10 > 0:
        maxlength -= maxlength % 100
    mklist = []
    for i in range(maxlength, 99, -100):
        # mklist.append(replaceCount(i, i - 100, -1, 1, "OriData"))
        items = CalBSaOE(i, i - 100, -1, "BS", 1)
        # for item in items:
        #     mklist.append(item)
        mklist.append(items[0])
    print(ah.mk_test(mklist))
    _db.close()

if __name__ == "__main__":
    while True:
        print("")
        select = input("请选择操作:\n1.爬取数据\n2.处理数据\n3.预测数据\n4.处理历史数据\n5.预测历史数据\n6.趋向性测试\n9.退出\n")
        if select == "1":
            crawler()
            print("-------------------------------------------")
        elif select == "2":
            ProcessData(0)
        elif select == "3":
            ForecastData(0)
        elif select == "4":
            num = int(input("输入预测期数："))
            ProcessData(num)
        elif select == "5":
            num = int(input("输入预测期数："))
            ForecastData(num)
        elif select == "6":
            CalMK()
        elif select == "9":
            break