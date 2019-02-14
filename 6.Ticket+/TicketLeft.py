# 只需在url填json链接，trainNO填车次，date填日期，即可监视硬卧余票信息，numi不用改
# url2,trainNO2,date2填第二志愿车次信息
# 邮件发送程序执行后，5秒之后远程服务器才发出邮件，1分钟之后才会收到短信提示
import time
from CdnList import CDN
import sys
import json
from requests import get, post, Session,packages
from bs4 import BeautifulSoup
from termcolor import *
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


class ticketleft(object):
    def __init__(self, url_list, date_list, trainNO_list,IS_CDN):
        self.url_list = url_list

        self.date_list = date_list

        self.trainNO_list = trainNO_list
        self.IS_CDN = IS_CDN
        self.resultDic = {}
        if self.IS_CDN:
            self.cdn = CDN()
            self.cdn.load_cdnfile('cdn_verify_cache')
    def sent(self, trainNO, ticketleft, datetime):
        from_addr = '139邮箱账户'#敏感信息
        password = '139邮箱密码'#敏感信息
        to_addr = '139邮箱账户'#敏感信息
        smtp_server = 'smtp.139.com'

        msg = MIMEText('火车票:%s硬卧%s' % (trainNO, ticketleft), 'plain', 'utf-8')
        msg['From'] = '139邮箱账户'#敏感信息
        msg['To'] = '139邮箱账户'#敏感信息
        msg['Subject'] = Header('%s:硬卧%s:%s' % (trainNO, ticketleft, datetime), 'utf-8').encode()

        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.set_debuglevel(0)#为0是不会输出调试信息
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()

    def login(self):
        for url in self.url_list:
            captchaurl = self.cdn.random_cdnurl(url) if self.IS_CDN else url
            print(self.date_list[self.url_list.index(url)])
            session = Session()
            packages.urllib3.disable_warnings()
            session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
                'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
                'Accept-Encoding': 'gzip, deflate,br',
                'Accept-Language': 'zh-CN,zh;q=0.9', 'Host': 'kyfw.12306.cn'
            })
            checkcodecontent = session.request(method='get',
                                   timeout=4,
                                   url=captchaurl,
                                   allow_redirects=False,
                                   verify=False)

            jsonstr = json.loads(checkcodecontent.text)
            traintable = jsonstr['data']['result']
            for x in traintable:
                for trainNO in self.trainNO_list:
                    if x.find(trainNO) != -1:
                        print(x)
                        trainmsg = x.split('|')
                        if (trainmsg[28] != '无') and (trainmsg[28] != '*'):
                            self.sent(trainNO, trainmsg[28], self.date_list[self.url_list.index(url)])
                            self.resultDic['trainNO'] = trainNO
                            self.resultDic['url'] = url
                            return 'getit'
            time.sleep(2)

    def query(self):
        numi = 0

        while True:
            numi = numi + 1
            localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            try:
                print('第%s次,%s' % (numi, localtime))
                if (self.login() == 'getit'):
                    break

            except:
                print(colored('第%s次出错,%s' % (numi, localtime), 'red'))
                print(sys.exc_info()[0], sys.exc_info()[1])
                with open('TicketLeft_err.txt', 'a') as f:
                    f.write('\n' + '第%s次出错,%s' % (numi, localtime) + '\n' + str(sys.exc_info()[0]) + str(
                        sys.exc_info()[1]) + '\n')
                time.sleep(10)
                continue


if __name__ == '__main__':
    url_list = [
        'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2019-03-01&leftTicketDTO.from_station=GZQ&leftTicketDTO.to_station=SBT&purpose_codes=ADULT', \
        'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2019-02-13&leftTicketDTO.from_station=GZQ&leftTicketDTO.to_station=SBT&purpose_codes=ADULT',\
        'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2019-02-12&leftTicketDTO.from_station=GZQ&leftTicketDTO.to_station=SBT&purpose_codes=ADULT'
    ]
    date_list = ['3月1日', '2月13日', '2月12日']
    trainNO_list = ['Z386'，'Z114']
    IS_CDN=True

    tk = ticketleft(url_list, date_list, trainNO_list,IS_CDN)
    tk.query()
    print(tk.resultDic['trainNO'])
    print(tk.resultDic['url'])

