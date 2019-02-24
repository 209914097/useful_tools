#url 填入查票url,trainNO='T122'填要买的车次,seattype='硬卧'要买的席别,student='学生票'学生票还是成人票,use,pw填12306账号密码
#内部变量尽量不改 dictory可以用于增加席别如一等座

from numpy import *
import json
from urllib.parse import unquote, quote
import sys
from requests import get, packages, Session
from bs4 import BeautifulSoup
import time
from termcolor import *
import re
from LogIn import login



def ticketbook(msg):
    url = msg['url']
    trainNO = msg['trainNO']
    seattype = msg['seattype']
    use = msg['use']
    pw = msg['pw']
    student = msg['student']
    AIcaptcha=msg['AIcaptcha']

    # -----------------------可改参数的内部变量-----------------------#
    dictory = {'硬卧': 3, '软卧': 4, '硬座': 1, '一等座': 'M','学生票':'3','成人票':'1'}
    train_date = re.findall('train_date=(.+?)&', url)[0]
    focitycode = re.findall('from_station=(.+?)&', url)[0]
    tocitycode= re.findall('to_station=(.+?)&', url)[0]

    Auth = login(use, pw, AIcaptcha)
    session = Auth.golog()
    # -----------------------index.html-登录个人中心---由于12306网站前端改版，因此修改代码--------------------#
    session.get('https://kyfw.12306.cn/otn/view/index.html', headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'kyfw.12306.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36', })
    # -----------------------https://kyfw.12306.cn/otn/modifyUser/initQueryUserInfoApi-----获取个人身份证，手机号信息---由于12306网站后端改版，因此修改代码---------------#

    information = BeautifulSoup(
        session.post('https://kyfw.12306.cn/otn/modifyUser/initQueryUserInfoApi', headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'kyfw.12306.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36', }).text,
        "html.parser")
    information.encoding = 'utf-8'#避免汉字乱码
    information = json.loads(information.text)['data']['userDTO']['loginUserDTO']
    # -----------------------由于12306网站前端改版，因此修改代码-----------------------#
    Name = information['name']  # '肖菲'
    ID_Number = information['id_no']  # '145481197512497514'
    PhoneNumber = information['agent_contact']  # '18820052354'
    # -----------------------查票获取secretStr-----------------------#
    query_url = url
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
    session.headers.update(query_headers)
    reply = session.request(method='get',
                            timeout=4,
                            url=query_url,
                            allow_redirects=False,
                            verify=False)
    jsonstr = json.loads(reply.text)
    trainlist = jsonstr['data']['result']
    fromcity = jsonstr['data']['map'][focitycode]
    tocity = jsonstr['data']['map'] [tocitycode]
    for x in trainlist:
        if x.find(trainNO) != -1:
            # print(x)
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
    print('checkUser:' + session.post('https://kyfw.12306.cn/otn/login/checkUser', data={'_json_att': '', },
                                      headers=checkUser_headers).text)

    # -----------------------submitOrderRequest-----------------------#
    form2_data = {
        'secretStr': unquote(trainmsglist[0]),
        # trainmsglist[0] 字符串要先解码，因为放到 post 请求里后会再编码,这是最大一个坑，找了一天!!! 感谢http://tiven.wang/train-api/提示
        'train_date': train_date,
        'back_train_date': time.strftime("%Y-%m-%d", time.localtime()),
        'tour_flag': 'dc',
        'purpose_codes': 'ADULT',
        'query_from_station_name': fromcity,
        'query_to_station_name': tocity,
        'undefined': ''
    }
    re0 = session.post('https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest', data=form2_data,
                       headers=query_headers)
    print('submitOrderRequest:' + re0.text)

    # -----------------------confirmPassenger/initDc-----------------------#
    re1 = session.post('https://kyfw.12306.cn/otn/confirmPassenger/initDc', headers={
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
    # confirm_html = BeautifulSoup(re1.text, "html.parser")
    # RepeatSubmitToken = confirm_html.find_all('script')[0].text.split(';')[1].split('=')[1][2:-1]
    RepeatSubmitToken = re.findall("var globalRepeatSubmitToken = '(\w+)';", re1.text)[0]
    key_check_isChange = re.findall("'key_check_isChange':'(\w+)','leftDetails'", re1.text)[0]
    # print(RepeatSubmitToken)
    time.sleep(5)
    # -----------------------checkOrderInfo-----------------------#
    form3_data = {
        'cancel_flag': '2',
        'bed_level_order_num': '000000000000000000000000000000',
        'passengerTicketStr': '%s,0,%s,%s,1,%s,%s,N' % (
        dictory[seattype],dictory[student], Name, ID_Number, PhoneNumber),  # %(硬卧，学生票，姓名，身份证，手机号)
        'oldPassengerStr': '%s,1,%s,3_' % (Name, ID_Number),
        'tour_flag': 'dc',
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
                           'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
                           'X-Requested-With': 'XMLHttpRequest', }

    print('checkOrderInfo:' + session.post('https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo',
                                             headers=checkOrderInfo_head, data=form3_data).text)

    # -----------------------getQueueCount-----------------------#
    form4_data = {
        'train_date': time.strftime('%a %b %d %Y 00:00:00 GMT%z ', time.strptime(train_date, '%Y-%m-%d')) + '(中国标准时间)',
        'train_no': trainmsglist[2],
        'stationTrainCode': trainmsglist[3],
        'seatType': dictory[seattype],
        'fromStationTelecode': trainmsglist[6],
        'toStationTelecode': trainmsglist[7],
        'leftTicket': trainmsglist[12],
        'purpose_codes': '00',
        'train_location': trainmsglist[15],
        '_json_att': '',
        'REPEAT_SUBMIT_TOKEN': RepeatSubmitToken,
    }
    print('getQueueCount:' + session.post('https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount',
                                          headers=checkOrderInfo_head, data=form4_data).text)
    # -----------------------confirmSingleForQueue-----------------------#
    form5_data = {
        'passengerTicketStr': '%s,0,%s,%s,1,%s,%s,N' % (
        dictory[seattype],dictory[student], Name, ID_Number, PhoneNumber),  # %(硬卧，学生票， 姓名，身份证，手机号)
        'oldPassengerStr': '%s,1,%s,3_' % (Name, ID_Number,),
        'randCode': '',
        'purpose_codes': '00',
        'key_check_isChange': key_check_isChange,
        'leftTicketStr': trainmsglist[12],
        'train_location': trainmsglist[15],
        'choose_seats': '',
        'seatDetailType': '000',
        'whatsSelect': '1',
        'roomType': '00',
        'dwAll': 'N',
        '_json_att': '',
        'REPEAT_SUBMIT_TOKEN': RepeatSubmitToken,
    }

    print('confirmSingleForQueue' + session.post('https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue',
                                                 data=form5_data,
                                                 headers=checkOrderInfo_head).text)
    # -----------------------queryOrderWaitTime-----------------------#
    timr = 0
    while True:
        re2 = session.get(
            'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random=%s&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN=%s' % (
            round(time.time() * 1000), RepeatSubmitToken), headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate,br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Host': 'kyfw.12306.cn',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest', })

        patorderid = '"orderId":"(.*?)"'
        orderidall = re.compile(patorderid).findall(re2.text)
        timr += 1
        if (timr > 20):
            print("超时!" )
            os._exit(0)#这样退出不会抛出异常
        if (len(orderidall) == 0):
            print("无orderid，重新请求。queryOrderWaitTime:"+ re2.text)
            continue
        else:
            orderid = orderidall[0]
            print("orderid:"+orderid)
            break
    #-------------------------------------resultOrderForDcQueue---------------#
    session.post('https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue',
                 data={
                     'orderSequence_no':orderid,
                     '_json_att':'',
                     'REPEAT_SUBMIT_TOKEN':RepeatSubmitToken,
                 },
                 headers={
                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
                 })

    #-------------------------------------payOrder/init---------------#
    session.post('https://kyfw.12306.cn/otn//payOrder/init',
                 data={
                     '_json_att':'',
                     'REPEAT_SUBMIT_TOKEN':RepeatSubmitToken,
                 },
                 headers={
                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
                 })
    WeChat = Session()
    response = WeChat.post('https://sc.ftqq.com/秘钥.send',
                            data={'text': trainNO+'订单完成提交', 'desp': '订单完成提交', })#Server酱,微信推送配置http://sc.ftqq.com/3.version
    # print(json.loads(response.text))
    print("订单已经完成提交，您可以登录后台进行支付了。")

if __name__ == '__main__':
    msg = {
        'url': 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2019-03-15&leftTicketDTO.from_station=GZQ&leftTicketDTO.to_station=SYT&purpose_codes=ADULT',
        'trainNO': 'Z114',
        'seattype': '硬卧',
        'use': '12306账户',#敏感信息
        'pw': '12306密码',#敏感信息
        'student': '学生票',
        'AIcaptcha': False,
    }
    err_num=0
    while True:
        try:
            ticketbook(msg)
            break
        except:
            err_num+=1
            if err_num>=5:
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



