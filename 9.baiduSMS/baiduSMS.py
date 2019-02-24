from requests import get, post, Session, packages
PhoneNum='手机号'
verify_url='https://wappass.baidu.com/wp/api/login/sms?tt=1550846213102'
http = Session()
http.headers.update({
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0.2; MI 2 Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Host':'wappass.baidu.com',

    'Referer': 'https://wappass.baidu.com/passport/?sms=1&clientfrom=&adapter=0&ssid=&from=&authsite=1&bd_page_type=&uid=1550842409497_168&pu=&tpl=netdisk&u=https://pan.baidu.com/wap/home%3FrealName%3D1%26wapBehaviorLog%3Dwap_click_welcome_login%26branchType%3DSMSlogin%26uid%3D1550842409497_168%26traceid%3D69321303&type=&bdcm=9ee1df0df8198618477adab44aed2e738ad4e693&tn=&regist_mode=&login_share_strategy=&subpro=&skin=default_v2&client=&connect=0&smsLoginLink=1&loginLink=&bindToSmsLogin=&overseas=1&is_voice_sms=&subpro=&traceid=69321303&hideSLogin=&forcesetpwd=&nousername=&regdomestic=1&extrajson='})
respond = http.request(method='post',
                                                   timeout=12,
                                                   url=verify_url,
                                                   allow_redirects=False,
                                                   verify=False,
data={'countrycode': '', 'gid': 'C878816-40EC-4EAD-A276-7F334168E9BE', 'vcodesign': '', 'vcodestr': '', 'dialogVerifyCode': '', 'clientfrom': 'wap', 'sub_source': '', 'is_voice_sms': '0', 'dv': 'tk0.451561236142381971550846213739%40v-ffEBfxrOqFFhxli8Qw~8DwyFlmLnSwp1Bf8vtz8vsP910y818x8vOa8vtf8kUy91s~8PFP4B__ilLp5IgHnIYE7l3Hq__Glc8mwwpk8z8mwf8vUS8P2wpk2y8mwP91qS8P2wpkt~4q__', 'username': PhoneNum, 'tpl': 'netdisk', 'subpro': '', 'traceid': '69321303'},
 cookies={'BAIDUID': 'C30BCE72C1D0AAB35758B5EBE7EB55E7:FG=1', 'rsv_i': '704013wBEmh%2Fas7dihwy6JxockygCqyCK%2B6y6FNZZb7R77IexwuQ12A64foYhztTUMSHZQ68FEbRrOb2NeM9%2FRGQKpFP13M', 'FEED_SIDS': '635321_0220_18', 'BDORZ': 'AE84CDB3A529C0F8A2B9DCDD1D18B695', 'SE_LAUNCH': '5%3A25847188', 'H_WISE_SIDS': '126126_128356_128701_113879_128068_125124_120176_123019_118896_118877_118844_118825_118788_107313_129180_129388_129088_117327_117433_128402_124629_129010_129559_128968_128247_129294_128805_129521_129287_127761_129480_129375_124030_129513_110085_123290_129270_128524_128600_128195_128962_100458', 'delPer': '0', 'PSINO': '6', 'BAIDU_WISE_UID': 'wpass_1550846185615_93', 'HISTORY': 'e95067aee7e0;'}

,)
print(respond.text)
