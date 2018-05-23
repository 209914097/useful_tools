#第三方"真·人工智能"打码平台接口
#关于安全:检查程序发现并没把12306的cookies携带访问第三方打码平台,请放心
import requests
from hashlib import md5
import time
class RClient(object):

    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()

if __name__ == '__main__':
    start = time.clock()
    rc = RClient('用户名', '用户密码'.encode("utf-8"), '软件ID', '软件Key')#敏感信息
    im = open('a.jpg', 'rb').read()
    print (rc.rk_create(im, 6113))#{'Result': '15', 'Id': 'c6a17f00-0d9d-4474-977c-f77929860f28'}

    elapsed = (time.clock() - start)
    print(elapsed)#4.087422691687358

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )