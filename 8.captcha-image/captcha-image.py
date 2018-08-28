"""
一个疑似河南郑州大学的网站接口，使用方法可参照该网站
http://122.114.198.116/
"""
from requests import get, post, Session
from urllib.parse import urlencode
import base64

session = Session()
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

session2 = Session()
url='http://122.114.198.116/12306/getResult'
urlheaders={
'cache-control':"no-cache",
'postman-token':"0f5db8dc-c930-416b-199d-336667c7d6c7",
'Content-Type':"application/x-www-form-urlencoded",
}

with open("captcha-image.jpg", "rb") as f:
    # b64encode是编码，b64decode是解码
    base64_data = base64.b64encode(f.read())
    # base64.b64decode(base64data)

captcha_data={"base64":base64_data}
print((captcha_data))
reply=session2.post(url, data=urlencode(captcha_data), headers=urlheaders)
# 打印图片坐标
print(reply.text)
