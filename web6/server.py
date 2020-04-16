"""
Author: BIN WANG
Time: 16:59
"""
import socket
import urllib.parse
import _thread

from models.users import User
from routes.todo_routes import route_todo
from request import Request
from routes.admin_routes import route_admin
from routes.main_routes import (
    route_static,
    route_main,
)
from utils import (
    log,
    error,
    parsed_path,
)


def response_for_path(path, request):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    log('path and query', path, query)
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = {
        '/static': route_static,
    }
    # 注册外部的路由
    r.update(route_main)
    r.update(route_todo)
    r.update(route_admin)
    # r.update(api_todo)
    # r.update(user_routes)
    # r.update(todo_routes)
    # r.update(weibo_routes)
    #
    response = r.get(path, error)
    return response(request)



def process_request(conn):
    r = conn.recv(1024)
    r = r.decode('utf-8')
    log("请求结束 ({})".format(r), flush=True)
    if len(r) < 2:
        conn.close()
    else:
        request = Request()
        # todo debug log
        # log("request {}".format(dir(request)), flush=True)
        request.method = r.split()[0]
        path = r.split()[1]
        request.add_headers(r.split("\r\n\r\n", 1)[0].split("\r\n")[1:])
        request.body = r.split("\r\n\r\n", 1)[1]
        response = response_for_path(path, request)

        conn.sendall(response)
        log("响应完成 response {}".format(response))
        conn.close()


def run(host="", port=3000):
    log("start at {}:{}".format(host, port), flush=True)
    with socket.socket() as s:
        s.bind((host, port))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            log("连接成功 {}".format(addr), flush=True)
            _thread.start_new_thread(process_request, (conn,))
            # process_request(conn)


if __name__ == "__main__":
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
