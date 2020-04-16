"""
Author: BIN WANG
Time: 10:05
"""
from utils import log
from utils import data_load
from utils import data_save


class Model(object):

    def __init__(self, form):
        self.id = form.get("id", -1)
        self._deleted = form.get("_deleted", False)

    def set_deleted(self):
        self._deleted = True

    def get_deleted(self):
        return self._deleted

    @classmethod
    def model_db_path(cls):
        class_name = cls.__name__
        path = "db/{}.json".format(class_name)
        return path

    @classmethod
    def model_all(cls):
        path = cls.model_db_path()
        models = data_load(path)
        ms = {int(k): cls(v) for k, v in models.items()}
        return ms

    @classmethod
    def model_validate_all(cls, models):
        if models:
            if isinstance(models, dict):
                ms = [m for m in models.values() if m.get_deleted() is not True]
                return ms
            else:
                ms = [m for m in models if m.get_deleted() is not True]
                return ms
        else:
            return []

    def model_add(self):
        models = self.model_all()
        self.id = 1
        if models:
            # id = max([int(m.id) for m in models])
            id = max(models.keys())
            if id > 0:
                self.id = id + 1
        models[self.id] = self
        self.model_save(models)

    @classmethod
    def model_delete(cls, **kwargs):
        models = cls.model_all()
        matched = cls.model_find_by(**kwargs)
        m = [m for m in models.values() if m.id == matched.id][0]
        m.set_deleted()
        cls.model_save(models)

    @classmethod
    def model_edit(cls, form, **kwargs):
        models = cls.model_all()
        matched = cls.model_find_by(**kwargs)
        m = [m for m in models.values() if m.id == matched.id][0]
        for k, v in form.items():
            # log("model edit {} {}".format(k, v))
            setattr(m, k, v)
        cls.model_save(models)

    @classmethod
    def model_save(cls, ms):
        """
        :param ms: model object list
        :return:
        """
        # l = [m.__dict__ for m in ms]
        d = dict()
        for k, v in ms.items():
            d[k] = v.__dict__
        log("Model Save: {}".format(d))
        path = cls.model_db_path()
        data_save(path, d)

    @classmethod
    def model_find_all(cls, **kwargs):
        models = cls.model_all()
        keys = kwargs.keys()
        if "id" in keys:
            model_id = kwargs.get("id")
            return [models.get(model_id)]
        # todo debug log
        log("models find all models: ({})".format(models))
        match_params = set([(k, v) for k, v in kwargs.items()])
        # todo debug log
        log("models find all match_params: ({})".format(match_params))
        matched_list = list()
        for model in models.values():
            item = set([(k, v) for k, v in model.__dict__.items()])
            if match_params.intersection(item) == match_params:
                matched_list.append(model)
        # todo debug log
        log("models find all mathed list {}".format(matched_list))
        return matched_list

    @classmethod
    def model_find_by(cls, **kwargs):
        matched_list = cls.model_find_all(**kwargs)
        if matched_list:
            return matched_list[0]

    def __repr__(self):
        """
        魔法函数，每次都会待用
        :return:
        """
        # todo 不是很能理解，需要运行时看
        class_name = self.__class__.__name__
        properties = ['{}, ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return 'repr < {}\n{} >\n'.format(class_name, s)