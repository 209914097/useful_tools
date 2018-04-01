# 只需在url填入json链接，trainNO填入车次，即可返回硬卧票数信息，num不用改

import time
import requests
import os
import json
from requests import get, post, Session
from bs4 import BeautifulSoup
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

url='https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date=2018-04-05&leftTicketDTO.from_station=SYT&leftTicketDTO.to_station=GZQ&purpose_codes=ADULT'
trainNO='Z384'

def sent(trainNO, ticketleft):
    from_addr = '@139.com'
    password = ''
    to_addr = '@139.com'
    smtp_server = 'smtp.139.com'

    msg = MIMEText('火车票:%s:硬卧%s' % (trainNO , ticketleft), 'plain', 'utf-8')
    msg['From'] = '@139.com'
    msg['To'] = '@139.com'
    msg['Subject'] = Header('%s:硬卧%s'% (trainNO , ticketleft), 'utf-8').encode()

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
            if trainmsg[28]!='无':sent(trainNO,trainmsg[28]);return 'getit'

# ------------------------------------------可注释，用于选择同一趟车多日期------------------#
    time.sleep(5)
    captchaurl ='https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date=2018-04-03&leftTicketDTO.from_station=SYT&leftTicketDTO.to_station=GZQ&purpose_codes=ADULT'
    session = Session()
    checkcodecontent = session.get(captchaurl, headers=headers)
    jsonstr=json.loads(checkcodecontent.text)
    trainlist=jsonstr['data']['result']
    for x in trainlist:
        if x.find(trainNO)!=-1:
            print(x)
            trainmsg=x.split('|')
            if trainmsg[28]!='无':sent(trainNO,trainmsg[28]);return 'getit'
# ------------------------------------------可注释，用于选择同一趟车多日期------------------#


def begin():
    num = 0
    while True:
        num=num+1
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            if (login() == 'getit'): break
            print('第%s次,%s'%(num,localtime))
            time.sleep(5)
        except:
            print('第%s次出错' % (num))
            time.sleep(60)
            begin()

begin()
