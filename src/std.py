from ast_objects import *
class Math():
    def __init__(self):
        pass

    def exports(self):
        return {
            "add": {
                "input": [{
                    "type": Number,
                    "name": "a"
                }, {
                    "type": Number,
                    "name": "b"
                }],
                "output": Number,
                "code": "return a + b;",
            }

        }
