from memory import *
from copy import deepcopy

# The most basic of the AST nodes, an abstract syntax tree node.
# All AST classes are subclasses of this class.


class Return():
    def __init__(self, expr):
        self.expr = expr

    def eval(self, env):
        if hasattr(self.expr, 'eval'):
            return self.expr.eval(env)
        return self.expr


class Node():
    def __init__(self, parent, children=[]):
        self.parent = parent
        self.children = children
        self.scope = None

    def __repr__(self) -> str:
        return "Node({})".format(id(self))

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children

    def get(self, key):
        scope = self.get_scope()
        if scope is not None:
            return scope.get(key)
        return Null()

    def get_scope(self):
        if self.parent is None:
            if self.scope is None:
                self.scope = Scope(self)
            return self.scope
        else:
            if type(self.parent) is Scope:
                return self.parent
            if hasattr(self.parent, "scope") and self.parent.scope is not None:
                return self.parent.scope
            return self.parent.get_scope()

    def set_parent(self, parent=None):
        self.parent = parent

    def add_child(self, child):
        if self.children is None:
            self.children = [child]
        else:
            child.set_parent(self)
            self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)


class Expression(Node):
    def __init__(self, expression, parent=None):
        self.expression = expression
        Node.__init__(self, parent)
        self.children = []

    def eval(self):
        return self.expression.eval()

    def __repr__(self):
        return "Expression: " + str(self.expression)


class Number(Node):
    def __init__(self, value, parent=None):
        self.value = value
        Node.__init__(self, parent)

    def eval(self):
        return int(self.value)

    def __repr__(self):
        return "Number: " + str(self.value)


class Float(Node):
    def __init__(self, value, parent=None):
        self.value = value
        Node.__init__(self, parent)

    def eval(self):
        return float(self.value)

    def __repr__(self):
        return "Float: " + str(self.value)


class PrivateVar(Node):
    def __init__(self, name, value, type=None, parent=None):
        self.name = name
        self.value = Null() if (value is None) else value
        if (type is None):
            self.type = type(value).__name__

        Node.__init__(self, parent)

    def eval(self):
        pass

    def __repr__(self):
        return "PrivateVar: " + str(self.name) + " " + str(self.value) + " " + str(self.type)


class String(Node):
    def __init__(self, value, parent=None):
        self.value = value
        Node.__init__(self, parent)

    def eval(self):
        return self.value.replace('"', '')

    def __repr__(self):
        return "String: " + str(self.value)


class Bool(Node):
    def __init__(self, value, parent=None):
        self.value = value
        Node.__init__(self, parent)

    def eval(self):
        return self.value

    def __repr__(self):
        return "Bool: " + str(self.value)


class Null(Node):
    def __init__(self, parent=None):
        Node.__init__(self, parent)

    def eval(self):
        return None

    def __repr__(self):
        return "Null"

    def __add__(self, other):
        return str(self) + str(other)


class Identifier(Node):
    def __init__(self, value, parent=None):
        self.value = value
        self.scope = None
        Node.__init__(self, parent)

    def eval(self):
        if (self.scope is None):
            # get the scope from the parent
            self.scope = self.parent.get_scope()
        return self.scope.get(self.value)

    def __repr__(self):
        return "Identifier: " + str(self.value) + ": <" + str(self.scope) + "> = " + str(self.value)


class BinaryOp(Node):
    def __init__(self, left, right, parent=None):
        self.left = left
        self.right = right
        Node.__init__(self, parent)

    def __repr__(self):
        return "BinaryOp: " + str(self.left) + " " + str(self.right)


class Multiply(BinaryOp):
    def eval(self):
        return self.left.eval() * self.right.eval()

    def __repr__(self):
        return "Multiply: " + str(self.left) + " * " + str(self.right)


class Modulo(BinaryOp):
    def eval(self):
        return self.left.eval() % self.right.eval()

    def __repr__(self):
        return "Modulo: " + str(self.left) + " % " + str(self.right)


class RightShift(BinaryOp):
    def eval(self):
        return self.left.eval() << self.right.eval()

    def __repr__(self):
        return "RightShift: " + str(self.left) + " >> " + str(self.right)


class LeftShift(BinaryOp):
    def eval(self):
        return self.left.eval() >> self.right.eval()

    def __repr__(self):
        return "LeftShift: " + str(self.left) + " << " + str(self.right)


class Divide(BinaryOp):
    def eval(self):
        return self.left.eval() / self.right.eval()

    def __repr__(self):
        return "Divide: " + str(self.left) + " / " + str(self.right)


class Sum(BinaryOp):
    def eval(self):
        return self.left.eval() + self.right.eval()

    def __repr__(self):
        return "Sum: " + str(self.left) + " + " + str(self.right)


class Sub(BinaryOp):
    def eval(self):
        return self.left.eval() - self.right.eval()

    def __repr__(self):
        return "Sub: " + str(self.left) + " - " + str(self.right)


class Print(Node):
    def __init__(self, value, print_null=False, parent=None):
        Node.__init__(self, parent)
        self.value = value
        self.print_null = print_null
        # Node.__init__(self, parent)
        # self.children = []

    def eval(self):
        val = self.value if not callable(
            getattr(self.value, "eval", None)) else self.value.eval()
        if (val is not None and type(val) is not Null) or self.print_null:
            print(val)

    def __repr__(self):
        val = self.value
        return "(" + str(id(self)) + ") Print: " + str(val)


class Assign(Node):
    def __init__(self, name, value, type, parent=None):
        self.name = name
        self.value = value
        self.type = None  # type if type != None else type(value).__name__
        self.scope = None
        Node.__init__(self, parent)

    def eval(self):
        if self.name is None:
            raise Exception("Assign: Unnamed varible")
        if (self.scope is None):
            # get the scope from the parent
            self.scope = self.parent.get_scope()
        self.scope.set(self.name, self.value.eval())

    def __repr__(self):
        return "Assign: " + str(self.name) + ": <" + str(self.type) + "> = " + str(self.value)


class If(Node):
    def __init__(self, condition, expression, else_expresion=None, parent=None):
        self.condition = condition
        self.expression = expression
        self.else_expresion = else_expresion
        Node.__init__(self, parent)

    def eval(self):
        if self.condition.eval():
            self.expression.eval()
        elif self.else_expresion is not None:
            self.else_expresion.eval()

    def __repr__(self):
        return "If: " + str(self.condition) + "  { " + str(self.expression) + " } { " + str(self.else_expresion) + " }"


class Pointer(Node):
    def __init__(self, index, stack, parent=None):
        self.index = index
        self.stack = stack
        Node.__init__(self, parent)

    def deref(self, target=None):
        if self.index is None:
            raise Exception("NullPtr")
        if target is None:
            target = self.stack

        if target is not None and (self.index <= len(target) - 1):
            return target[self.index]

        if target is None:
            raise Exception("Pointer: deref: no target")

        raise Exception(
            f"Pointer deref: Index out of range, index: {self.index}, len(target): {len(target)}")

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

    def __repr__(self):
        return "Pointer: " + str(self.index) + " -> " + str(self.stack)


class Scope():
    def __init__(self, parent=None, children=[], name=None):
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

    def set_parent(self, parent):
        self.parent = parent

    def get(self, key):
        if key not in self.heap:
            if self.parent is not None:
                return self.parent.get(key)
            else:
                return Null()

        ptr = self.heap[key]
        return ptr.deref(self.stack)

    def set(self, key, value):
        self.stack.append(value)
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

    def __repr__(self):
        return "Scope (" + str(self.name) + "): Memory(" + str(self.stack) + " " + str(self.heap) + ") Children Count: " + str(len(self.children)) + " has parent: " + str(self.parent is not None)

    def iter(self):
        yield from self.children


class Block(Scope):
    def __init__(self, parent=None, children=[], name=None, expressions=[]):
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
            res = expr.eval()
            if isinstance(res, Return):
                return res.value

    def get_scope(self):
        return self.scope

    def __repr__(self):
        return "Block Scope (" + str(self.name) + "): Memory(" + str(self.stack) + " " + str(self.heap) + ") Children Count: " + str(len(self.children)) + " has parent: " + str(self.parent is not None)


class Program(Node):
    def __init__(self, statments, parent=None):
        self.statments = statments
        Node.__init__(self, parent)

    def eval(self):
        for statment in self.statments:
            if isinstance(statment, Return) or len(self.statments) == 1:
                return statment.eval()
            statment.eval()

    def iter(self):
        yield from self.statments

    def __repr__(self):
        return "Program: " + str(self.statments)


class Parameter(Node):
    def __init__(self, name, type, default=None, parent=None):
        self.name = name
        self.type = type
        self.default = default
        Node.__init__(self, parent)

    def eval(self):
        if self.default is not None:
            return self.default
        else:
            return Null()

    def __repr__(self):
        return "Parameter: " + str(self.name) + ": <" + str(self.type) + "> = " + str(self.default)


class Function(Node):
    def __init__(self, name, args, body, parent=None):
        self.name = name
        self.args = args  # A List of Parameter()s
        self.body = body
        self.scope = None
        Node.__init__(self, parent)

    def eval(self, argsList, scope):  # Args list is a list of Args
        self.scope = Scope(self, name=str(self.name) + "LocalFnScope")
        for parameter in self.args.args:
            found = False
            for arg in argsList.args:
                if arg.name == parameter.name:
                    if hasattr(arg.value, "eval"):
                        self.scope.set(arg.name, arg.value.eval())
                    else:
                        self.scope.set(arg.name, arg.value)
                    found = True
                    break
            if not found:  # If the argument is not in the list, we assume that it is the default value
                default = parameter.eval()
                if default.eval() is not None:
                    self.scope.set(parameter.name, default.eval())
                elif default is not None:
                    self.scope.set(parameter.name, default)
                else:
                    self.scope.set(parameter.name, Null())
        body_scope_copy = deepcopy(self.body.get_scope())

        self.body.scope = self.scope
        self.body.eval()
        self.scope = None
        self.body.scope = body_scope_copy

    def get_name(self):
        return self.name

    def __repr__(self):
        return "Function: " + str(self.name) + "(" + str(self.args) + ") { " + str(self.body) + " }"


class AssignFunction(Node):
    def __init__(self, name, args, body, parent=None):
        self.name = name
        self.args = args
        self.body = body
        self.scope = None
        Node.__init__(self, parent)

    def eval(self):
        if (self.scope is None):
            # get the scope from the parent
            self.scope = self.parent.get_scope()
        self.scope.set(self.name, Function(
            self.name, self.args, self.body))

    def __repr__(self):
        return "AssignFunction: " + str(self.name) + "(" + str(self.args) + ") { " + str(self.body) + " }"


class Comment(Node):
    def __init__(self, value, parent=None):
        self.value = value
        Node.__init__(self, parent)

    def eval(self):
        pass

    def __repr__(self):
        return "Comment: " + str(self.value)


class ArgList(Node):
    def __init__(self, args, parent=None):
        self.args = args
        Node.__init__(self, parent)

    def eval(self):
        raise Exception("ArgList: Called eval")

    def __repr__(self):
        return "ArgList: " + str(self.args)


class Import(Node):
    def __init__(self, path, atlas=None, parent=None):
        self.path = path
        self.atlas = atlas
        Node.__init__(self, parent)

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

    def __repr__(self):
        return "Import: " + str(self.path) + " as " + str(self.atlas)


class CallFunction(Node):
    def __init__(self, name, args, parent=None):
        self.name = name
        self.args = args
        self.scope = None
        Node.__init__(self, parent)

    def eval(self):
        if (self.scope is None):
            # get the scope from the parent
            self.scope = self.parent.get_scope()
        func = self.scope.get(self.name)
        if not func:
            raise Exception("CallFunction: Function undefined")
        if type(func) is not Function:
            raise Exception("CallFunction: Cannot call " + type(func).__name__)
        if func.body is None:
            raise Exception("CallFunction: No body")
        else:
            func.eval(self.args, self.scope)

    def __repr__(self):
        return "CallFunction: " + str(self.name) + "(" + str(self.args) + ")"


class Arg(Node):
    def __init__(self, name, value, parent=None):
        self.name = name
        self.value = value
        Node.__init__(self, parent)

    def derive_type(self, parent=None):
        if parent + "." + self.name in global_scope["ParameterStack"]:
            return global_scope["ParameterStack"][parent + "." + self.name].type
        else:
            return type(self.value).toString()

    def __repr__(self):
        return "Arg: " + str(self.name) + " = " + str(self.value)


class Type(Node):
    def __init__(self, type, parent=None):
        self.type = type
        Node.__init__(self, parent)

    def toString(self):
        return self.type

    def eval(self):
        return self.type

    def __repr__(self):
        return "Type: " + str(self.type)


class DebugPrintStack(Node):
    def __init__(self, parent=None):
        Node.__init__(self, parent)

    def eval(self):
        print(global_scope)

    def __repr__(self):
        return "DebugPrintStack()"


class StatmentList(Node):
    def __init__(self, expresions, parent=None):
        self.expresion = []
        Node.__init__(self, parent)
        for exp in expresions:
            self.expresion.append(exp)

    def eval(self):
        for exp in self.expresion:
            exp.eval()

    def add(self, exp):
        self.expresion.append(exp)

    def __repr__(self):
        return "StatmentList: " + str(self.expresion)

    def iter(self):
        yield from self.expresion
# Abstract Condition Class


class Condition(Node):
    def __init__(self, one, two, parent=None):
        Node.__init__(self, parent)
        self.one = one
        self.two = two

    def __repr__(self):
        return "Condition: " + str(self.one) + " " + str(self.two)


class Equal(Condition):
    def eval(self):
        return self.one.eval() == self.two.eval()

    def __repr__(self):
        return "Equal: " + str(self.one) + " == " + str(self.two)


class NotEqual(Condition):
    def eval(self):
        return self.one.eval() != self.two.eval()

    def __repr__(self):
        return "NotEqual: " + str(self.one) + " != " + str(self.two)


class GreaterThan(Condition):
    def eval(self):
        return self.one.eval() > self.two.eval()

    def __repr__(self):
        return "GreaterThan: " + str(self.one) + " > " + str(self.two)


class LessThan(Condition):
    def eval(self):
        return self.one.eval() < self.two.eval()

    def __repr__(self):
        return "LessThan: " + str(self.one) + " < " + str(self.two)


class GreaterThanOrEqual(Condition):
    def eval(self):
        return self.one.eval() >= self.two.eval()

    def __repr__(self):
        return "GreaterThanOrEqual: " + str(self.one) + " >= " + str(self.two)


class LessThanOrEqual(Condition):
    def eval(self):
        return self.one.eval() <= self.two.eval()

    def __repr__(self):
        return "LessThanOrEqual: " + str(self.one) + " <= " + str(self.two)


class And(Condition):
    def eval(self):
        return self.one.eval() and self.two.eval()

    def __repr__(self):
        return "And: " + str(self.one) + " && " + str(self.two)


class Or(Condition):
    def eval(self):
        return self.one.eval() or self.two.eval()

    def __repr__(self):
        return "Or: " + str(self.one) + " || " + str(self.two)


class Not(Condition):
    def eval(self):
        return not self.one.eval()

    def __repr__(self):
        return "Not: " + str(self.one)


class In(Condition):
    def eval(self):
        return self.one.eval() in self.two.eval()

    def __repr__(self):
        return "In: " + str(self.one) + " in " + str(self.two)


class NotIn(Condition):
    def eval(self):
        return self.one.eval() not in self.two.eval()

    def __repr__(self):
        return "NotIn: " + str(self.one) + " not in " + str(self.two)


class Is(Condition):
    def eval(self):
        return self.one.eval() is self.two.eval()

    def __repr__(self):
        return "Is: " + str(self.one) + " is " + str(self.two)


class ConditionResolver(Node):
    def __init__(self, expresion, type, other_expresion, parent=None):
        self.expresion = expresion
        self.type = type
        self.other_expresion = other_expresion
        Node.__init__(self, parent)

    def eval(self):
        if self.type == 'EQ':
            return Equal(self.expresion, self.other_expresion, self.parent).eval()
        elif self.type == 'NEQ':
            return NotEqual(self.expresion, self.other_expresion, self.parent).eval()
        elif self.type == 'GREATER_THAN':
            return GreaterThan(self.expresion, self.other_expresion, self.parent).eval()
        elif self.type == 'LESS_THAN':
            return LessThan(self.expresion, self.other_expresion, self.parent).eval()
        elif self.type == 'GREATER_THAN_EQ':
            return GreaterThanOrEqual(self.expresion, self.other_expresion, self.parent).eval()
        elif self.type == 'LESS_THAN_EQ':
            return LessThanOrEqual(self.expresion, self.other_expresion, self.parent).eval()
        elif self.type == 'AND':
            return And(self.expresion, self.other_expresion, self.parent).eval()
        elif self.type == 'OR':
            return Or(self.expresion, self.other_expresion, self.parent).eval()
        elif self.type == 'NOT':
            return Not(self.expresion, self.parent).eval()
        elif self.type == 'IN':
            return In(self.expresion, self.other_expresion, self.parent).eval()
        elif self.type == 'NOT_IN':
            return NotIn(self.expresion, self.other_expresion, self.parent).eval()
        elif self.type == 'IS':
            return Is(self.expresion, self.other_expresion, self.parent).eval()

    def __repr__(self):
        return "ConditionResolver: " + str(self.expresion) + " " + str(self.type) + " " + str(self.other_expresion)


class TypeOf(Node):
    def __init__(self, expresion, parent=None):
        self.expresion = expresion
        Node.__init__(self, parent)

    def eval(self):
        return type(self.expresion.eval()).__name__

    def __repr__(self):
        return "TypeOf: " + str(self.expresion)


class ClassPointer(Pointer):
    def __init__(self, index, parent=None):
        Pointer.__init__(self, index, "classinstances", parent)

    def eval(self):
        return global_scope[self.path][self.index]

    def __repr__(self):
        return "ClassPointer: " + str(self.index) + super().__repr__()


class Class(Node):
    def __init__(self, name, superclass, methods, interface, parent=None):
        self.name = name
        Node.__init__(self, parent)
        self.methods = methods.methods  # passed method var is a ClassBody class
        # find the constructor method
        self.constructor = None
        for statementList in methods.methods:
            for method in statementList.expresion:
                if (type(method) == AssignFunction and (
                    method.name == "constructor"
                )):
                    self.constructor = method.scope.get(method.name)

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

    def __repr__(self):
        return "Class: " + str(self.name) + " " + str(self.superclass) + " " + str(self.interface) + " " + str(self.methods)


class AbstractClass(Class):
    def __init__(self, name, superclass, methods, interface, parent=None):
        Class.__init__(self, name, superclass, methods, interface, parent)

    def eval(self):
        # Push onto the stack
        global_scope["classes"].append(self)

    def instanciate(self):
        raise Exception("Abstract classes cannot be instantiated")

    def __repr__(self):
        return "AbstractClass: " + str(self.name) + " " + str(self.superclass) + " " + str(self.interface) + " " + str(self.methods)


class ClassBody(Node):
    def __init__(self, methods, parent=None):
        self.methods = methods
        Node.__init__(self, parent)

    def add_method(self, method):
        self.methods.append(method)

    def get_methods(self):
        return self.methods

    def eval(self):
        return Null()

    def __repr__(self):
        return "ClassBody: " + str(self.methods)
