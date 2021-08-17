from rply.parsergenerator import ParserGenerator
from memory import *
from copy import deepcopy


class Expression():
    def __init__(self, expression):
        self.expression = expression

    def eval(self):
        return self.expression.eval()


class Number():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return int(self.value)


class Float():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return float(self.value)


class PrivateVar():
    def __init__(self, name, value, type=None):
        self.name = name
        self.value = Null() if (value is None) else value
        if (type is None):
            self.type = type(value).__name__

    def eval(self):
        pass


class String():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value.replace('"', '')


class Bool():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


class Null():
    def __init__(self):
        pass

    def eval(self):
        return None


class Identifier():
    def __init__(self, value, scope):
        self.value = value
        self.scope = scope

    def eval(self):
        return self.scope.get(self.value)


class BinaryOp():
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Multiply(BinaryOp):
    def eval(self):
        return self.left.eval() * self.right.eval()


class Modulo(BinaryOp):
    def eval(self):
        return self.left.eval() % self.right.eval()


class RightShift(BinaryOp):
    def eval(self):
        return self.left.eval() << self.right.eval()


class LeftShift(BinaryOp):
    def eval(self):
        return self.left.eval() >> self.right.eval()


class Divide(BinaryOp):
    def eval(self):
        return self.left.eval() / self.right.eval()


class Sum(BinaryOp):
    def eval(self):
        return self.left.eval() + self.right.eval()


class Sub(BinaryOp):
    def eval(self):
        return self.left.eval() - self.right.eval()


class Print():
    def __init__(self, value, print_null=False):
        self.value = value
        self.print_null = print_null

    def eval(self):
        val = self.value if not callable(
            getattr(self.value, "eval", None)) else self.value.eval()
        if (val is not None and type(val) is not Null) or self.print_null:
            print(val)


class Assign():
    def __init__(self, name, value, type, scope):
        self.name = name
        self.value = value
        self.type = type if type != None else type(value).__name__
        self.scope = scope
        
    def eval(self):
        if self.name is None:
            raise Exception("Assign: Unnamed varible")
        if self.scope is not None:
            raise Exception("Assign: No scope declared")
        self.scope.set(self.name, self.value.eval());


class If():
    def __init__(self, condition, expression, else_expresion=None):
        self.condition = condition
        self.expression = expression
        self.else_expresion = else_expresion

    def eval(self):
        if self.condition.eval():
            self.expression.eval()
        elif self.else_expresion is not None:
            self.else_expresion.eval()


class Pointer():
    def __init__(self, index, stack):
        self.index = index
        self.stack = stack

    def deref(self, target=None):
        if self.index is None:
            raise Exception("NullPtr")
        if target is None:
            target = self.stack
        if target is not None and (self.index < len(target) - 1):
            return target[self.index]
        if target is None:
            raise Exception("Pointer: deref: no target")
        raise Exception("Pointer deref: Index out of range")

    def delete(self, target=None):
        if self.index is None:
            raise Exception("NullPtr")
        if target is None:
            target = self.stack
        if target is not None and (self.index < len(target) - 1):
            del target[self.index]
            return Null()
        if target is None:
            raise Exception("Pointer: deref: no target")
        raise Exception("Pointer deref: Index out of range")


class Scope():
    def __init__(self, parent=None, children=None, name=None):
        self.parent = parent
        self.children = children
        self.stack = []
        self.heap = {}
        self.name = name

        # Create a new dict for this scope
        global_scope["scopes"].append(self)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get(self, key):
        if key not in self.heap:
            return self.parent.get(key)

        ptr = self.heap[key]
        return ptr.deref(self.stack)

    def set(self, key, value):
        self.stack.push(value)
        # get the index of the key
        index = self.stack.index(value)
        ptr = Pointer(index, self.stack)
        self.heap[key] = ptr
        return ptr

    def delete(self, key):
        if key not in self.heap:
            return self.parent.delete(key)

        ptr = self.heap[key]
        ptr.delete(self.stack)

    def eval(self):
        for child in self.children:
            child.eval()


class Block(Scope):
    def __init__(self, parent=None, children=None, name=None, expressions=[]):
        Scope.__init__(self, parent, children, name)
        self.stack = []
        self.heap = {}
        self.name = name
        self.scope = Scope(self, name=name)
        self.scope.stack = self.stack
        self.scope.heap = self.heap
        self.scope.name = name
        self.expressions = expressions

    def eval(self):
        for i, expr in enumerate(self.expressions):
            # if (i == len(self.expressions) - 1): # TODO: Only return return statments, not just the last one
            #    return expr.eval() # If this is the last expression, return the last value
            expr.eval()


class Program():
    def __init__(self, statments):
        self.statments = statments

    def eval(self):
        for statment in self.statments:
            statment.eval()


class Parameter():
    def __init__(self, name, type, default=None):
        self.name = name
        self.type = type
        self.default = default

    def eval(self):
        if self.default is not None:
            return self.default
        else:
            return Null()


class Function():
    def __init__(self, name, args, body):
        self.name = name
        self.args = args  # A List of Parameter()s
        self.body = body

    def eval(self, argsList, scope):  # Args list is a list of Args
        prev_values = {}
        for parameter in self.args.args:
            if (parameter.name in global_scope):
                prev_values[parameter.name] = global_scope[parameter.name]
            found = False
            for arg in argsList.args:
                if arg.name == parameter.name:
                    if arg.value.eval is not None:
                        global_scope[arg.name] = arg.value.eval()
                    else:
                        global_scope[arg.name] = arg.value
                    found = True
                    break
            if not found:  # If the argument is not in the list, we assume that it is the default value
                default = parameter.eval()
                if default.eval() is not None:
                    global_scope[parameter.name] = default.eval()
                elif default is not None:
                    global_scope[parameter.name] = default
                else:
                    global_scope[parameter.name] = Null()
        self.body.eval()
        for arg in prev_values:
            global_scope[arg] = prev_values[arg]
        for arg in self.args.args:
            if arg.name in global_scope:
                del global_scope[arg.name]

    def get_name(self):
        return self.name


class AssignFunction():
    def __init__(self, name, args, body, scope):
        self.name = name
        self.args = args
        self.body = body
        self.scope = scope

    def eval(self):
        self.scope.set(self.name, Function(
            self.name, self.args, self.body))


class Comment():
    def __init__(self, value):
        self.value = value

    def eval(self):
        pass


class ArgList():
    def __init__(self, args):
        self.args = args

    def eval(self):
        raise Exception("ArgList: Called eval")


class Import():
    def __init__(self, path, atlas=None):
        self.path = path
        self.atlas = atlas

    def eval(self):
        if self.atlas is None:
            self.atlas = self.path

        if "std/" not in self.path:
            raise Exception("Import: Not Implemented")

        # import from the standard library
        if self.path == "std/Math":
            # import the math library
            from std import Math
            math = Math()
            imports = math.exports()
            for key, value in imports.items():
                # form a function
                global_scope[key] = Function(key, value.input, value.code)


class CallFunction():
    def __init__(self, name, args, scope):
        self.name = name
        self.args = args
        self.scope = scope

    def eval(self):
        func = self.scope.get(self.name)
        if not func:
            raise Exception("CallFunction: Function undefined")
        if type(func) is not Function:
            raise Exception("CallFunction: Cannot call " + type(func).__name__)
        if func.body is None:
            raise Exception("CallFunction: No body")
        else:
            func.eval(self.args, scope)


class Arg():
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def derive_type(self, parent):
        if parent + "." + self.name in global_scope["ParameterStack"]:
            return global_scope["ParameterStack"][parent + "." + self.name].type
        else:
            return type(self.value).toString()


class Type():
    def __init__(self, type):
        self.type = type

    def toString(self):
        return self.type

    def eval(self):
        return self.type


class DebugPrintStack():
    def __init__(self):
        pass

    def eval(self):
        print(global_scope)


class StatmentList():
    def __init__(self, expresions):
        self.expresion = []
        for exp in expresions:
            self.expresion.append(exp)

    def eval(self):
        for exp in self.expresion:
            exp.eval()

    def add(self, exp):
        self.expresion.append(exp)


class ConditionResolver():
    def __init__(self, expresion, type, other_expresion):
        self.expresion = expresion
        self.type = type
        self.other_expresion = other_expresion

    def eval(self):
        if self.type == 'EQ':
            if self.expresion.eval() == self.other_expresion.eval():
                return True
        elif self.type == 'NEQ':
            if self.expresion != self.other_expresion.eval():
                return True
        elif self.type == 'GREATER_THAN':
            if self.expresion > self.other_expresion.eval():
                return True
        elif self.type == 'LESS_THAN':
            if self.expresion < self.other_expresion.eval():
                return True
        elif self.type == 'GREATER_THAN_EQ':
            if self.expresion >= self.other_expresion.eval():
                return True
        elif self.type == 'LESS_THAN_EQ':
            if self.expresion <= self.other_expresion.eval():
                return True
        elif self.type == 'AND':
            if self.expresion and self.other_expresion.eval():
                return True
        elif self.type == 'OR':
            if self.expresion or self.other_expresion.eval():
                return True
        elif self.type == 'NOT':
            if not self.other_expresion.eval():
                return True
        elif self.type == 'IN':
            if self.expresion in self.other_expresion.eval():
                return True
        elif self.type == 'NOT_IN':
            if self.expresion not in self.other_expresion.eval():
                return True
        elif self.type == 'IS':
            if self.expresion is self.other_expresion.eval():
                return True


class TypeOf():
    def __init__(self, expresion):
        self.expresion = expresion

    def eval(self):
        return type(self.expresion.eval()).__name__


class ClassPointer(Pointer):
    def __init__(self, index):
        Pointer.__init__(self, index, "classinstances")

    def eval(self):
        return global_scope[self.path][self.index]


class Class():
    def __init__(self, name, superclass, methods, interface):
        self.name = name
        self.methods = methods.methods  # passed method var is a ClassBody class
        # find the constructor method
        self.constructor = None
        for statementList in methods.methods:
            for method in statementList.expresion:
                if (type(method) == AssignFunction and (
                    method.name == "constructor"
                )):
                    print("found constructor", method.name)
                    self.constructor = method.scope.get(method.name)
                else:
                    print(type(method))

        if (superclass is not None):
            self.superclass = superclass
        if (interface is not None):
            self.interface = interface

    def eval(self):
        # Push onto the stack
        global_scope["classes"].append(self)

    def instanciate(self, args):
        instance = deepcopy(self)
        if (instance.constructor is not None):
            # call the constructor
            instance.constructor.eval(ArgList(args))
        # Push onto the stack
        global_scope["classinstances"].append(instance)
        # find our index in the class list
        return ClassPointer(global_scope["classinstances"].index(instance))

    def get_methods(self):
        return self.methods

    def get_superclass(self):
        return self.superclass

    def get_interface(self):
        return self.interface

    def get_name(self):
        return self.name

    def get_method(self, name):
        for method in self.methods:
            if (method.get_name() == name):
                return method
        # if we didn't find the method look in the superclass
        if (self.superclass is not None):
            # get the superclass
            superclass = None
            for class_ in global_scope["classes"]:
                if (class_.get_name() == self.superclass):
                    superclass = class_
                    break
            if (superclass is not None):
                return superclass.get_method(name)

        return None

    def call_method(self, name, args):
        method = self.get_method(name)
        if (method is None):
            raise Exception("Method not found")
        # construct a set of local variables
        local_scope = ArgList(args)
        # push all local methods into the local scope
        for local_method in self.methods:
            local_scope.push(local_method)

        return method.eval(args)

    def get_method_names(self):
        return [method.get_name() for method in self.methods]


class AbstractClass(Class):
    def __init__(self, name, superclass, methods, interface):
        Class.__init__(self, name, superclass, methods, interface)

    def eval(self):
        # Push onto the stack
        global_scope["classes"].append(self)

    def instanciate(self):
        raise Exception("Abstract classes cannot be instantiated")


class ClassBody():
    def __init__(self, methods):
        self.methods = methods

    def add_method(self, method):
        self.methods.append(method)

    def get_methods(self):
        return self.methods

    def eval(self):
        return Null()
