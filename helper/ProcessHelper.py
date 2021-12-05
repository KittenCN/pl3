import math

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
        if ans[int(strnum[i])] == 3:
            return 0
        elif ans[int(strnum[i])] == 2:
            return 1
    return 2

def getSumNum(num):
    ans = 0
    while num > 0:
        ans += num % 10
        num //= 10
    return ans
