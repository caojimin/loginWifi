# -*- coding:utf-8 -*-
import re
import threading
import time
import requests
import os

username = ''
password = ''

logs = {
    'status': '未启动',
    'login_times': 0,
    'last_login_time': 0,
}


class int2time:
    @staticmethod
    def strtime(t):
        time_local = time.localtime(int(t))
        return time.strftime("%Y-%m-%d %H:%M:%S", time_local)


class AutoLogin(threading.Thread):
    postform = {
        'is_auto_land': 'false',
        'usernameHidden': username,
        'username_tip': 'Username',
        'username': username,
        'strTypeAu': '',
        'uuidQrCode': '',
        'authorMode': '',
        'pwd_tip': 'Password',
        'pwd': password
    }
    ISOTIMEFORMAT = '%Y-%m-%d %X'

    def __init__(self):
        threading.Thread.__init__(self)

    @staticmethod
    def getstatus():
        try:
            r = requests.get('http://www.baidu.com')
            array = r.text.split("'")
            if array[0] == '<script>top.self.location.href=':
                logs['status'] = "正在重连"
                return 1
            else:
                logs['status'] = "已连接"
                return 0
        except Exception:
            logs['status'] = "网络未连接"
            return 2

    def login(self):
        r = requests.get('http://www.baidu.com')
        info = re.findall(r"index.jsp\?(.*)'</script>", r.text)
        post_url = "http://10.0.0.12/eportal/userV2.do?method=login&param=true&" + info[0]
        requests.post(post_url, data=self.postform)
        logs['login_times'] += 1
        logs['last_login_time'] = time.time()

    def run(self):
        while True:
            status = self.getstatus()
            if status == 0:
                time.sleep(5)
            if status == 1:
                self.login()
                time.sleep(5)
            if status == 2:
                time.sleep(5)


if __name__ == '__main__':
    try:
        master = AutoLogin()
        master.setDaemon(True)
        master.start()
        while True:
            os.system("cls")
            print("\033[1;34m(按 ctrl+c 退出)\033[0m")
            if logs['status'] == "已连接":
                print("状态:\033[1;32m%s\033[0m" % logs['status'])
            elif logs['status'] == "正在重连":
                print("状态:\033[1;33m%s\033[0m" % logs['status'])
            else:
                print("状态:\033[1;31m%s\033[0m" % logs['status'])
            print("登录次数:%d" % logs['login_times'])
            print("上次登录时间:%s" % int2time.strtime(logs['last_login_time']))
            print("当前时间:%s" % int2time.strtime(time.time()))
            time.sleep(1)
    except KeyboardInterrupt:
        print("程序已结束")

