import inspect
from json import dumps, loads

import typing

from JsonFomatterModule.JsonContract import JsonContract
from JsonFomatterModule.TypeInspect import TypeInspect


class JsonFormatter:
    @staticmethod
    def serialize(obj: JsonContract) -> str:
        if obj is None or not isinstance(obj, JsonContract):
            raise Exception("the object must implement JsonContract !")

        obj_dict_view = JsonFormatter.__object_to_dict(obj)
        return dumps(obj_dict_view, ensure_ascii=False)

    @staticmethod
    def __object_to_dict(obj):
        fields: dict = dict()
        fields.update(obj.to_minimize_dict())

        for k, v in fields.items():
            if isinstance(v, JsonContract):
                fields[k] = JsonFormatter.__object_to_dict(v)
            elif isinstance(v, typing.List):
                for index, item in enumerate(v):
                    if isinstance(item, JsonContract):
                        v[index] = JsonFormatter.__object_to_dict(item)
            elif isinstance(v, typing.Dict):
                for key, value in v.items():
                    if isinstance(value, JsonContract):
                        v[key] = JsonFormatter.__object_to_dict(value)

        return fields

    @staticmethod
    def deserialize(data: str, cls: type):
        if not isinstance(data, str):
            raise TypeError("data must be a string !")
        obj: dict = loads(data)
        return JsonFormatter.__json_to_instance(obj, cls)

    @staticmethod
    def __json_to_instance(obj, cls: type):
        instance: cls = cls()
        annotations: dict = TypeInspect.get_annotations(cls)
        for name, value in obj.items():
            full_field_name = instance.json_to_field(name)
            if full_field_name is None:
                continue  # in case when try to serialize base class of instance
            type_value = annotations.get(full_field_name)
            origin_type_value = typing.get_origin(type_value)
            if origin_type_value is not None:  # if type is Generic
                if TypeInspect.has_any_subclass(type_value.__args__, JsonContract):
                    if issubclass(origin_type_value, typing.List):
                        items_type = type_value.__args__[0]
                        for index, item in enumerate(value):
                            item = JsonFormatter.__json_to_instance(item, items_type)
                            value[index] = item
                    elif issubclass(origin_type_value, typing.Dict):
                        values_type = type_value.__args__[1]
                        for key, val in value.items():
                            val = JsonFormatter.__json_to_instance(val, values_type)
                            value[key] = val
                    else:
                        value = JsonFormatter.__json_to_instance(value, type_value)
            elif inspect.isclass(type_value) and issubclass(type_value, JsonContract):
                value = JsonFormatter.__json_to_instance(value, type_value)

            if not TypeInspect.object_has_same_type(value, type_value):
                continue  # received wrong type of value. Attempt to substitute type of value
            setattr(instance, full_field_name, value)
        return instance
