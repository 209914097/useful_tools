### bug修复记录:
checkOrderInfo前需要延时。不然12306会认为使用抢票软件进入死排队
<br>
getQueueCount的表单改动了两处：
<br>
(1)'train_no': trainmsglist[2],
<br>
(2)'fromStationTelecode': trainmsglist[6],
<br>
### 感谢：
(1)https://zhuanlan.zhihu.com/p/36234946?utm_medium=social&utm_member=ZTdjODE2NmNlMmE4ZTY4YmM5YzNmNTZiMGJiMmJlZWM%3D&utm_source=qq
<br>
根据韦玮的代码改动了getQueueCount的表单，在checkOrderInfo前进行延时摆脱死排队
<br>
我的代码个人身份证手机号是从12306查看个人信息页面获取的，他的是从确认订单接口getPassengerDTOs获取
<br>
(2)https://blog.csdn.net/lzqwebsoft/article/details/18674635
<br>
帮我找到REPEAT_SUBMIT_TOKEN从那里获取
<br>
(3)http://tiven.wang/train-api/
<br>
帮我解决了一个未解之谜，提示我secretStr需要解码
<br>
(4)https://github.com/testerSunshine/12306
<br>
这个项目开发团队当时和我一样遇到了死排队问题，他们推荐了我韦玮的代码
<br>

### 以下内容则增长了我的见识
<br>
(5)https://zhuanlan.zhihu.com/p/31865300
<br>
(7)http://www.cnblogs.com/guozili/p/6144561.html
<br>
(8)https://www.lanindex.com/12306%E8%B4%AD%E7%A5%A8%E6%B5%81%E7%A8%8B%E5%85%A8%E8%A7%A3%E6%9E%90/
<br>

### 感想:
蒲苇韧如丝，磐石无转移。<br>
12306对反爬虫反黄牛的决心是坚持不懈的，它正从一个很烂的网站逐步成长起来。<br>
它的反爬虫技术主要体现在：<br>
(1)变化的查票url<br>
(2)设置各种复杂奇葩很长的令牌cookies，这意味着必须像正常购票一样访问特定的买票流程页面。这些令牌大部分如tk是通过xhr数据返回，相对好找，key_check_isChange和RepeatSubmitToken则是访问特定html中包含的JavaScript变量里才有，十分难找。<br>
有些令牌是在访问特别的url之后获得的，但它会马上跳转至新页面，这意味着用Chrome抓包，一旦跳转至新页面，这个特别的url包会一下子刷没，故需把Chrome中Network网速放慢<br>
(3)延时机制，订单提交太快将进入死排队<br>
不得不感慨:代码写了2天，找bug用了3天!!<br>
