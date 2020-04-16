"""
Author: BIN WANG
Time: 15:02
"""

from utils import log
from utils import http_response
from utils import template
from utils import redirect
from routes import current_user

from routes import session
from models.users import User
from models.todo import Todo

from routes import is_login


@is_login
def route_todo_list(request):
    uid = current_user(request)
    if request.method == "POST":
        redirect(request.headers, "/todo/add")
    todo_dict = Todo.model_find_all(uid=int(uid))
    # todo_list = [todo for todo in todo_list if todo.get_deleted() != True]
    todo_list = Todo.model_validate_all(todo_dict)
    # todo test
    # for todo in todo_list:
    #     print(todo.get_deleted())
    body = template("todo.html", todo_list=todo_list)
    r = http_response(body, request.headers)
    return r


@is_login
def route_todo_add(request):
    uid = current_user(request)
    form = request.form()
    form["uid"] = uid
    todo = Todo(form)
    todo.ct = todo.set_time()
    todo.ut = todo.ct
    todo.model_add()
    return redirect(request.headers, "/todo")


@is_login
def route_todo_delete(request):
    todo_id = request.query.get("id", -1)
    if id != -1:
        Todo.model_delete(id=int(todo_id))
    return redirect(request.headers, "/todo")

@is_login
def route_todo_edit(request):
    todo_id = request.query.get("id", -1)
    if id != -1:
        if request.method == "POST":
            form = request.form()
            form["ut"] = Todo.set_time()
            Todo.model_edit(form, id=int(todo_id))
            return redirect(request.headers, "/todo")
        else:
            todo = Todo.model_find_by(id=int(todo_id))
            body = template("todo.edit.html", todo=todo)
            return http_response(body, request.headers)


route_todo = {
    "/todo": route_todo_list,
    "/todo/add": route_todo_add,
    "/todo/delete": route_todo_delete,
    "/todo/edit": route_todo_edit
}