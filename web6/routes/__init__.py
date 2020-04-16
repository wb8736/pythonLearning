"""
Author: BIN WANG
Time: 15:35
"""
from utils import redirect
from utils import log
from models.users import User

session = dict()


# 获取当前用户
def current_user(request):
    session_id = request.cookies.get("user", -1)
    user_id = session.get(session_id, -1)
    log("current user {}".format(user_id))
    return user_id


# 判断是否登录
def is_login(func):
    def inner(request):
        uid = current_user(request)
        if uid == -1:
            url = "/login"
            return redirect(request.headers, url)
        else:
            return func(request)
    return inner


# 判断是否为admin
def is_admin(func):
    def inner(request):
        uid = current_user(request)
        u = User.model_find_by(id=int(uid))
        if u.is_admin():
            return func(request)
        else:
            return redirect(request.headers, "/")
    return inner




