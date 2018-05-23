# 只需在url填json链接，trainNO填车次，date填日期，即可监视硬卧余票信息，numi不用改
#url2,trainNO2,date2填第二志愿车次信息
#邮件发送程序执行后，5秒之后远程服务器才发出邮件，1分钟之后才会收到短信提示
import time
import requests
import sys
import json
from requests import get, post, Session
from bs4 import BeautifulSoup
from termcolor import *
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

class ticketleft(object):
    def __init__(self,url,url2,date,date2,trainNO,trainNO2):
        self.url = url
        self.url2 = url2
        self.date = date
        self.date2 = date2
        self.trainNO = trainNO
        self.trainNO2 = trainNO2
        self.resultDic={}

    def sent(self,trainNO, ticketleft,datetime):
        from_addr = '139邮箱账户'#敏感信息
        password = '139邮箱密码'#敏感信息
        to_addr = '139邮箱账户'#敏感信息
        smtp_server = 'smtp.139.com'

        msg = MIMEText('火车票:%s硬卧%s' % (trainNO , ticketleft), 'plain', 'utf-8')
        msg['From'] = '139邮箱账户'#敏感信息
        msg['To'] = '139邮箱账户'#敏感信息
        msg['Subject'] = Header('%s:硬卧%s:%s'% (trainNO , ticketleft,datetime), 'utf-8').encode()

        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()

    def login(self):
        captchaurl =self.url
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
            if x.find(self.trainNO)!=-1:
                print(x)
                trainmsg=x.split('|')
                if (trainmsg[28] != '无')and(trainmsg[28] != '*'):
                    self.sent(self.trainNO,trainmsg[28],self.date)
                    self.resultDic['trainNO']=self.trainNO
                    self.resultDic['url'] =self.url
                    return 'getit'
    # ------------------------------------------可注释，用于选择同一日期多趟车------------------#
            if x.find(self.trainNO2)!=-1:
                print(x)
                trainmsg=x.split('|')
                if (trainmsg[28] != '无')and(trainmsg[28] != '*'):
                    self.sent(self.trainNO2,trainmsg[28],self.date)
                    self.resultDic['trainNO'] = self.trainNO2
                    self.resultDic['url'] = self.url
                    return 'getit'
    # ------------------------------------------可注释，用于选择同一日期多趟车------------------#

    # ------------------------------------------可注释，用于选择同一趟车多日期------------------#
        time.sleep(5)
        captchaurl =self.url2
        session = Session()
        checkcodecontent = session.get(captchaurl, headers=headers)
        jsonstr=json.loads(checkcodecontent.text)
        trainlist=jsonstr['data']['result']
        for x in trainlist:
            if x.find(self.trainNO)!=-1:
                print(x)
                trainmsg=x.split('|')
                if (trainmsg[28] != '无')and(trainmsg[28] != '*'):
                    self.sent(self.trainNO,trainmsg[28],self.date2)
                    self.resultDic['trainNO'] = self.trainNO
                    self.resultDic['url'] = self.url2
                    return 'getit'

    # ------------------------------------------可注释，用于选择同一趟车多日期------------------#
    # ------------------------------------------可注释，用于选择同一日期多趟车------------------#
            if x.find(self.trainNO2)!=-1:
                print(x)
                trainmsg=x.split('|')
                if (trainmsg[28] != '无')and(trainmsg[28] != '*'):
                    self.sent(self.trainNO2,trainmsg[28],self.date2)
                    self.resultDic['trainNO'] = self.trainNO2
                    self.resultDic['url'] = self.url2
                    return 'getit'
    # ------------------------------------------可注释，用于选择同一日期多趟车------------------#

    def query(self):
        numi = 0
        while True:
            numi=numi+1
            localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            try:
                print('第%s次,%s' % (numi, localtime))
                if (self.login() == 'getit'):
                    break
                time.sleep(5)
            except:
                print(colored('第%s次出错,%s' % (numi,localtime),'red' ))
                print(sys.exc_info()[0],sys.exc_info()[1])
                with open('TicketLeft_err.txt', 'a') as f:
                    f.write('\n' + '第%s次出错,%s' % (numi,localtime) + '\n'+str(sys.exc_info()[0])+str(sys.exc_info()[1]) + '\n')
                time.sleep(30)
                continue

if __name__ == '__main__':
    url='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-05-23&leftTicketDTO.from_station=SBT&leftTicketDTO.to_station=GZQ&purpose_codes=ADULT'
    url2='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-05-27&leftTicketDTO.from_station=SBT&leftTicketDTO.to_station=GZQ&purpose_codes=ADULT'
    date='5月23日'
    date2='5月27日'
    trainNO='Z384'
    trainNO2='Z114'
    tk=ticketleft(url,url2,date,date2,trainNO,trainNO2)
    tk.query()
    print(tk.resultDic['trainNO'])
    print(tk.resultDic['url'])

