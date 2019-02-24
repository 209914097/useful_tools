# 只需在url_list填json链接，trainNO_list填备选车次，date_list填备选日期，tickettype填票别，seattype填席别，use12306，pw12306填12306账号密码，即可
#其它不用管
from TicketBook import *
from TicketChange import *
from TicketLeft import ticketleft

#---------------------购票信息---------------------#
url_list = [
        'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2019-02-24&leftTicketDTO.from_station=SFX&leftTicketDTO.to_station=AAX&purpose_codes=ADULT', \
        'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2019-02-23&leftTicketDTO.from_station=SFX&leftTicketDTO.to_station=AAX&purpose_codes=ADULT'
    ]
date_list = ['2月24日', '2月23日']
trainNO_list = ['6261', '6265']
IS_CDN=True
tickettype='学生票'
seattype='硬卧'
use12306=''#敏感信息
pw12306= ''#敏感信息
IS_TicketBook=False#是订票还是捡漏改签
sequence_no= 'E128932057'#捡漏改签填入要改签的订单号


#---------------------查票---------------------#

tk = ticketleft(url_list, date_list, trainNO_list,IS_CDN)
tk.query()

if IS_TicketBook:
    #---------------------订票---------------------#
    msg = {
        'url': tk.resultDic['url'],
        'trainNO': tk.resultDic['trainNO'],
        'seattype': seattype ,
        'use': use12306,
        'pw': pw12306,
        'student': tickettype,
        'AIcaptcha':False,
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
elif not IS_TicketBook:
    #---------------------改签---------------------#
    resginmsg = {
            'resginurl': tk.resultDic['url'],
            'trainNO': tk.resultDic['trainNO'],#改签到哪辆车次
            'sequence_no':sequence_no,#订单号
            'use': use12306,
            'pw': pw12306,
            'AIcaptcha': False,
            'changeTSFlag': False,#True ‘变更到站’改签出发日期,车次,到站必须不同 False‘改签’仅改签出发日期和车次
        }
    err_num=0
    while True:
        try:
            tkc = ticketchange(resginmsg)
            tkc.resginticket()
            break
        except:
            err_num+=1
            if err_num>=5:
                os._exit(0)
            localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(
                colored('resginticket(msg)出错,正在重试 %s\n%s %s' % (localtime, sys.exc_info()[0], sys.exc_info()[1]), 'red'))
            with open('TicketChange_err.txt', 'a') as f:
                f.write(
                    '\n' + 'resginticket(msg)出错,重试,%s' % (localtime) + '\n' + str(sys.exc_info()[0]) + str(
                        sys.exc_info()[1]) + '\n')
            time.sleep(1)
            continue
