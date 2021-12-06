from decimal import Decimal
import numpy as np
import helper.CalculateHelper as ch
# import helper.ProcessHelper as ph

def ProcessData(begin=0):
    print("-------------------------------------------")
    # print("原始重复率:" + str(ch.replaceCount(begin, begin + ch.getLastID(), 1, 0, "OriData")) + "%")
    # print("近5000期原始重复率:" + str(ch.replaceCount(begin, begin + 5000, 1, 0, "OriData")) + "%")
    # print("近1000期原始重复率:" + str(ch.replaceCount(begin, begin + 1000, 1, 0, "OriData")) + "%")
    print("近100期原始重复率:" + str(ch.replaceCount(begin, begin + 100, 1, 0, "OriData")) + "%")
    print("近50期原始重复率:" + str(ch.replaceCount(begin, begin + 50, 1, 0, "OriData")) + "%")
    print("近30期原始重复率:" + str(ch.replaceCount(begin, begin + 30, 1, 0, "OriData")) + "%")
    print("近10期原始重复率:" + str(ch.replaceCount(begin, begin + 10, 1, 0, "OriData")) + "%")
    print("")
    # print("有序重复率:" + str(ch.replaceCount(begin, begin + ch.getLastID())) + "%")
    # print("近5000期有序重复率:" + str(ch.replaceCount(begin, begin + 5000)) + "%")
    # print("近1000期有序重复率:" + str(ch.replaceCount(begin, begin + 1000)) + "%")
    print("近100期有序重复率:" + str(ch.replaceCount(begin, begin + 100)) + "%")
    print("近50期有序重复率:" + str(ch.replaceCount(begin, begin + 50)) + "%")
    print("近30期有序重复率:" + str(ch.replaceCount(begin, begin + 30)) + "%")
    print("近10期有序重复率:" + str(ch.replaceCount(begin, begin + 10)) + "%")
    print("")
    # print("总智能重复率:" + str(smartCount()) + "%")
    # print("")
    # 大：小
    # print("大小比：" + str(ch.CalBSaOE(begin, begin + ch.getLastID(), 1, "BS", 0)))
    # print("近5000期大小比：" + str(ch.CalBSaOE(begin, begin + 5000, 1, "BS", 0)))
    print("近1000期大小比：" + str(ch.CalBSaOE(begin, begin + 1000, 1, "BS", 0)))
    print("近100期大小比：" + str(ch.CalBSaOE(begin, begin + 100, 1, "BS", 0)))
    print("近50期大小比：" + str(ch.CalBSaOE(begin, begin + 50, 1, "BS", 0)))
    print("近30期大小比：" + str(ch.CalBSaOE(begin, begin + 30, 1, "BS", 0)))
    print("近10期大小比：" + str(ch.CalBSaOE(begin, begin + 10, 1, "BS", 0)))
    print("")
    # print("奇偶比：" + str(ch.CalBSaOE(begin, begin + ch.getLastID(), 1, "BS", 0)))
    # print("近5000期奇偶比：" + str(ch.CalBSaOE(begin, begin + 5000, 1, "BS", 0)))
    print("近1000期奇偶比：" + str(ch.CalBSaOE(begin, begin + 1000, 1, "OE", 0)))
    print("近100期奇偶比：" + str(ch.CalBSaOE(begin, begin + 100, 1, "OE", 0)))
    print("近50期奇偶比：" + str(ch.CalBSaOE(begin, begin + 50, 1, "OE", 0)))
    print("近30期奇偶比：" + str(ch.CalBSaOE(begin, begin + 30, 1, "OE", 0)))
    print("近10期奇偶比：" + str(ch.CalBSaOE(begin, begin + 10, 1, "OE", 0)))
    print("")
    # print("36比：" + str(ch.CalTS(begin, begin + ch.getLastID())))
    # print("近5000期36比：" + str(ch.CalTS(begin, begin + 5000)))
    print("近1000期36比：" + str(ch.CalTS(begin, begin + 1000)))
    print("近100期36比：" + str(ch.CalTS(begin, begin + 100)))
    print("近50期36比：" + str(ch.CalTS(begin, begin + 50)))
    print("近30期36比：" + str(ch.CalTS(begin, begin + 30)))
    print("近10期36比：" + str(ch.CalTS(begin, begin + 10)))
    print("")
    # print("和值比：" + "\r\n" + str(ch.CalSum(begin, begin + ch.getLastID(), 1, 0)))
    # print("近5000期和值比：" + "\r\n" + str(ch.CalSum(begin, begin + 5000, 1, 0)))
    print("近1000期和值比：" + "\r\n" + str(ch.CalSum(begin, begin + 1000, 1, 0)))
    print("近100期和值比：" + "\r\n" + str(ch.CalSum(begin, begin + 100, 1, 0)))
    print("近50期和值比：" + "\r\n" + str(ch.CalSum(begin, begin + 50, 1, 0)))
    print("近30期和值比：" + "\r\n" + str(ch.CalSum(begin, begin + 30, 1, 0)))
    print("近10期和值比：" + "\r\n" + str(ch.CalSum(begin, begin + 10, 1, 0)))
    print("")
    # 0小 1大
    # print("按位大小比: " + str(ch.CalBSSaOES(begin, begin + ch.getLastID(), "BSS")))
    # print("近5000期按位大小比: " + str(ch.CalBSSaOES(begin, begin + 5000, "BSS")))
    print("近1000期按位大小比: " + str(ch.CalBSSaOES(begin, begin + 1000, "BSS")))
    print("近100期按位大小比: " + str(ch.CalBSSaOES(begin, begin + 100, "BSS")))
    print("近50期按位大小比: " + str(ch.CalBSSaOES(begin, begin + 50, "BSS")))
    print("近30期按位大小比: " + str(ch.CalBSSaOES(begin, begin + 30, "BSS")))
    print("近10期按位大小比: " + str(ch.CalBSSaOES(begin, begin + 10, "BSS")))
    print("")
    # print("按位奇偶比: " + str(ch.CalBSSaOES(begin, begin + ch.getLastID(), "OES")))
    # print("近5000期按位奇偶比: " + str(ch.CalBSSaOES(begin, begin + 5000, "OES")))
    print("近1000期按位奇偶比: " + str(ch.CalBSSaOES(begin, begin + 1000, "OES")))
    print("近100期按位奇偶比: " + str(ch.CalBSSaOES(begin, begin + 100, "OES")))
    print("近50期按位奇偶比: " + str(ch.CalBSSaOES(begin, begin + 50, "OES")))
    print("近30期按位奇偶比: " + str(ch.CalBSSaOES(begin, begin + 30, "OES")))
    print("近10期按位奇偶比: " + str(ch.CalBSSaOES(begin, begin + 10, "OES")))
    print("")
    ch.CalCurrent(begin)
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
    sums = list(map(int, input("和值比：").split(",")))
    st = list(map(int, input("杀百位：").split(",")))
    nd = list(map(int, input("杀十位：").split(",")))
    rd = list(map(int, input("杀个位：").split(",")))
    bss = list(map(str, input("杀大小比: ").split(",")))
    oes = list(map(str, input("杀奇偶比: ").split(",")))
    print("预测直选结果：")
    ch.Guess(begin, begin + 100, int(repeace), bigsmall, oddeven, ts, 0, st, nd, rd, bss, oes, sums)
    print("预测组选结果：")
    ch.Guess(begin, begin + 100, int(repeace), bigsmall, oddeven, ts, 1, st, nd, rd, bss, oes, sums)           
if __name__ == "__main__":
    np.seterr(invalid='ignore')
    while True:
        print("")
        select = input("请选择操作:\n1.爬取数据\n2.处理数据\n3.预测数据\n4.处理历史数据\n5.预测历史数据\n6.趋向性模型计算\n7.趋向性模型模拟\n8.绘制指定图像\n9.临时测试\n99.退出\n")
        if select == "1":
            ch.crawler()
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
            num = int(input("输入预测期数："))
            ch.CalMK(num)
        elif select == "7":
            num = int(input("输入预测期数："))
            ch.CalMKP(num)
        elif select == "8":
            select = input("输入选择的期数，默认为当前期：")
            if select.isdigit():
                if int(select) < 0:
                    num = -1
                else:
                    num = int(select)
            else:
                num = 0
            ch.CalLimit(num, 1000, 1, 20, 10, ch.getLastSumData(num))
            # ch.CalLimit(num, ch.getLastID(), 1, 20, 10, ch.getLastSumData(num))
            # CreateIMG(0, 5000, 1, "BS", 0)
        elif select == "9":
            # print(ch.CalculateMuliteRate())
            listA = ch.CalculateMuliteRate()
            # str(Decimal((scnt[i] / (cnt * 3)) * 100).quantize(Decimal("0.00"))) + "%"
            for i in range(28):
                print(str(i) + ":     " + str(Decimal(listA[0][i]).quantize(Decimal("0.00"))) + "%     " + str(Decimal(listA[1][i]).quantize(Decimal("0.00"))) + "%" + "     " + str(Decimal(listA[2][i]).quantize(Decimal("0.00"))) + "%" + "     " + str(Decimal(listA[3][i]).quantize(Decimal("0.00"))) + "%")
        elif select == "99":
            break