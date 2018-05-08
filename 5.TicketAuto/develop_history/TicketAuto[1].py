from numpy import *
import json
from urllib.parse import unquote, quote
import os
from requests import get, post, Session
from bs4 import BeautifulSoup
import time
import re

url ='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-05-20&leftTicketDTO.from_station=SBT&leftTicketDTO.to_station=GZQ&purpose_codes=ADULT'
trainNO='Z12'
fromcity='沈阳'
tocity='广州'
train_date='2018-05-20'
seattype='硬卧'

str_login_site='E'
str_rand='sjrand'


def login(use='', pw=''):
    dictory = {'硬卧': 3, '软卧': 4, '硬座': 1, '一等座': 'M'}

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
    # -----------------------uamtk-----------------------#
    session.post('https://kyfw.12306.cn/passport/web/auth/uamtk', data={'appid': 'otn', }, headers={
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'kyfw.12306.cn',
        'Origin': 'https://kyfw.12306.cn',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
        'X-Requested-With': 'XMLHttpRequest', })

    # -----------------------captcha-image?login_site=E&module=login&rand=sjrand&0.9725909596164388-------下载验证码----------------#
    captchaurl = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.9725909596164388'
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
    os.startfile('captcha-image.jpg')
    checkcode = [int(x) for x in input('输入图片序号用,分隔:').split(',')]
    checkcode = pick(checkcode)
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
        'login_site': str_login_site,
        'rand': str_rand,
    }
    captcha_response = session.post(check_url, data=captcha_data, headers=check_headers)
    print(captcha_response.text)
    # -----------------------web/login-----------------------#
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

    # -----------------------redirect=/otn/login/userLogin-----------------------#
    session.get('https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin', headers={
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

    # -----------------------查票获取secretStr-----------------------#
    session.get('https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=passenger&rand=randp&0.051538683369815263',
                headers={
                    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate,br',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Host': 'kyfw.12306.cn',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36', })

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
    # ----------------------------------------------#
    #     p=session.get('https://kyfw.12306.cn/otn/HttpZF/logdevice?algID=RcHOncNR3i&hashCode=4CN16hiCWZSoP2EuwU4ZN9aiI4GbSs9Em45NB-tGbBM&FMQw=0&q4f3=zh-CN&VySQ=FGHldLUbosbDgpJq7AtDcvbufjSwXH2s&VPIf=1&custID=133&VEek=unknown&dzuS=29.0%20r0&yD16=0&EOQP=8f58b1186770646318a429cb33977d8c&lEnu=3396734384&jp76=bb5032aedcaa9cca45f29e44506d1288&hAqN=Win32&platform=WEB&ks0Q=93b5994b1daea02ec4a30a4f9c1a569c&TeRS=1040x1920&tOHY=24xx1080x1920&Fvje=i1l1o1s1&q5aJ=-8&wNLf=99115dfb07133750ba677d055874de87&0aew=Mozilla/5.0%20(Windows%20NT%206.1;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/64.0.3282.186%20Safari/537.36&E3gR=4fd3e2483e3e7ce617e5307727b0c4e8&timestamp=1525100252901',
    #                 headers={
    #                     'Accept': '*/*',
    #                     'Accept-Encoding': 'gzip, deflate,br',
    #                     'Accept-Language': 'zh-CN,zh;q=0.9',
    #                     'Host': 'kyfw.12306.cn',
    #                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36', })

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
        'passengerTicketStr': '%s,0,3,%s,1,%s,%s,N' % (
        dictory[seattype], usemsg[1].text, usemsg[5].text, usemsg[17].text),  # %(硬卧，姓名，身份证，手机号)
        'oldPassengerStr': '%s,1,%s,3_' % (usemsg[1].text, usemsg[5].text),
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
        'passengerTicketStr': '%s,0,3,%s,1,%s,%s,N' % (
        dictory[seattype], usemsg[1].text, usemsg[5].text, usemsg[17].text),  # %(硬卧，姓名，身份证，手机号)
        'oldPassengerStr': '%s,1,%s,3_' % (usemsg[1].text, usemsg[5].text),
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
    p = session.post('https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue', data=form5_data,
                     headers=checkOrderInfo_head)
    print('confirmSingleForQueue' + p.text)
    # -----------------------queryOrderWaitTime-----------------------#
    timr = 0
    while True:
        k = session.get(
            'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random=%s&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN=%s' % (
            round(time.time() * 1000), RepeatSubmitToken), headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate,br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Host': 'kyfw.12306.cn',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest', })
        print('queryOrderWaitTime' + k.text)
        u = session.get(
            'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random=%s&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN=%s' % (
                round(time.time() * 1000), RepeatSubmitToken), headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate,br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Host': 'kyfw.12306.cn',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest', })
        print('queryOrderWaitTime' + u.text)

        timr+=1
        if(timr>5):break



login()



