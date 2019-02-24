from LogIn import login
from requests import packages,Session
import json
import datetime
import re
from bs4 import BeautifulSoup
from urllib.parse import unquote, quote
import time,os,sys
from termcolor import *

class ticketchange:
    def __init__(self, resginmsg):
        self.use=resginmsg['use']
        self.pw=resginmsg['pw']
        self.resginurl = resginmsg['resginurl']
        self.AIcaptcha=resginmsg['AIcaptcha']
        self.sequence_no=resginmsg['sequence_no']
        self.trainNO = resginmsg['trainNO']
        self.changeTSFlag='Y'if resginmsg['changeTSFlag'] else 'N'

        Auth = login(self.use, self.pw, self.AIcaptcha)
        self.session=Auth.golog()
    def resginticket(self):
# --------------queryMyOrder-------------------#
        packages.urllib3.disable_warnings()
        query_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/view/train_order.html',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
            'X-Requested-With': 'XMLHttpRequest',
        }
        queryEndDate = datetime.datetime.now().strftime('%Y-%m-%d')
        queryStartDate = (datetime.datetime.now() + datetime.timedelta(days=-31)).strftime('%Y-%m-%d')
        self.session.headers.update(query_headers)
        reply = self.session.request(method='post',
                                timeout=8,
                                url='https://kyfw.12306.cn/otn/queryOrder/queryMyOrder',
                                allow_redirects=False,
                                verify=False,
                                data={'come_from_flag': 'my_order',
                                        'pageIndex': '0',
                                        'pageSize': '8',
                                        'query_where': 'G',
                                        'queryStartDate': queryStartDate,
                                        'queryEndDate': queryEndDate,
                                        'queryType': '1',
                                        'sequeue_train_name':'', }
                                     )
        jsonstr = json.loads(reply.text)

        for order in jsonstr['data']['OrderDTODataList']:
            if( order['sequence_no']==self.sequence_no):
                tickets_msg= order['tickets'][0]
                resign_flag=tickets_msg['resign_flag']#1
                coach_no=tickets_msg['coach_no']#07车
                seat_no=tickets_msg['seat_no']#0173
                start_train_date_page=tickets_msg['start_train_date_page']#2019-03-01 17:10
                back_train_date=tickets_msg['start_train_date_page'][0:10]
                seat_type_code=tickets_msg['seat_type_code']
                ticket_type_code=tickets_msg['ticket_type_code']
# --------------resginTicket-------------------#
        reply = self.session.request(method='post',
                                timeout=8,
                                url='https://kyfw.12306.cn/otn/queryOrder/resginTicket',
                                allow_redirects=False,
                                verify=False,
                                data={  'ticketkey': self.sequence_no+','+resign_flag+','+coach_no+','+seat_no+','+start_train_date_page+'#' ,
                                        'sequenceNo': self.sequence_no,
                                        'changeTSFlag': self.changeTSFlag,
                                        '_json_att':'', }
                                     )
        jsonstr = json.loads(reply.text)
# {"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,"data":{"existError":"N"},"messages":[],"validateMessages":{}}
# -----------------------https://kyfw.12306.cn/otn/modifyUser/initQueryUserInfoApi-----获取个人身份证，手机号信息---由于12306网站后端改版，因此修改代码---------------#
        information = BeautifulSoup(
            self.session.post('https://kyfw.12306.cn/otn/modifyUser/initQueryUserInfoApi', headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate,br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Host': 'kyfw.12306.cn',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36', }).text,
            "html.parser")
        information.encoding = 'utf-8'  # 避免汉字乱码
        information = json.loads(information.text)['data']['userDTO']['loginUserDTO']
        # -----------------------由于12306网站前端改版，因此修改代码-----------------------#
        Name = information['name']  # '肖菲'
        ID_Number = information['id_no']  # '145481197512497514'
        PhoneNumber = information['agent_contact']  # '18820052354'
# -----------------------查票获取secretStr-----------------------#
        packages.urllib3.disable_warnings()
        query_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.session.headers.update(query_headers)
        purpose_codes = re.findall("purpose_codes=(\w+)", self.resginurl)[0]
        self.resginurl=self.resginurl.replace(purpose_codes,'0X00' if ticket_type_code=='3' else 'ADULT')#若原来的车票是学生票
        purpose_codes='0X00' if ticket_type_code=='3' else 'ADULT'
        reply = self.session.request(method='get',
                                timeout=4,
                                url=self.resginurl,
                                allow_redirects=False,
                                verify=False)
        jsonstr = json.loads(reply.text)
        train_date = re.findall('train_date=(.+?)&', self.resginurl)[0]
        focitycode = re.findall('from_station=(.+?)&', self.resginurl)[0]
        tocitycode= re.findall('to_station=(.+?)&', self.resginurl)[0]
        trainlist = jsonstr['data']['result']
        fromcity = jsonstr['data']['map'][focitycode]
        tocity = jsonstr['data']['map'] [tocitycode]
        for x in trainlist:
            if x.find(self.trainNO) != -1:
                trainmsglist = x.split('|')
# -----------------------checkUser-----------------------#
        checkUser_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'kyfw.12306.cn',
            'If-Modified-Since': '0',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
            'X-Requested-With': 'XMLHttpRequest',
        }
        print('checkUser:' + self.session.post('https://kyfw.12306.cn/otn/login/checkUser', data={'_json_att': '', },
                                          headers=checkUser_headers).text)
# -----------------------submitOrderRequest-----------------------#
        form2_data = {
            'secretStr': unquote(trainmsglist[0]),
            # trainmsglist[0] 字符串要先解码，因为放到 post 请求里后会再编码,这是最大一个坑，找了一天!!! 感谢http://tiven.wang/train-api/提示
            'train_date': train_date,
            'back_train_date': back_train_date,
            'tour_flag': 'gc',
            'purpose_codes': purpose_codes,
            'query_from_station_name': fromcity,
            'query_to_station_name': tocity,
            'undefined': ''
        }
        re0 = self.session.post('https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest', data=form2_data,
                           headers=query_headers)
        print('submitOrderRequest:' + re0.text)
# -----------------------confirmPassenger/initGc-----------------------#
        re1 = self.session.post('https://kyfw.12306.cn/otn/confirmPassenger/initGc', headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36', },
                           data={'_json_att': '', })

        RepeatSubmitToken = re.findall("var globalRepeatSubmitToken = '(\w+)';", re1.text)[0]
        key_check_isChange = re.findall("'key_check_isChange':'(\w+)','leftDetails'", re1.text)[0]
        time.sleep(5)
# -----------------------checkOrderInfo-----------------------#
        form3_data = {
            'cancel_flag': '2',
            'bed_level_order_num': '000000000000000000000000000000',
            'passengerTicketStr': '%s,0,%s,%s,1,%s,%s,Y' % (
            seat_type_code,ticket_type_code, Name, ID_Number, PhoneNumber),  # %(硬卧，学生票，姓名，身份证，手机号)
            'oldPassengerStr': '%s,1,%s,_' % (Name, ID_Number),
            'tour_flag': 'gc',
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': RepeatSubmitToken,
        }
        checkOrderInfo_head = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                               'Accept-Encoding': 'gzip, deflate, br',
                               'Accept-Language': 'zh-CN,zh;q=0.9',
                               'Connection': 'keep - alive',
                               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                               'Host': 'kyfw.12306.cn',
                               'Origin': 'https://kyfw.12306.cn',
                               'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initGc',
                               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
                               'X-Requested-With': 'XMLHttpRequest', }

        print('confirmPassenger:' + self.session.post('https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo',
                                                 headers=checkOrderInfo_head, data=form3_data).text)
    # -----------------------getQueueCount-----------------------#
        purpose_codes='0X00' if ticket_type_code=='3' else '00'
        form4_data = {
            'train_date': time.strftime('%a %b %d %Y 00:00:00 GMT%z ', time.strptime(train_date, '%Y-%m-%d')) + '(中国标准时间)',
            'train_no': trainmsglist[2],
            'stationTrainCode': trainmsglist[3],
            'seatType': seat_type_code,
            'fromStationTelecode': trainmsglist[6],
            'toStationTelecode': trainmsglist[7],
            'leftTicket': trainmsglist[12],
            'purpose_codes':purpose_codes ,
            'train_location': trainmsglist[15],
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': RepeatSubmitToken,
        }
        print('getQueueCount:' + self.session.post('https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount',
                                              headers=checkOrderInfo_head, data=form4_data).text)
        # -----------------------confirmResignForQueue-----------------------#
        form5_data = {
            'passengerTicketStr': '%s,0,%s,%s,1,%s,%s,Y' % (
                seat_type_code,ticket_type_code, Name, ID_Number, PhoneNumber),  # %(硬卧，学生票， 姓名，身份证，手机号)
            'oldPassengerStr': '%s,1,%s,_' % (Name, ID_Number,),
            'randCode': '',
            'purpose_codes': purpose_codes,
            'key_check_isChange': key_check_isChange,
            'leftTicketStr': trainmsglist[12],
            'train_location': trainmsglist[15],
            'choose_seats': '',
            'seatDetailType': '000',
            'whatsSelect': '1',
            'roomType': '00',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': RepeatSubmitToken,
        }

        print('confirmResignForQueue:' + self.session.post('https://kyfw.12306.cn/otn/confirmPassenger/confirmResignForQueue',
                                                     data=form5_data,
                                                     headers=checkOrderInfo_head).text)
        #-------------------------------------resultOrderForGcQueue---------------#
        self.session.post('https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForGcQueue',
                     data={
                         'orderSequence_no':self.sequence_no,
                         '_json_att':'',
                         'REPEAT_SUBMIT_TOKEN':RepeatSubmitToken,
                     },
                     headers={
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
                     })

        WeChat = Session()
        response = WeChat.post('https://sc.ftqq.com/秘钥.send',
                                data={'text': self.trainNO+'改签完成提交', 'desp': '改签完成提交', })
        print("改签已经完成提交，您可以登录后台进行支付了。")





if __name__ == '__main__':

    resginmsg = {
        'resginurl': 'https://115.223.7.173/otn/leftTicket/queryZ?leftTicketDTO.train_date=2019-02-26&leftTicketDTO.from_station=SFX&leftTicketDTO.to_station=AAX&purpose_codes=ADULT',
        'trainNO': '6261',#改签到哪辆车次
        'sequence_no': 'E188426512',#订单号
        'use': '12306账户',#敏感信息
        'pw': '12306密码',#敏感信息
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
