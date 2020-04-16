"""
Author: BIN WANG
Time: 17:00
"""
import urllib


class Request(object):

    def __init__(self):
        self.headers = {}
        self.cookies = {}
        self.query = {}
        self.method = 'GET'
        self.body = ''
        self.path = ''

    def add_cookies(self):
        """
        height=169; user=gua
        :return:
        """
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split("; ")
        for kv in kvs:
            if "=" in kv:
                k, v = kv.split("=")
                self.cookies[k] = v

    def add_headers(self, header):
        """
        :param header: list
        [
            'Accept-Language: zh-CN,zh;q=0.8',
            'Cookie: height=169; user=gua'
        ]
        :return:
        """
        lines = header
        for line in lines:
            k, v = line.split(": ", 1)
            self.headers[k] = v
        # 清理cookies
        self.cookies = {}
        self.add_cookies()

    def form(self):
        args = self.body.split('&')
        args = [urllib.parse.unquote(arg) for arg in args]
        f = dict()
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f
