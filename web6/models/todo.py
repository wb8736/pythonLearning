"""
Author: BIN WANG
Time: 15:06
"""
import time

from models import Model


class Todo(Model):
    def __init__(self, form):
        super(Todo, self).__init__(form)
        self.todo = form.get("todo")
        self.ct = form.get("ct", "")
        self.ut = form.get("ut", "")
        self.uid = form.get("uid", -1)

    @classmethod
    def set_time(self):
        time_formate = "%Y/%m/%d %H:%M:%S"
        value = time.localtime(int(time.time()))
        return time.strftime(time_formate, value)