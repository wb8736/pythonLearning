"""
Author: BIN WANG
Time: 11:10
"""
from models import Model


class User(Model):
    def __init__(self, form):
        super().__init__(form)
        self.username = form.get("username", "")
        self.password = form.get("password", "")
        self.note = form.get("note", "")
        self.role = form.get("role", 10)

    def is_admin(self):
        if self.role == 1:
            return True
        else:
            return False

    def validate_login(self):
        if self._deleted:
            return False
        if self.model_find_by(username=self.username, password=self.password):
            return True
        else:
            return False

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 4
