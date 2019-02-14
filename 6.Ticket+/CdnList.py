from requests import get, post, Session, packages
import random
import datetime
import json
class CDN(object):
    def __init__(self):
        self.cdn_list=[]

    def cdn_verify(self,urlstr):
        cdn_cache=[]
        for cdn_IP in self.cdn_list:
            verify_url = urlstr.replace('kyfw.12306.cn', cdn_IP, 1)
            http = Session()
            packages.urllib3.disable_warnings()
            http.headers.update({
                                       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) 12306-electron/1.0.1 Chrome/59.0.3071.115 Electron/1.8.4 Safari/537.36',
                                       'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive',
                                       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                       'Referer': 'https://kyfw.12306.cn/otn/index/init', 'Host': 'kyfw.12306.cn'})
            try:
                start_time=datetime.datetime.now()
                respond = http.request(method='get',
                                                   timeout=2,
                                                   url=verify_url,
                                                   allow_redirects=False,
                                                   verify=False)
                if respond.status_code==200 and (datetime.datetime.now() - start_time).microseconds / 1000 < 500 and json.loads(respond.text)['status']:
                    cdn_cache.append(cdn_IP)
            except Exception as e:
                print(e)
                continue
        with open('cdn_verify_cache', "w") as f:
            for cdn_IP in cdn_cache:
                f.write(cdn_IP+'\n')

    def load_cdnfile(self,filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for i in f.readlines():
                if i.strip():
                    self.cdn_list.append(i.strip())

    def random_cdnurl(self,urlstr):
        cdn_IP=self.cdn_list[random.randint(0, len(self.cdn_list) - 1)]
        return  urlstr.replace('kyfw.12306.cn', cdn_IP, 1)

if __name__ == '__main__':
    url='https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2019-03-01&leftTicketDTO.from_station=GZQ&leftTicketDTO.to_station=SBT&purpose_codes=ADULT'
    cdn=CDN()
    cdn.load_cdnfile('cdn_list')
    cdn.cdn_verify(url)
    cdn.load_cdnfile('cdn_verify_cache')
    print(cdn.random_cdnurl(url))