'''
测试版本
http://123.57.138.40:9443/
功能:通过图片进行人工智能识别
本接口请勿使用于商业行为,供学习参考用
识别率:文字99.7%,图片98%
算法:Dense
运算方式: CPU
识别时间:6至8秒(不含网络时间)
---------------------------------
商业版本
识别率:文字99.7%,图片98%
算法:Dense
运算方式: GPU
识别时间:0.5至1.7秒(不含网络时间)
商业合作请加QQ: 2269778308
QQ群:627132523(曙光识别)
'''
import requests

if __name__ == '__main__':
    url = 'http://123.57.138.40:8000/12306/code'
    data = {'user': '123','key': '111111'}
    # 将以下image_url替换为您的验证码路径
    image_url = '22.jpg'
    files = {'file': open(image_url, 'rb')}
    response = requests.post(url, data=data, files=files)
    print(response.text)
    # 返回结果如下,商业版本支持接口定制
    # {"time": "6.590874s", "msg": "success", "code": 0, "text": "电子秤", "result": [6]}


