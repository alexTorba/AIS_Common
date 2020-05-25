from JsonFomatterModule.JsonContract import JsonContract


class Person(JsonContract):
    age: int
    name: str

    __json_fields = {
        "a": "age",
        "n": "name"
    }

    def __init__(self, age: int = None, name: str = None):
        super().__init__(self.__json_fields)

        if age is not None:
            self.age = age
        if name is not None:
            self.name = name
