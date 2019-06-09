import re
from urllib.parse import urlencode

import requests
import json
import random


def spider():
    sess = requests.Session()

    url = 'http://xk.zucc.edu.cn/CheckCode.aspx'
    code_res = sess.get(url)

    url = 'http://63.211.111.82:19952/captcha/v3'
    identification_res = sess.post(url, data=code_res.content)
    code = json.loads(identification_res.text)['message']
    print(code)

    sess.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'Referer': 'http://xk.zucc.edu.cn/default2.aspx'
    }

    url = 'http://xk.zucc.edu.cn/default2.aspx'
    data = {
        '__VIEWSTATE': 'dDwxNTMxMDk5Mzc0Ozs+HjPJ2APgB+73zYSyRsZkjFxlx0A=',
        'txtUserName': 'username',
        'Textbox1': '',
        'TextBox2': 'password',
        'txtSecretCode': code,
        'RadioButtonList1': '学生',
        'Button1': '',
        'lbLanguage': '',
        'hidPdrs': '',
        'hidsc': ''
    }
    data = urlencode(data, encoding='gb2312')
    login_res = sess.post(url, data=data)
    login_res.encoding = 'gb2312'
    info = re.search(r"alert\('(.*?)'\);", login_res.text).group(1)
    print(info)

    if '验证码' not in info:
        with open('data/{}_{}.jpg'.format(code, random.randint(100000, 999999)), 'wb') as f:
            f.write(code_res.content)


if __name__ == '__main__':
    while 1:
        spider()
