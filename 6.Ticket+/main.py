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
err_num = 0
while True:
    try:
        ticketbook(msg)
        break
    except:
        err_num += 1
        if err_num >= 5:
            os._exit(0)
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(
            colored('ticketbook(msg)出错,正在重试 %s\n%s %s' % (localtime, sys.exc_info()[0], sys.exc_info()[1]), 'red'))
        with open('TicketBook_err.txt', 'a') as f:
            f.write(
                '\n' + 'ticketbook(msg)出错,重试,%s' % (localtime) + '\n' + str(sys.exc_info()[0]) + str(
                    sys.exc_info()[1]) + '\n')
        time.sleep(1)
        continue
