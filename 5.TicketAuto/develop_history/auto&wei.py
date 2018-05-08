from numpy import *
import json
from urllib.parse import unquote,quote
import os
from requests import get, post, Session
from bs4 import BeautifulSoup
import time
import re

url ='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-05-13&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=SHH&purpose_codes=ADULT'
trainNO='G101'
fromcity='北京'
tocity='上海'
train_date='2018-05-13'
seattype='一等座'

str_login_site='E'
str_rand='sjrand'
def login(use='',pw=''):
    dictory = {'硬卧': 3, '软卧': 4, '硬座': 1,'一等座':'M'}
    def pick(num):
        answer = ''
        axis = ['37,45', '107,45', '182,45', '252,45',
                '37,115', '107,115', '182,115', '252,115']
        for x in num:
            answer += axis[x - 1] + ','
        return (answer[:-1])
    session = Session()
# -----------------------https://kyfw.12306.cn/otn/login/init-----------------------#

    session.get('https://kyfw.12306.cn/otn/login/init#', headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'kyfw.12306.cn',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",})
    time.sleep(1)
# -----------------------captcha-image?login_site=E&module=login&rand=sjrand&0.9725909596164388-------下载验证码----------------#
    captchaurl = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&'
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
    time.sleep(1)
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
        'rand': str_rand,
        'login_site': str_login_site,
    }
    captcha_response = session.post(check_url, data=captcha_data, headers=check_headers)
    print(captcha_response.text)
    time.sleep(1)
# -----------------------web/login-----------------------#
    login_url = 'https://kyfw.12306.cn/passport/web/login'
    form_data = {
        'username': use,
        'password': pw,
        'appid': 'otn',
    }
    log_response = session.post(login_url, data=form_data, headers=check_headers)
    print(log_response.text)
    # time.sleep(1)

# -----------------------userLogin-----------------------#
    session.post('https://kyfw.12306.cn/otn/login/userLogin', data={'_json_att': '', }, headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'kyfw.12306.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36', })
    # time.sleep(1)
# # -----------------------uamtk-----------------------#
#     session.post('https://kyfw.12306.cn/passport/web/auth/uamtk', data={'appid':'otn',}, headers={
#         'Accept': 'application/json, text/javascript, */*; q=0.01',
#         'Accept-Encoding': 'gzip, deflate,br',
#         'Accept-Language': 'zh-CN,zh;q=0.9',
#         'Host': 'kyfw.12306.cn',
#         'Origin': 'https://kyfw.12306.cn',
#         'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
#         'X-Requested-With': 'XMLHttpRequest',})
#     # time.sleep(1)
    # -----------------------uamtk-----------------------#
    uamtk_response1 = session.post('https://kyfw.12306.cn/passport/web/auth/uamtk', data={'appid': 'otn', }, headers={
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'kyfw.12306.cn',
        'Origin': 'https://kyfw.12306.cn',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
        'X-Requested-With': 'XMLHttpRequest', })
    # time.sleep(1)
    tk = json.loads(uamtk_response1.text)["newapptk"]


# # -----------------------redirect=/otn/login/userLogin-----------------------#
#     session.get('https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin', headers={
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#         'Accept-Encoding': 'gzip, deflate,br',
#         'Accept-Language': 'zh-CN,zh;q=0.9',
#         'Host': 'kyfw.12306.cn',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',})
#     time.sleep(1)

# -----------------------uamauthclient-----------------------#
    session.post('https://kyfw.12306.cn/otn/uamauthclient', data={'tk': tk, }, headers={
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'kyfw.12306.cn',
        'Origin': 'https://kyfw.12306.cn',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
        'X-Requested-With': 'XMLHttpRequest', })
    # time.sleep(1)
# -----------------------initMy12306-----------------------#
    session.get('https://kyfw.12306.cn/otn/index/initMy12306', headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'kyfw.12306.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36', })
    # time.sleep(1)
# -----------------------https://kyfw.12306.cn/otn/leftTicket/init-----------------------#
    session.get('https://kyfw.12306.cn/otn/leftTicket/init', headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'kyfw.12306.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',})

# -----------------------查票获取secretStr-----------------------#
    # session.get('https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=passenger&rand=randp&0.051538683369815263',
    #             headers={
    #                 'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    #                 'Accept-Encoding': 'gzip, deflate,br',
    #                 'Accept-Language': 'zh-CN,zh;q=0.9',
    #                 'Host': 'kyfw.12306.cn',
    #                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36', })
    # time.sleep(1)
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
    # time.sleep(1)
    jsonstr = json.loads(reply.text)
    trainlist = jsonstr['data']['result']
    for x in trainlist:
        if x.find(trainNO) != -1:
            # print(x)
            trainmsglist = x.split('|')

    # time.sleep(1)

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
        # time.sleep(1)
# -----------------------submitOrderRequest-----------------------#
    form2_data = {
        'secretStr': unquote(trainmsglist[0]),#trainmsglist[0] 字符串要先解码，因为放到 post 请求里后会再编码,这是最大一个坑，找了一天!!! 感谢http://tiven.wang/train-api/提示
        'train_date':train_date,
        'back_train_date':time.strftime("%Y-%m-%d", time.localtime()),
        'tour_flag':'dc',
        'purpose_codes':'ADULT',
        'query_from_station_name':fromcity,
        'query_to_station_name':tocity,
        # 'undefined':''
    }
    re0=session.post('https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest', data=form2_data, headers=query_headers)
    print('submitOrderRequest:'+re0.text)
    # time.sleep(1)
# -----------------------confirmPassenger/initDc-----------------------#
    re1=session.post('https://kyfw.12306.cn/otn/confirmPassenger/initDc',headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9',
'Cache-Control':'max-age=0',
'Content-Type':'application/x-www-form-urlencoded',
'Host':'kyfw.12306.cn',
'Origin':'https://kyfw.12306.cn',
'Referer':'https://kyfw.12306.cn/otn/leftTicket/init',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',}, data={'_json_att': '', })
    # confirm_html = BeautifulSoup(re1.text, "html.parser")
    # RepeatSubmitToken = confirm_html.find_all('script')[0].text.split(';')[1].split('=')[1][2:-1]
    train_no_pat = "'train_no':'(.*?)'"
    leftTicketStr_pat = "'leftTicketStr':'(.*?)'"
    fromStationTelecode_pat = "from_station_telecode':'(.*?)'"
    toStationTelecode_pat = "'to_station_telecode':'(.*?)'"
    train_location_pat = "'train_location':'(.*?)'"
    pattoken = "var globalRepeatSubmitToken.*?'(.*?)'"
    patkey = "'key_check_isChange':'(.*?)'"
    req7data=re1.text
    train_no_all = re.compile(train_no_pat).findall(req7data)
    if (len(train_no_all) != 0):
        train_no = train_no_all[0]
    else:
        raise Exception("train_no获取失败")
    leftTicketStr_all = re.compile(leftTicketStr_pat).findall(req7data)
    if (len(leftTicketStr_all) != 0):
        leftTicketStr = leftTicketStr_all[0]
    else:
        raise Exception("leftTicketStr获取失败")
    fromStationTelecode_all = re.compile(fromStationTelecode_pat).findall(req7data)
    if (len(fromStationTelecode_all) != 0):
        fromStationTelecode = fromStationTelecode_all[0]
    else:
        raise Exception("fromStationTelecod获取失败")
    toStationTelecode_all = re.compile(toStationTelecode_pat).findall(req7data)
    if (len(toStationTelecode_all) != 0):
        toStationTelecode = toStationTelecode_all[0]
    else:
        raise Exception("toStationTelecode获取失败")
    train_location_all = re.compile(train_location_pat).findall(req7data)
    if (len(train_location_all) != 0):
        train_location = train_location_all[0]
    else:
        raise Exception("train_location获取失败")
    tokenall = re.compile(pattoken).findall(req7data)
    if (len(tokenall) != 0):
        token = tokenall[0]
    else:
        raise Exception("Token获取失败")
    keyall = re.compile(patkey).findall(req7data)
    if (len(keyall) != 0):
        key = keyall[0]
    else:
        raise Exception("key_check_isChange获取失败")

    # RepeatSubmitToken = re.findall("var globalRepeatSubmitToken = '(\w+)';", re1.text)[0]
    # key_check_isChange=re.findall("'key_check_isChange':'(\w+)','leftDetails'", re1.text)[0]
    # token=RepeatSubmitToken
    # key=key_check_isChange
    # print(RepeatSubmitToken)
    # time.sleep(2)
# 新加入-----------------------getPassengerDTOs-----获取个人身份证，手机号信息------------------#
#     time.sleep(1)
    usemsg_html = BeautifulSoup(
        session.post('https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs', data={"REPEAT_SUBMIT_TOKEN":token,}, headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'kyfw.12306.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36', }).text,
        "html.parser")
    req8data=usemsg_html.text
    # 获取用户信息
    # 提取姓名
    namepat = '"passenger_name":"(.*?)"'
    # 提取身份证
    idpat = '"passenger_id_no":"(.*?)"'
    # 提取手机号
    mobilepat = '"mobile_no":"(.*?)"'
    # 提取对应乘客所在的国家
    countrypat = '"country_code":"(.*?)"'
    nameall = re.compile(namepat).findall(req8data)
    idall = re.compile(idpat).findall(req8data)
    mobileall = re.compile(mobilepat).findall(req8data)
    countryall = re.compile(countrypat).findall(req8data)
    # 选择乘客

    # 输出乘客信息，由于可能有多位乘客，所以通过循环输出
    for i in range(0, len(nameall)):
        print("第" + str(i + 1) + "位用户,姓名:" + str(nameall[i]))
#     chooseno = input("请选择要订票的用户的序号，此处只能选择一位哦，如需选择多\
# 位，可以自行修改一下代码")
        chooseno = 2
    # thisno为对应乘客的下标，比序号少1，比如序号为1的乘客在列表中的下标为0
    thisno = int(chooseno) - 1

    time.sleep(5)
# -----------------------checkOrderInfo-----------------------#
    form3_data={
        'cancel_flag':'2',
        'bed_level_order_num':'000000000000000000000000000000',
        'passengerTicketStr':"M,0,3,"+str(nameall[thisno])+",1,"+str(idall[thisno])+",\
"+str(mobileall[thisno])+",N",
        'oldPassengerStr':str(nameall[thisno])+",1,"+str(idall[thisno])+",3_",
        'tour_flag':'dc',
        'randCode':'',
        'whatsSelect':'1',
        '_json_att':'',
        'REPEAT_SUBMIT_TOKEN':token,
    }
    checkOrderInfo_head={'Accept':'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection': 'keep - alive',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'Host':'kyfw.12306.cn',
'Origin':'https://kyfw.12306.cn',
'Referer':'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
'X-Requested-With':'XMLHttpRequest',}

    print('checkOrderInfo:'+session.post('https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo',headers=checkOrderInfo_head, data=form3_data).text)
    # time.sleep(2)
# -----------------------initQueryUserInfo-----获取个人身份证，手机号信息------------------#
#     time.sleep(1)
#     usemsg_html = BeautifulSoup(session.post('https://kyfw.12306.cn/otn/modifyUser/initQueryUserInfo', data={'_json_att':''}, headers={
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#         'Accept-Encoding': 'gzip, deflate,br',
#         'Accept-Language': 'zh-CN,zh;q=0.9',
#         'Host': 'kyfw.12306.cn',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36', }).text, "html.parser")
#     usemsg =usemsg_html.select('div[class="con"]')


# ----------------------------------------------#
#     p=session.get('https://kyfw.12306.cn/otn/HttpZF/logdevice?algID=RcHOncNR3i&hashCode=4CN16hiCWZSoP2EuwU4ZN9aiI4GbSs9Em45NB-tGbBM&FMQw=0&q4f3=zh-CN&VySQ=FGHldLUbosbDgpJq7AtDcvbufjSwXH2s&VPIf=1&custID=133&VEek=unknown&dzuS=29.0%20r0&yD16=0&EOQP=8f58b1186770646318a429cb33977d8c&lEnu=3396734384&jp76=bb5032aedcaa9cca45f29e44506d1288&hAqN=Win32&platform=WEB&ks0Q=93b5994b1daea02ec4a30a4f9c1a569c&TeRS=1040x1920&tOHY=24xx1080x1920&Fvje=i1l1o1s1&q5aJ=-8&wNLf=99115dfb07133750ba677d055874de87&0aew=Mozilla/5.0%20(Windows%20NT%206.1;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/64.0.3282.186%20Safari/537.36&E3gR=4fd3e2483e3e7ce617e5307727b0c4e8&timestamp={}'.format(round(time.time()*1000)),
#                 headers={
#                     'Accept': '*/*',
#                     'Accept-Encoding': 'gzip, deflate,br',
#                     'Accept-Language': 'zh-CN,zh;q=0.9',
#                     'Host': 'kyfw.12306.cn',
#                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36', })
#     time.sleep(2)

# -----------------------getQueueCount-----------------------#
    form4_data={
        'train_date':time.strftime('%a %b %d %Y 00:00:00 GMT%z ',time.strptime(train_date,'%Y-%m-%d'))+'(中国标准时间)',
        'train_no':train_no,
        'stationTrainCode':trainmsglist[3],
        'seatType':dictory[seattype],
        'fromStationTelecode':fromStationTelecode,
        'toStationTelecode':toStationTelecode,
        'leftTicket':leftTicketStr,
        'purpose_codes':'00',
        'train_location':train_location,
        '_json_att':'',
        'REPEAT_SUBMIT_TOKEN':token,
    }
    print('getQueueCount:'+session.post('https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount',headers=checkOrderInfo_head, data=form4_data).text)
    # time.sleep(2)
# -----------------------confirmSingleForQueue-----------------------#
    form5_data={
        'passengerTicketStr':"M,0,3,"+str(nameall[thisno])+",1,"+str(idall[thisno])+",\
"+str(mobileall[thisno])+",N",
        'oldPassengerStr':str(nameall[thisno])+",1,"+str(idall[thisno])+",3_",
        'randCode':'',
        'purpose_codes':'00',
        'key_check_isChange': key,
        'leftTicketStr': leftTicketStr,
        'train_location': train_location,
        'choose_seats':'',
        'seatDetailType':'000',
        'whatsSelect': '1',
        'roomType': '00',
        'dwAll': 'N',
        '_json_att':'',
        'REPEAT_SUBMIT_TOKEN':token,
    }
    p=session.post('https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue', data=form5_data,headers=checkOrderInfo_head)
    print('confirmSingleForQueue'+p.text)
    # time.sleep(1)
# -----------------------queryOrderWaitTime-----------------------#
    time2=0
    while True:
        k=session.get('https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random={}&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN={}'.format(str(round(time.time()*1000)),token), headers={
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'kyfw.12306.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',})
        print('queryOrderWaitTime'+k.text)
        # time.sleep(4)
        u=session.get(
            'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random={}&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN={}' .format (
                round(time.time() * 1000), token), headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate,br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Host': 'kyfw.12306.cn',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest', })
        print('queryOrderWaitTime'+u.text)
        time2+=1
        if (time2  > 5):
            print("获取orderid超时，正在进行新一次抢购")
            break
login()



