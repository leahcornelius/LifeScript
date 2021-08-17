from ast_objects import *
from memory import *

prelude_vars = {
    '_version': '0.1',
    'classinstances': [],
    'classes': [],
    'scopes': [],
}

prelude_imports = {}


def prelude():
    for k, v in prelude_vars.items():
        global_scope[k] = v
    
    set_scope_stack([Scope( None, [], "main")])
