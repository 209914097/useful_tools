#url 填入查票url,trainNO='T122'填要买的车次,seattype='硬卧'要买的席别,student='学生票'学生票还是成人票,use,pw填12306账号密码
#内部变量尽量不改 dictory可以用于增加席别如一等座

from numpy import *
import json
from urllib.parse import unquote, quote
import os
from requests import get, post, Session
from bs4 import BeautifulSoup
import time
from termcolor import *
import re
from rk import RClient



def ticketbook(msg):
    url = msg['url']
    trainNO = msg['trainNO']
    seattype = msg['seattype']
    use = msg['use']
    pw = msg['pw']
    student = msg['student']

    # -----------------------可改参数的内部变量-----------------------#
    dictory = {'硬卧': 3, '软卧': 4, '硬座': 1, '一等座': 'M','学生票':'3','成人票':'1'}
    train_date = re.findall('train_date=(.+?)&', url)[0]
    focitycode = re.findall('from_station=(.+?)&', url)[0]
    tocitycode= re.findall('to_station=(.+?)&', url)[0]

    def pick(num):
        answer = ''
        axis = ['37,45', '107,45', '182,45', '252,45',
                '37,115', '107,115', '182,115', '252,115']
        for x in num:
            answer += axis[x - 1] + ','
        return (answer[:-1])

    # -----------------------https://kyfw.12306.cn/otn/login/init-----------------------#
    session = Session()
    session.get('https://kyfw.12306.cn/otn/login/init', headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'kyfw.12306.cn',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36", })

    # -----------------------captcha-image?login_site=E&module=login&rand=sjrand&0.9725909596164388-------下载验证码----------------#
    captchaurl = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand'
    captchaheaders = {
        'Accept': 'image / webp, image / apng, image / *, * / *;q = 0.8',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'kyfw.12306.cn',
        'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
    }
    checkcodecontent = session.get(captchaurl, headers=captchaheaders)
    with open('captcha-image.jpg', 'wb') as f:
        f.write(checkcodecontent.content)

    # -----------------------验证码"真·人工智能"识别-----------------------#
    rc = RClient('用户名', '用户密码'.encode("utf-8"), '软件ID', '软件Key')#敏感信息
    im = open('captcha-image.jpg', 'rb').read()
    im_num =rc.rk_create(im, 6113)
    checkcode = [int(x) for x in list(im_num['Result'])]
    checkcode = pick(checkcode)
    # -----------------------验证码手动识别-----------------------#
    # os.startfile('captcha-image.jpg')
    # checkcode = [int(x) for x in input('输入图片序号用,分隔:').split(',')]
    # checkcode = pick(checkcode)
    # -----------------------captcha-check------------提交验证码-----------#
    check_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
    check_headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'kyfw.12306.cn',
        'Origin': 'https://kyfw.12306.cn',
        'Referer': 'https://kyfw.12306.cn/otn/login/init',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
        'X-Requested-With': 'XMLHttpRequest',
    }
    captcha_data = {
        'answer': checkcode,
        'login_site': 'E',
        'rand': 'sjrand',
    }
    captcha_response = session.post(check_url, data=captcha_data, headers=check_headers)
    print(captcha_response.text)
    if (captcha_response.json()["result_message"]=="验证码校验失败"):
        return "验证码校验失败"

    # -----------------------web/login-----------------------#{"result_message":"验证码校验失败","result_code":"5"}
    # print('继续')

    login_url = 'https://kyfw.12306.cn/passport/web/login'
    form_data = {
        'username': use,
        'password': pw,
        'appid': 'otn',
    }
    log_response = session.post(login_url, data=form_data, headers=check_headers)
    print(log_response.text)
    # -----------------------userLogin-----------------------#
    session.post('https://kyfw.12306.cn/otn/login/userLogin', data={'_json_att': '', }, headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'kyfw.12306.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36', })


    # -----------------------uamtk-----------------------#
    uamtk_response1 = session.post('https://kyfw.12306.cn/passport/web/auth/uamtk', data={'appid': 'otn', }, headers={
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'kyfw.12306.cn',
        'Origin': 'https://kyfw.12306.cn',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
        'X-Requested-With': 'XMLHttpRequest', })
    tk = json.loads(uamtk_response1.text)["newapptk"]
    # -----------------------uamauthclient-----------------------#
    session.post('https://kyfw.12306.cn/otn/uamauthclient', data={'tk': tk, }, headers={
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'kyfw.12306.cn',
        'Origin': 'https://kyfw.12306.cn',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
        'X-Requested-With': 'XMLHttpRequest', })
    # -----------------------initMy12306-----------------------#
    session.get('https://kyfw.12306.cn/otn/index/initMy12306', headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'kyfw.12306.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36', })
    # -----------------------initQueryUserInfo-----获取个人身份证，手机号信息------------------#

    usemsg_html = BeautifulSoup(
        session.post('https://kyfw.12306.cn/otn/modifyUser/initQueryUserInfo', data={'_json_att': ''}, headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'kyfw.12306.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36', }).text,
        "html.parser")
    usemsg = usemsg_html.select('div[class="con"]')
    # -----------------------由于12306网站前端改版，因此修改代码-----------------------#
    Name=usemsg[2].text
    ID_Number=usemsg[3].text
    PhoneNumber=usemsg[17].text
    # -----------------------查票获取secretStr-----------------------#

    query_url = url
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
    reply = session.get(query_url, headers=query_headers)
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

    print('confirmPassenger:' + session.post('https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo',
                                             headers=checkOrderInfo_head, data=form3_data).text)

    # -----------------------getQueueCount-----------------------#
    form4_data = {
        'train_date': time.strftime('%a %b %d %Y 00:00:00 GMT%z ', time.strptime(train_date, '%Y-%m-%d')) + '(中国标准时间)',
        'train_no': trainmsglist[2],
        'stationTrainCode': trainmsglist[3],
        'seatType': dictory[seattype],
        'fromStationTelecode': trainmsglist[6],
        'toStationTelecode': trainmsglist[5],
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
            exit()
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

    #-------------------------------------resultOrderForDcQueue---------------#
    session.post('https://kyfw.12306.cn/otn//payOrder/init',
                 data={
                     '_json_att':'',
                     'REPEAT_SUBMIT_TOKEN':RepeatSubmitToken,
                 },
                 headers={
                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
                 })
    print("订单已经完成提交，您可以登录后台进行支付了。")

if __name__ == '__main__':
    msg = {
        'url': 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-05-22&leftTicketDTO.from_station=SBT&leftTicketDTO.to_station=GZQ&purpose_codes=ADULT',
        'trainNO': 'T122',
        'seattype': '硬卧',
        'use': '12306账户',#敏感信息
        'pw': '12306密码',#敏感信息
        'student': '成人票',
        }

    flag=ticketbook(msg)
    while (flag=="验证码校验失败"):
        print(colored('验证码识别出错,正在重试%s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), 'red'))
        with open('TicketBook_err.txt', 'a') as f:
            f.write('\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '验证码识别出错,正在重试' + '\n')
        flag =ticketbook(msg)  # 再次登录订票



