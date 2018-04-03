# 只需在url填json链接，trainNO填车次，date填日期，即可监视硬卧余票信息，num不用改

import time
import requests
import os
import json
from requests import get, post, Session
from bs4 import BeautifulSoup
from termcolor import *
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

url='https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date=2018-04-28&leftTicketDTO.from_station=SYT&leftTicketDTO.to_station=GZQ&purpose_codes=ADULT'
url2='https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date=2018-04-29&leftTicketDTO.from_station=SYT&leftTicketDTO.to_station=GZQ&purpose_codes=ADULT'
date='4-28'
date2='4-29'
trainNO='Z666'
trainNO2='Z1024'


def sent(trainNO, ticketleft,datetime):
    from_addr = '139.com'
    password = 'l'
    to_addr = 'm'
    smtp_server = 'smtp.139.com'

    msg = MIMEText('火车票:%s硬卧%s' % (trainNO , ticketleft), 'plain', 'utf-8')
    msg['From'] = 'm'
    msg['To'] = 'm'
    msg['Subject'] = Header('%s:硬卧%s:%s'% (trainNO , ticketleft,datetime), 'utf-8').encode()

    server = smtplib.SMTP_SSL(smtp_server, 465)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def login():
    captchaurl =url
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
        'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    session = Session()
    checkcodecontent = session.get(captchaurl, headers=headers)
    jsonstr=json.loads(checkcodecontent.text)
    trainlist=jsonstr['data']['result']
    for x in trainlist:
        if x.find(trainNO)!=-1:
            print(x)
            trainmsg=x.split('|')
            if (trainmsg[28] != '无')and(trainmsg[28] != '*'):sent(trainNO,trainmsg[28],date);return 'getit'
# ------------------------------------------可注释，用于选择同一日期多趟车------------------#
        if x.find(trainNO2)!=-1:
            print(x)
            trainmsg=x.split('|')
            if (trainmsg[28] != '无')and(trainmsg[28] != '*'):sent(trainNO2,trainmsg[28],date);return 'getit'
# ------------------------------------------可注释，用于选择同一日期多趟车------------------#

# ------------------------------------------可注释，用于选择同一趟车多日期------------------#
    time.sleep(5)
    captchaurl =url2
    session = Session()
    checkcodecontent = session.get(captchaurl, headers=headers)
    jsonstr=json.loads(checkcodecontent.text)
    trainlist=jsonstr['data']['result']
    for x in trainlist:
        if x.find(trainNO)!=-1:
            print(x)
            trainmsg=x.split('|')
            if (trainmsg[28] != '无')and(trainmsg[28] != '*'):sent(trainNO,trainmsg[28],date2);return 'getit'

# ------------------------------------------可注释，用于选择同一趟车多日期------------------#
# ------------------------------------------可注释，用于选择同一日期多趟车------------------#
        if x.find(trainNO2)!=-1:
            print(x)
            trainmsg=x.split('|')
            if (trainmsg[28] != '无')and(trainmsg[28] != '*'):sent(trainNO2,trainmsg[28],date2);return 'getit'
# ------------------------------------------可注释，用于选择同一日期多趟车------------------#

def begin():
    num = 0
    while True:
        num=num+1
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            print('第%s次,%s'%(num,localtime))
            if (login() == 'getit'): break            
            time.sleep(5)
        except:
            print(colored('第%s次出错,%s' % (num,localtime),'red' ))

            with open('log.txt', 'a') as f:
                f.write('\n' + '第%s次出错,%s' % (num,localtime) + '\n')

            time.sleep(30)
            begin()

begin()
