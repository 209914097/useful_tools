import os
from requests import Session
from rk import RClient
import json

class login:
    def __init__(self,use,pw,AIcaptcha):
        self.use=use
        self.pw=pw
        self.AIcaptcha=AIcaptcha
        self.session = Session()

    def pick(self,num):
        answer = ''
        axis = ['37,45', '107,45', '182,45', '252,45',
                '37,115', '107,115', '182,115', '252,115']
        for x in num:
            answer += axis[x - 1] + ','
        return (answer[:-1])

    def golog(self):
        # -----------------------https://kyfw.12306.cn/otn/login/init-----------------------#
        self.session.get('https://kyfw.12306.cn/otn/login/init', headers={
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
        checkcodecontent = self.session.get(captchaurl, headers=captchaheaders)
        with open('captcha-image.jpg', 'wb') as f:
            f.write(checkcodecontent.content)

        if self.AIcaptcha:
        # -----------------------验证码"真·人工智能"识别-----------------------#
            rc = RClient('用户名', '用户密码'.encode("utf-8"), '软件ID', '软件Key')#敏感信息
            im = open('captcha-image.jpg', 'rb').read()
            im_num =rc.rk_create(im, 6113)
            checkcode = [int(x) for x in list(im_num['Result'])]
            checkcode = self.pick(checkcode)
        # -----------------------验证码手动识别-----------------------#
        else:
            os.startfile('captcha-image.jpg')
            print(
                """
                -----------------
                | 1 | 2 | 3 | 4 |
                -----------------
                | 5 | 6 | 7 | 8 |
                -----------------
                """
            )
            checkcode = [int(x) for x in input('输入图片序号用,分隔:').split(',')]
            checkcode = self.pick(checkcode)
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
        captcha_response = self.session.post(check_url, data=captcha_data, headers=check_headers)
        print(captcha_response.text)
        if (captcha_response.json()["result_message"]=="验证码校验失败"):
            raise Exception("验证码校验失败")

        # -----------------------web/login-----------------------#

        login_url = 'https://kyfw.12306.cn/passport/web/login'
        form_data = {
            'username': self.use,
            'password': self.pw,
            'appid': 'otn',
        }
        log_response = self.session.post(login_url, data=form_data, headers=check_headers)
        print(log_response.text)
        # -----------------------userLogin-----------------------#
        self.session.post('https://kyfw.12306.cn/otn/login/userLogin', data={'_json_att': '', }, headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'kyfw.12306.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36', })

        # -----------------------uamtk-----------------------#
        uamtk_response1 = self.session.post('https://kyfw.12306.cn/passport/web/auth/uamtk', data={'appid': 'otn', }, headers={
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
            'X-Requested-With': 'XMLHttpRequest', })
        tk = json.loads(uamtk_response1.text)["newapptk"]
        # -----------------------uamauthclient-----------------------#
        self.session.post('https://kyfw.12306.cn/otn/uamauthclient', data={'tk': tk, }, headers={
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
            'X-Requested-With': 'XMLHttpRequest', })

        return self.session


if __name__ == '__main__':
    Auth=login('12306账户','12306密码',False)#敏感信息
    Auth.golog()