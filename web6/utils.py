"""
Author: BIN WANG
Time: 16:49
"""
import time
import json
import os
from jinja2 import Environment, FileSystemLoader


def log(*args, **kwargs):
    time_format = "%Y/%m/%d %H:%M:%S"
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    print(dt, *args, **kwargs)


def parsed_path(path):
    index = path.find("?")
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split("?", 1)
        args = query_string.split("&")
        query = {}
        for arg in args:
            k, v = arg.split("=")
            query[k] = v
        return path, query


def data_load(path):
    """
    本函数用于将json文件读入转换为list或dict
    :param path: json文件路径
    :return: dict或list
    """
    with open(path, "r+", encoding="utf-8") as f:
        s = f.read()
        log("Data Load: {}".format(s))
        return json.loads(s)


def data_save(path, data):
    """
    本函数是将一个list或dict写入文件
    :param path: 存储文件路径
    :param data: list或dict
    :return:
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, "w+", encoding="utf-8") as f:
        f.write(s)


# 获取模板路径
template_path = "{}/templates".format(os.path.dirname(__file__))
# 常见一个加载器，jinja2或从这个目录加载模板
loader = FileSystemLoader(template_path)
# 用加载创建一个，可以读取模板文件的环境
env = Environment(loader=loader)


def template(path, **kwargs):
    """
    :param path: "index.html"
    :param kwargs:
    :return:
    """
    t = env.get_template(path)
    return t.render(**kwargs)


def response_with_headers(headers, status_code=200):
    header = "HTTP/1.1 {} OK\r\n".format(status_code)
    header += "".join(['{}: {}\r\n'.format(k, v) for
                       k, v in headers.items()])
    return header


def redirect(headers, location):
    headers['Location'] = location
    header = response_with_headers(headers, 302)
    r = header + '\r\n' + ''
    return r.encode(encoding='utf-8')


def error(request, code=404):
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def http_response(body, headers=None):
    if headers is not None:
        headers["Content-Type"] = "text/html"
        if headers.get("Content-Length"):
            headers.pop("Content-Length")
        header = response_with_headers(headers)
    r = header + "\r\n" + body
    return r.encode(encoding="utf-8")
    # header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    # if headers is not None:
    #     header += ''.join(['{}: {}\r\n'.format(k, v)
    #                        for k, v in headers.items()])
    # r = header + '\r\n' + body
    # return r.encode(encoding='utf-8')


def json_response(data, headers=None):
    if headers is not None:
        headers["Content-Type"] = "application/json"
        header = response_with_headers(headers)
        body = json.dumps(data, indent=2, ensure_ascii=False)
        r = header + "\r\n" + body
        return r.encode(encoding='utf-8')



