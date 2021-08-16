from rply.parsergenerator import ParserGenerator


global_scope = {}  # A Dict of all the variables in the global scope


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


class String():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


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
    def __init__(self, value):
        self.value = value

    def eval(self):
        if self.value in global_scope:
            return global_scope[self.value]
        else:
            return Null()


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


class Sum(BinaryOp):
    def eval(self):
        return self.left.eval() + self.right.eval()


class Sub(BinaryOp):
    def eval(self):
        return self.left.eval() - self.right.eval()


class Print():
    def __init__(self, value):
        self.value = value

    def eval(self):
        print(self.value.eval())


class Assign():
    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        #self.type = type if type != None else type(value).toString()

    def eval(self):
        if self.name is None:
            raise Exception("Assign: NullPtr")
        global_scope[self.name] = self.value.eval()


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


class Block():
    def __init__(self, expresion):
        self.expresion = expresion

    def eval(self):
        for exp in self.expresion:
            exp.eval()


class AssignFunction():
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body

    def eval(self):
        global_scope[self.name] = self


class CallFunction():
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def eval(self):
        if self.name in global_scope:
            func = global_scope[self.name]
            if func.body is None:
                raise Exception("CallFunction: No body")
            else:
                func.body.eval()  # TODO: args


class ParameterDeclaration():
    def __init__(self, name, type, parent):
        self.name = name
        self.type = type
        self.parent = parent

    def eval(self):
        global_scope["ParameterStack"][self.parent + "." + self.name] = self


class Arg():
    def __init__(self, name, value,):
        self.name = name
        self.value = value

    def derive_type(self, parent):
        if parent + "." + self.name in global_scope["ParameterStack"]:
            return global_scope["ParameterStack"][parent + "." + self.name].type
        else:
            return type(self.value).toString()

    def eval(self):
        global_scope[self.name] = self.value.eval()


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
