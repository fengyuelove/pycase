#!/usr/lib/env python2.7
# -*- coding:utf-8 -*-
from datetime import datetime, date, time, timedelta
from random import randrange, randint
import sys
import os

args = sys.argv
if args.__len__() < 2:
    print "请输入要生成的月份(1-12)!"

month = args[1]

print "开始生成%s月份的数据……" % month


if os.path.isfile("t.txt"):
    os.remove('t.txt')

startDateDict = {"10": 15, "20": 30, "30": 20, "40": 15, "50": 10, "60": 5, "70": 5}


def randomrange(data):
    startdatelist = []
    for m, n in data.items():
        for i in range(n):
            startdatelist.append(int(m))
    return startdatelist[randrange(len(startdatelist) - 1)]


startDate = date(datetime.now().year, int(month), 1)

while True:
    if startDate.month == int(month):
        if startDate.weekday() == 5 or startDate.weekday() == 6:
            print "%s不是工作日" % startDate
            startDate += timedelta(1)
            continue

        with open("./t.txt", 'a') as f:
            randomStartMinRange = randomrange(startDateDict)
            startTime = datetime(startDate.year, startDate.month, startDate.day, 21, 0, 0) + timedelta(
                    minutes=(randint(randomStartMinRange - 10, randomStartMinRange)))
            timeInterval = randint(39, 50)
            endTime = startTime + timedelta(minutes=timeInterval)

            if timeInterval < 42:
                money = 75 + randrange(timeInterval - 38)
            elif timeInterval < 46:
                money = 78 + randrange(timeInterval - 41)
            elif timeInterval < 51:
                money = 80 + randrange(timeInterval - 45)

            f.write("%s, %s - %s, %s  \n" % (startDate, startTime.strftime("%H:%M"), endTime.strftime("%H:%M"), money))

        startDate += timedelta(1)

    else:
        print "数据生成结束……"
        break

