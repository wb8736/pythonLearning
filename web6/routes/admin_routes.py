"""
Author: BIN WANG
Time: 17:27
"""
from utils import template
from utils import log
from utils import http_response
from utils import redirect
from routes import is_admin
from routes import current_user
from routes import is_login
from models.users import User


@is_admin
@is_login
def route_admin_index(request):
    # uid = current_user(request)
    # u = User.model_find_by(id=int(uid))
    # if u.role != 1:
    #     return redirect(request.headers, "/")
    if request.method == "POST":
        return redirect(request.headers, "/register")
    else:
        users = User.model_all()
        # users = [user for user in users if user.get_deleted() != False]
        users = User.model_validate_all(users)
        body = template("users.management.html", users=users)
        return http_response(body, request.headers)


@is_admin
@is_login
def route_admin_user_add(request):
    form = request.form()
    u = User(form)
    u.role = int(u.role)
    if u.validate_register():
        u.model_add()
    return redirect(request.headers, "/user/list")


@is_admin
@is_login
def route_admin_user_delete(request):
    uid = request.query.get("id", -1)
    if uid != -1:
        User.model_delete(id=int(uid))
    return redirect(request.headers, "/user/list")


@is_admin
@is_login
def route_admin_user_edit(request):
    uid = request.query.get("id", -1)
    if uid != -1:
        if request.method == "POST":
            form = request.form()
            if form.get("password", ""):
                User.model_edit(form, id=int(uid))
            return redirect(request.headers, "/user/list")
        else:
            user = User.model_find_by(id=int(uid))
            body = template("user.edit.html", user=user)
            return http_response(body, request.headers)
    return redirect(request.headers, "/user/list")



route_admin = {
    "/user/list": route_admin_index,
    "/user/add": route_admin_user_add,
    "/user/delete": route_admin_user_delete,
    "/user/edit": route_admin_user_edit,
}
