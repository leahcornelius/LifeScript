from traceback import print_exc


global_scope = {}  # A Dict of all the variables in the global scope
scope_stack = []  

def push_scope(scope):
    global scope_stack
    scope_stack.append(scope)

def pop_scope():
    global scope_stack
    scope_stack.pop()

def top_scope():
    global scope_stack
    return scope_stack[len(scope_stack) - 1]

def set_scope_stack(new):
    global scope_stack
    scope_stack = new

def get_scope_stack():
    return scope_stack

def clear():
    global global_scope
    global_scope = {}
