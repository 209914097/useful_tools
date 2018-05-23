# 只需在url填json链接，trainNO填车次，date填日期，tickettype填票别，seattype填席别，use12306，pw12306填12306账号密码，即可
#url2,trainNO2,date2填第二志愿车次信息
#其它不用管
from TicketBook import *
from TicketLeft import ticketleft

#---------------------购票信息---------------------#
url='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-06-04&leftTicketDTO.from_station=SBT&leftTicketDTO.to_station=GZQ&purpose_codes=ADULT'
url2='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-05-29&leftTicketDTO.from_station=SBT&leftTicketDTO.to_station=GZQ&purpose_codes=ADULT'
date='6月4日'
date2='5月29日'
trainNO='Z384'
trainNO2='Z238'
tickettype='成人票'

seattype='硬卧'
use12306=''#敏感信息
pw12306= ''#敏感信息

#---------------------查票---------------------#
tk=ticketleft(url,url2,date,date2,trainNO,trainNO2)
tk.query()

#---------------------订票---------------------#
msg = {
    'url': tk.resultDic['url'],
    'trainNO': tk.resultDic['trainNO'],
    'seattype': seattype ,
    'use': use12306,
    'pw': pw12306,
    'student': tickettype,
}
flag=ticketbook(msg)
while (flag=="验证码校验失败"):
    print(colored('验证码识别出错,正在重试%s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), 'red'))
    with open('TicketBook_err.txt', 'a') as f:
        f.write('\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '验证码识别出错,正在重试' + '\n')
    flag =ticketbook(msg)  # 再次登录订票