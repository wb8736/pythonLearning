"""
Author: BIN WANG
Time: 16:05
"""
from utils import template
import uuid
from utils import log
from utils import http_response
from utils import redirect
from routes import session
from routes import current_user
from models.users import User


def route_index(request):
    uid = current_user(request)
    u = User.model_find_by(id=uid)
    log("route index uid: ({}) session: ({})".format(uid, session))
    data = {
        "username": u.username
    }
    # log("template {}".format(template("index.html", data=data)))
    body = template("index.html", data=data)
    r = http_response(body, request.headers)
    return r


def route_static(request):
    filename = request.query.get('file', "")
    path = 'static/' + filename
    with open(path, "rb") as f:
        header = b'HTTP/1.1 200 OK\r\n'
        img = f.read()
        r = header + b'\r\n' + img
        return r


def route_register(request):
    result = ''
    if request.method == "POST":
        form = request.form()
        u = User(form)

        if u.validate_register():
            u.model_add()
            result = "注册成功"
        else:
            result = "注册失败"
    body = template("register.html", result=result)
    r = http_response(body, request.headers)
    return r


def route_login(request):
    result = ""
    if request.method == "POST":
        form = request.form()
        u = User.model_find_by(**form)
        try:
            if u.validate_login():
                session_id = str(uuid.uuid4())
                session[session_id] = u.id
                request.headers["Set-Cookie"] = "user={}".format(session_id)
                log("route login {} session ({}): 登录成功！".format(u.username, session))
                return redirect(request.headers, "/")
            else:
                result = "登录失败"
        except Exception as e:
            result = "用户名或密码错误"
    body = template("login.html", result=result)
    r = http_response(body, request.headers)
    return r


route_main = {
    "/": route_index,
    "/index": route_index,
    "/register": route_register,
    "/login": route_login,
}