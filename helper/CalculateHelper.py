# from numpy.lib.shape_base import split
import helper.ProcessHelper as ph
import helper.SqliteHelper as sh
from decimal import Decimal
import random
import helper.pytorch as pt
import matplotlib.pyplot as plt
import numpy as np
import helper.init as init
import helper.lxmlheper as lxmlheper

def replaceCount(begin=0, index=0, step=1, ai=0, col="SortData"):
    _db = sh.Connect(init.db_file)
    _data = _db.table('pl3').findAll()
    _pridata = [0] * 1000
    sumcount = 0
    if step < 0:
        index -= step
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
    _db = sh.Connect(init.db_file)
    _data = _db.table('pl3').findAll()
    ans = [0] * 4
    if step < 0:
        index -= step
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
    strans = ("0:3 占比 " + str(Decimal(ans[0] / abs(index - begin) * 100).quantize(Decimal("0.00"))).rjust(5) + "%" + ", 1:2 占比 " + str(Decimal(ans[1] / abs(index - begin) * 100).quantize(Decimal("0.00"))).rjust(5) + "%" + ", 2:1 占比 " + str(Decimal(ans[2] / abs(index - begin) * 100).quantize(Decimal("0.00"))).rjust(5) + "%" + ", 3:0 占比 " + str(Decimal(ans[3] / abs(index - begin) * 100).quantize(Decimal("0.00"))).rjust(5) + "%")
    _db.close()
    if ai == 0:
        return strans
    else:
        strans = [ans[0] / abs(index - begin) * 100, ans[1] / abs(index - begin) * 100, ans[2] / abs(index - begin) * 100, ans[3] / abs(index - begin) * 100]
        return strans

def CalSum(begin=0, index=0, step=1, ai=0):
    _db = sh.Connect(init.db_file)
    _data = _db.table('pl3').findAll()
    ans = [0] * 28
    if step < 0:
        index -= step
    for i in range(begin, index, step):
        ans[int(_data[i]["SumData"])] += 1
    _db.close()
    strAns = ""
    listAns = []
    if ai == 0:
        for i in range(28):
            strAns += str(i) + ": " + str(Decimal(ans[i] / abs(index - begin) * 100).quantize(Decimal("0.00"))) + "%  "
            if (i + 1) % 15 == 0:
                strAns += "\r\n"
                return strAns
    elif ai == 1:
        for i in range(28):
            listAns.append(Decimal(ans[i] / abs(index - begin) * 100).quantize(Decimal("0.00")))
        return listAns
    

def CalMuliteSum(begin=0, step=1, Mul=[]):
    # CalSum(begin, begin + 1000, 1, 0)
    listAns = []
    strAns = ""
    splitnum = 15 // len(Mul)
    for i in range(len(Mul)):
        listAns.append(CalSum(begin, begin + Mul[i], step, 1))
    for i in range(28):
        if i < 10:
            strAns += "0"
        strAns += str(i) + ": "
        for j in range(len(Mul)):
            strAns += str(listAns[j][i]).rjust(5) + "%  "
        strAns += "|"
        if (i + 1) % splitnum == 0:
            strAns += "\r\n"
    return strAns

def CalBSSaOES(begin, index, strChose="BSS"):
    _db = sh.Connect(init.db_file)
    _data = _db.table("pl3").findAll()
    ans = [0] * 8
    strans = ""
    for i in range(begin, index):
        ans[ph.DtoB(int(_data[i][strChose]))] += 1
    for i in range(8):
        # if i == 4:
        #     strans += '\r\n'
        strans += ph.BtoD(i) + "占比: " + str(Decimal(ans[i] / (index - begin) * 100).quantize(Decimal("0.00"))).rjust(5) + "%"
        if i != 7:
            strans += ", "
    return strans

def CalTS(begin=0, index=0):
    _db = sh.Connect(init.db_file)
    _data = _db.table('pl3').findAll()
    ans = [0] * 3
    for i in range(begin, index):
        if _data[i]['TS'] == 0:
            ans[0] += 1
        elif _data[i]['TS'] == 3:
            ans[1] += 1
        else:
            ans[2] += 1
    strans = ("豹子占比 " + str(Decimal(ans[0] / (index - begin) * 100).quantize(Decimal("0.00"))).rjust(5) + "%" + ", 组合3占比 " + str(Decimal(ans[1] / (index - begin) * 100).quantize(Decimal("0.00"))).rjust(5) + "%" + ", 组合6占比 " + str(Decimal(ans[2] / (index - begin) * 100).quantize(Decimal("0.00"))).rjust(5) + "%")
    _db.close()
    return strans

def smartCount():
    smartList = [27,35,37,38,45,47,56,57,58,67,78,126,129,136,138,156,167,236,238,239,249,256,259,267,269,346,347,348,349,356]
    _db = sh.Connect(init.db_file)
    _data = _db.table('pl3').findAll()
    sumcount = 0
    for i in range(len(_data)):
        if int(_data[i]['SortData']) in smartList:
            sumcount += 1
    _db.close()
    return round(sumcount / len(_data), 4) * 100

def CalCurrent(n):
    _db = sh.Connect(init.db_file)
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
            bssans[ph.DtoB(int(_data[i + 1]["BSS"]))] += 1
            oesans[ph.DtoB(int(_data[i + 1]["OES"]))] += 1
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
        strans += ph.BtoD(i) + "占比: " + str(Decimal(bssans[i] / sortcnt * 100).quantize(Decimal("0.00"))) + "%"
        if i != 7:
            strans += ", "   
    print(strans)
    strans = "按位奇偶比: "
    for i in range(8):
        strans += ph.BtoD(i) + "占比: " + str(Decimal(oesans[i] / sortcnt * 100).quantize(Decimal("0.00"))) + "%"
        if i != 7:
            strans += ", "   
    print(strans)    
    _db.close()

def CalMK(index=0):
    _db = sh.Connect(init.db_file)
    _data = _db.table('pl3').findAll()
    maxlength = len(_data)
    # if maxlength % 10 > 0:
    #     maxlength -= maxlength % 10
    maxlength = (maxlength // 10 * 10)
    mklist = []
    mkrlist = []
    for i in range(maxlength, 9 + index, -1):
        # mklist.append(replaceCount(i, i - 100, -1, 1, "OriData"))
        # items = CalBSaOE(i, i - 100, -1, "BS", 1)
        # for item in items:
        #     mklist.append(item)
        tmplist = []
        for j in range(10):
            tmplist.append(int(_data[i - j]["OriData"][0]))
        mklist.append(tmplist)
        mkrlist.append(int(_data[i - 10]["OriData"][0]))
    # print(ah.mk_test(mklist))
    pt.TorchCal(mklist, mkrlist, maxlength, 10)
    mkplist = []
    for i in range(9, -1, -1):
        mkplist.append(int(_data[i + index]["OriData"][0]))
    pt.TorchProcess(mkplist, 10)
    _db.close()

def CalMKP(index=0):
    _db = sh.Connect(init.db_file)
    _data = _db.table('pl3').findAll()
    maxlength = len(_data)
    maxlength = (maxlength // 10 * 10)
    mkplist = []
    for i in range(9, -1, -1):
        mkplist.append(int(_data[i + index]["OriData"][0]))
    pt.TorchProcess(mkplist, 10)
    _db.close()  

def CreateIMG(begin=0, index=0, step=1, strChose="BS", ai=0):
    _db = sh.Connect(init.db_file)
    _data = _db.table('pl3').findAll()
    if step < 0:
        index -= step
    x = np.array([np.datetime64("1900-01-01")] * abs(index - begin))
    y = np.array([0] * abs(index - begin))
    for i in range(begin, index, step):
        # ans[int(_data[i]["SumData"])] += 1
        # x = np.append(x, np.datetime64(_data[i]["OriDate"]))
        # y = np.append(y, int(_data[i]["SumData"]))
        x[i] = np.datetime64(_data[i]["OriDate"])
        y[i] = int(_data[i]["SumData"])
    _db.close()
    # plt.scatter(x, y, s=1)
    plt.plot(x, y)
    plt.grid()
    plt.show()

def CalLimit(begin=0, index=0, step=1, MaxN=20, MinN=10, select=-1, ai=0):
    _db = sh.Connect(init.db_file)
    _data = _db.table('pl3').findAll()
    if step < 0:
        index -= step
    ans = np.zeros([28, 5])
    ansdetial = np.zeros([28, 28])   
    # totalB = 0
    # totalS = 0
    for i in range(begin, index - 1, step):
        # if int(_data[i]["SumData"]) == 8:
        #     print(int(_data[i]["SumData"]), int(_data[i + 1]["SumData"]))
        ans[int(_data[i]["SumData"]), 0] += 1
        if int(_data[i]["SumData"]) > int(_data[i + 1]["SumData"]):
            ans[int(_data[i]["SumData"]), 1] += 1
        elif int(_data[i]["SumData"]) == int(_data[i + 1]["SumData"]):
            ans[int(_data[i]["SumData"]), 2] += 1
        elif int(_data[i]["SumData"]) < int(_data[i + 1]["SumData"]):
            ans[int(_data[i]["SumData"]), 3] += 1
        ansdetial[int(_data[i]["SumData"]), int(_data[i + 1]["SumData"])] += 1
        # if int(_data[i]["SumData"]) >= 20:
        #     totalB += 1 
        #     if int(_data[i + 1]["SumData"]) < int(_data[i]["SumData"]):
        #         ans[1] += 1
        # elif int(_data[i]["SumData"]) <= 10:
        #     totalS += 1
        #     if int(_data[i + 1]["SumData"]) > int(_data[i]["SumData"]):
        #         ans[0] += 1
    _db.close()
    # print("极大数封顶概率：" + str(Decimal(ans[1] / totalB * 100).quantize(Decimal("0.00"))) + "%," + "极小数封底概率：" + str(Decimal(ans[0] / totalS * 100).quantize(Decimal("0.00"))) + "%")
    if select == -1:
        for i in range(0, 28):
            print(str(i) + ":  " + str(Decimal(ans[i, 1] / ans[i, 0] * 100).quantize(Decimal("0.00"))) + "%, " + str(Decimal(ans[i, 2] / ans[i, 0] * 100).quantize(Decimal("0.00"))) + "%, " + str(Decimal(ans[i, 3] / ans[i, 0] * 100).quantize(Decimal("0.00"))) + "% ")
    else:
        if ai == 0:
            i = select
            print(str(i) + ":  " + str(Decimal(ans[i, 1] / ans[i, 0] * 100).quantize(Decimal("0.00"))) + "%, " + str(Decimal(ans[i, 2] / ans[i, 0] * 100).quantize(Decimal("0.00"))) + "%, " + str(Decimal(ans[i, 3] / ans[i, 0] * 100).quantize(Decimal("0.00"))) + "% ")
            print("当前和值为" + str(select) + ",回归概率为：")
            for i in range(0, 28):
                print(str(i) + ":  " + str(Decimal(ansdetial[select, i] / ans[select, 0] * 100).quantize(Decimal("0.00"))) + "% ")
        else:
            listAns = []
            for i in range(0, 28):
                listAns.append(ansdetial[select, i] / ans[select, 0] * 100)
            return listAns

def Guess(begin=0, index=-1, replace=10, bsp=[0,1,2], oep=[1,2], tsp=[2], sorted=0, st=[], nd=[], rd=[], bss=[], oes=[], sums=[14,15]):
    _db = sh.Connect(init.db_file)
    _used = _db.table('pl3').findAll()
    # 容错处理
    for i in range(len(tsp)):
        if tsp[i] == 3:
            tsp[i] = 1
        elif tsp[i] == 6:
            tsp[i] = 2
    if index == -1:
        index = len(_used)
    _data = [0] * 1000
    for i in range(1000):
        if ph.getSumNum(i) not in sums:
            _data[i] = -1
        else:
            _data[i] += 1
    for i in range(begin, index):
        if replace > 0 and _data[int(_used[i]["OriData"])] >= 1: 
            tmpran = random.randint(0, 100)
            if tmpran <= replace:
                _data[int(_used[i]["OriData"])] = -1 
        elif replace == 0 and _data[int(_used[i]["OriData"])] >= 1:
            _data[int(_used[i]["OriData"])] = -1
    for i in range(1000):
        if _data[i] >= 0:
            if sorted == 1:
                if(i // 100 > i // 10 % 10 or i // 10 % 10 > i % 10 or i // 100 > i % 10):
                    _data[i] = -1
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
                _data[i] = -1
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
                _data[i] = -1
                continue
            check = False
            for j in range(10):
                if tscnt[j] == 3 and 0 not in tsp:
                    check = True
                    _data[i] = -1
                    break
                if tscnt[j] == 2 and 1 not in tsp:
                    check = True
                    _data[i] = -1
                    break
            if (check is False and 2 not in tsp) or (1 not in tsp and i < 10):
                _data[i] = -1
    strans = ""
    cnt = 0
    cnts = [0] * 3
    scnt = [0] * 10
    stranss = [""] * 3
    for i in range(1000):
        if _data[i] >= 0:
            scnt[i // 100] += 1
            scnt[i // 10 % 10] += 1
            scnt[i % 10] += 1
            strans += str(i) + " "
            if ph.intCheck36(i) == 0:
                stranss[0] += str(i) + " "
                cnts[0] += 1
            elif ph.intCheck36(i) == 1:
                stranss[1] += str(i) + " "
                cnts[1] += 1
            elif ph.intCheck36(i) == 2:
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
    _db.close()
    # if sorted == 1:
    #     scnt.sort(reverse=True)
    #     for i in range(10):
    #         if scnt[i] > 0:
    #             print(str(i) + " " + str(scnt[i]) + " " + str(Decimal((scnt[i] / (cnt * 3)) * 100).quantize(Decimal("0.00"))) + "%")

def crawler():
    _db = sh.Connect(init.db_file)
    _db.table('pl3').delete()
    _db.table("sqlite_sequence").save({"seq": '0'})
    _db.close()
    lxmlheper.parse_one_page(lxmlheper.get_page(3))

def getLastSumData(select=0):
    _db = sh.Connect(init.db_file)
    _data = _db.table('pl3').findAll()
    _db.close()
    return _data[select]["SumData"]

def getLastID():
    _db = sh.Connect(init.db_file)
    _data = _db.table('pl3').findAll()
    _db.close()
    return len(_data)

def CalculateMuliteRate():
    # _db = sh.Connect(init.db_file)
    # _data = _db.table('pl3').findAll()
    # replaceCount(begin=0, index=0, step=1, ai=0, col="SortData")
    # replaceCount(begin, begin + 100, 1, 0, "OriData")
    # ch.CalLimit(num, 1000, 1, 20, 10, ch.getLastSumData(num))
    RptRate = []
    SamplePropotion = [getLastID(), 5000, 1000, 500]
    for i in range(len(SamplePropotion)):
        # RptRate[i] = replaceCount(0, SamplePropotion[i], step=1, ai=1, col="OriData")
        RptRate.append(CalLimit(0, SamplePropotion[i], 1, 20, 10, getLastSumData(0), 1))
    # _db.close()
    return RptRate

def getSomething(begin=0, end=100, step=1, ai=0, col="SortData"):
    _db = sh.Connect(init.db_file)
    _data = _db.table('pl3').findAll()
    _db.close()
    listAns = []
    for i in range(begin, end, step):
        listAns.append([int(_data[i][col])])
    return listAns