from numpy.core.defchararray import mod
from rply import ParserGenerator, Token
from pprint import pprint
from ast_objects import *
from memory import *


class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names, accepted by the parser.
            ['STRING', 'INTEGER', 'FLOAT', 'IDENTIFIER', 'BOOLEAN',
             'PLUS', 'MINUS', 'MUL', 'DIV',
             'IF', 'ELSE', 'COLON', 'END', 'AND', 'OR', 'NOT', 'LET', 'VAR', 'WHILE',
             'OPEN_BRACKET', 'CLOSE_BRACKET', 'EQUAL', 'EQ', 'NEQ', 'GREATER_THAN_EQ', 'LESS_THAN_EQ', 'GREATER_THAN', 'LESS_THAN', 'OPEN_SQUARE_BRACKET', 'CLOSE_SQUARE_BRACKET', 'COLON',
             'OPEN_CURLY_BRACKET', 'CLOSE_CURLY_BRACKET',
             '$end', 'NEWLINE', 'FUNCTION', 'SEMI_COLON', 'PRINT', 'PERCENT', "DOT", "TYPEOF", "RETURN", "AS", "COMMA", "WHILE", "FOR", "DEBUG_PRINT_STACK", "SINGLE_LINE_COMMENT", "MULTI_LINE_COMMENT", "IMPORT",
             "TYPE", "CLASS", "IMPLEMENTS", "EXTENDS", "ABSTRACT", "PRIVATE", "NEW", "PRINT_SCOPES", "NULL", "STR", "FLOAT", "INT"
             ],
            # A list of precedence rules with ascending precedence, to
            # disambiguate ambiguous production rules.
            precedence=[
                ('left', ['FUNCTION', 'PRINT']),
                ('left', ['LET', 'IDENTIFIER']),
                ('left', ['EQUAL']),
                ('left', ['OPEN_SQUARE_BRACKET',
                          'CLOSE_SQUARE_BRACKET', 'COMMA']),
                ('left', ['IF', 'COLON', 'SEMI_COLON',
                          'ELSE', 'END', 'NEWLINE', 'WHILE', ]),
                ('left', ['AND', 'OR', ]),
                ('left', ['NOT', ]),
                ('left', ['EQ', 'NEQ', 'GREATER_THAN_EQ',
                          'GREATER_THAN', 'LESS_THAN', 'LESS_THAN_EQ', ]),
                ('left', ['PLUS', 'MINUS', ]),
                ('left', ['MUL', 'DIV', ]),
            ]
        )

    def parse(self):
        # The top level object of the AST
        @self.pg.production('program : statement_list')
        def program(p):
            statement_list = p[0]
            program = Program([statement_list], get_scope_stack()[-1])
            statement_list.parent = program
            program.add_child(statement_list)
            return program

        # When we enter a new scope we need to add it to the stack
        # so that we can keep track of nested scopes.

        @self.pg.production('scope : OPEN_CURLY_BRACKET program CLOSE_CURLY_BRACKET')
        def scope_program(p):
            # Create a new block scope
            program = p[1]
            scope = Block(None, [], None, [program])

            scope.add_child(program)
            return scope

        # Block scopes can be nested as statments
        @self.pg.production('statement : scope')
        def statement_scope(p):
            return p[0]

        @self.pg.production('statement_list : statement SEMI_COLON')
        @self.pg.production('statement_list : statement')
        def statement_list(p):
            statement = p[0]
            statementList = StatmentList([p[0]])
            statementList.add_child(statement)
            return statementList

        @self.pg.production('statement_list : statement_list statement SEMI_COLON')
        @self.pg.production('statement_list : statement_list statement')
        def statement_list(p):
            statements = [p[0], p[1]]
            statemenList = StatmentList(statements)
            for statement in statements:
                statemenList.add_child(statement)
            return statemenList

        @self.pg.production('expression : IDENTIFIER')
        def statement(p):
            return Identifier(p[0].getstr())

        @self.pg.production('statement : PRINT OPEN_BRACKET expression CLOSE_BRACKET SEMI_COLON')
        def statement(p):
            expr = p[2]
            print_ = Print(expr)
            print_.add_child(expr)
            return print_

        @self.pg.production('condition_list : condition')
        def condition_list(p):
            return p[0]

        @self.pg.production('condition : expression EQ expression')
        @self.pg.production('condition : expression NEQ expression')
        @self.pg.production('condition : expression GREATER_THAN expression')
        @self.pg.production('condition : expression LESS_THAN expression')
        @self.pg.production('condition : expression GREATER_THAN_EQ expression')
        @self.pg.production('condition : expression LESS_THAN_EQ expression')
        def condition(p):
            CR = ConditionResolver(p[0], p[1].gettokentype(), p[2])
            CR.add_child(p[0])
            CR.add_child(p[2])
            return CR

        @self.pg.production('expression : expression PLUS expression')
        @self.pg.production('expression : expression MINUS expression')
        @self.pg.production('expression : expression MUL expression')
        @self.pg.production('expression : expression DIV expression')
        def expression(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            to_return = None
            if operator.gettokentype() == 'PLUS':
                to_return = Sum(left, right)
            elif operator.gettokentype() == 'MINUS':
                to_return = Sub(left, right)
            elif operator.gettokentype() == 'MUL':
                to_return = Multiply(left, right)
            elif operator.gettokentype() == 'DIV':
                to_return = Divide(left, right)
            else:
                raise Exception("Unknown operator: " + operator.gettokentype())

            to_return.add_child(left)
            to_return.add_child(right)
            return to_return

        @self.pg.production('expression : INTEGER')
        def number(p):
            return Number(p[0].value)

        @self.pg.production('expression : FLOAT')
        def float(p):
            return Float(p[0].value)

        @self.pg.production('expression : IDENTIFIER')
        def identifier(p):
            return Identifier(p[0].value)

        @self.pg.production('expression : BOOLEAN')
        def boolean(p):
            return Bool(p[0].value)

        @self.pg.production('expression : STRING')
        def string(p):
            return String(p[0].value)

        @self.pg.production('expression : condition')
        def expression_condition(p):
            return p[0]

        @self.pg.production('statement : expression')
        def debug_statement(p):
            expr = p[0]
            print_ = Print(expr)
            print_.add_child(expr)
            return print_

        @self.pg.production('expression : expression PERCENT expression')
        def expression_modulo(p):
            left = p[0]
            right = p[2]
            mod_ = Modulo(left, right)
            mod_.add_child(left)
            mod_.add_child(right)
            return mod_

        @self.pg.production('statement : VAR IDENTIFIER EQUAL expression SEMI_COLON')
        @self.pg.production('statement : LET IDENTIFIER EQUAL expression SEMI_COLON')
        @self.pg.production('statement : LET IDENTIFIER COLON LESS_THAN expression GREATER_THAN EQUAL expression SEMI_COLON')
        def expression_assign(p):
            # Check if the type has been declared
            assign_ = Null()
            if p[2].gettokentype() == 'COLON' and p[3].gettokentype() == 'LESS_THAN' and p[5].gettokentype() == 'GREATER_THAN':
                assign_ = Assign(p[1].value, p[7], p[4])
                assign_.add_child(p[4])
                assign_.add_child(p[7])
                return assign_
            name = p[1].value
            value = p[3]
            assign_ = Assign(name, value, None)
            assign_.add_child(value)
            return assign_
        #                                0  1            2         3             4     5

        @self.pg.production('statement : IF OPEN_BRACKET condition CLOSE_BRACKET scope scope')
        @self.pg.production('statement : IF OPEN_BRACKET condition CLOSE_BRACKET scope')
        def expression_if(p):
            condition = p[2]
            if len(p) == 6:
                if_ = If(condition, p[4], p[5])
                if_.add_child(p[2])
                if_.add_child(p[4])
                if_.add_child(p[5])
                return if_
            elif len(p) == 5:
                if_ = If(p[2], p[4], None)
                if_.add_child(p[2])
                if_.add_child(p[4])
                return if_
            else:
                raise Exception('Invalid IF statement, length=' + str(len(p)))

        # parameters

        # Arg name: type
        @self.pg.production('parameters : IDENTIFIER COLON IDENTIFIER')
        # Arg name = value
        @self.pg.production('parameters : IDENTIFIER EQUAL expression')
        # Arg name: expression = default value
        @self.pg.production('parameters : IDENTIFIER COLON IDENTIFIER EQUAL expression')
        def parameters(p):
            if (len(p) == 5):
                return Parameter(p[0].value, p[2], p[4])
            elif (p[1].gettokentype() == 'EQUAL'):
                arg_ = Arg(p[0].value, p[2])
                arg_.add_child(p[2])
                return arg_
            elif (p[1].gettokentype() == 'COLON'):
                par_ = Parameter(p[0].value, p[2])
                if len(p) == 5:
                    par_.add_child(p[4])
                return par_
            else:
                raise Exception(
                    'Invalid parameter/arg declaration, length=' + str(len(p)))

        @self.pg.production('parameters_list : parameters')
        @self.pg.production('parameters_list : parameters_list COMMA parameters')
        def parameters_list(p):
            if len(p) == 3:
                argList_ = ArgList(p[0].args + [p[2]])
                argList_.add_child(p[0])
                argList_.add_child(p[2])
                return argList_
            argList_ = ArgList([p[0]])
            argList_.add_child(p[0])
            return argList_

        # function declaration

        @self.pg.production('statement : FUNCTION IDENTIFIER OPEN_BRACKET CLOSE_BRACKET OPEN_CURLY_BRACKET program CLOSE_CURLY_BRACKET')
        @self.pg.production('statement : FUNCTION IDENTIFIER OPEN_BRACKET parameters_list CLOSE_BRACKET OPEN_CURLY_BRACKET program CLOSE_CURLY_BRACKET')
        def function_declaration(p):
            if (len(p) == 7):
                AssignFn_ = AssignFunction(p[1].value, ArgList([]), p[5])
                AssignFn_.add_child(p[5])
                return AssignFn_
            AssignFn_ = AssignFunction(p[1].value, p[3], p[6])
            AssignFn_.add_child(p[3])
            AssignFn_.add_child(p[6])
            return AssignFn_

        # function call
        @self.pg.production('call_function : IDENTIFIER OPEN_BRACKET CLOSE_BRACKET SEMI_COLON')
        @self.pg.production('call_function : IDENTIFIER OPEN_BRACKET parameters_list CLOSE_BRACKET SEMI_COLON')
        def function_call(p):
            if (len(p) == 4):
                return CallFunction(p[0].value,  ArgList([]))

            CallFn_ = CallFunction(p[0].value, p[2])
            CallFn_.add_child(p[2])
            return CallFn_

        @self.pg.production('expression : call_function')
        def expression_call_fn(p):
            return p[0]
        # TODO : Move the following dbs & ps commands to a preluded std libary

        @self.pg.production('statement : DEBUG_PRINT_STACK OPEN_BRACKET CLOSE_BRACKET SEMI_COLON')
        def print_stack(p):
            return DebugPrintStack()

        @self.pg.production('statement : PRINT_SCOPES OPEN_BRACKET CLOSE_BRACKET SEMI_COLON')
        def print_scopes(p):
            print("This is deprecated")
            ss = get_scope_stack()
            for s in ss:
                for child in s.children:
                    print("Child node: ", child)
                print("Parent Node", s)
            # return Print(get_scope_stack())

        @self.pg.production('expression : TYPEOF IDENTIFIER')
        @self.pg.production('expression : TYPEOF expression')
        def typeof(p):
            if type(p[1]) == Token and p[1].gettokentype() == 'IDENTIFIER':
                return TypeOf(Identifier(p[0].value))
            elif type(p[1]) != Token:
                TO_ = TypeOf(p[1])
                TO_.add_child(p[1])
                return TO_

        # comments
        @self.pg.production(r'expression : SINGLE_LINE_COMMENT')
        @self.pg.production(r'expression : MULTI_LINE_COMMENT')
        def comment(p):
            return Comment(p[0].value)

        # return statments
        @self.pg.production('statement : RETURN expression SEMI_COLON')
        def return_statement(p):
            return p[1]

        # importing

        @self.pg.production('statement : IMPORT STRING SEMI_COLON')
        def import_statement(p):
            return Import(p[1].value.replace('"', ''))

        # private variables
        @self.pg.production('statement : PRIVATE VAR IDENTIFIER COLON IDENTIFIER EQUAL expression SEMI_COLON')
        @self.pg.production('statement : PRIVATE VAR IDENTIFIER EQUAL expression SEMI_COLON')
        @self.pg.production('statement : PRIVATE VAR IDENTIFIER COLON IDENTIFIER')
        def private_var(p):
            if len(p) == 8:
                PrivateVar_ = PrivateVar(p[2].value, p[6], p[4])
                PrivateVar_.add_child(p[6])
                return PrivateVar_
            elif len(p) == 6:
                PrivateVar_ = PrivateVar(p[2].value, p[4], None)
                PrivateVar_.add_child(p[4])
                return PrivateVar_
            elif len(p) == 5:
                return PrivateVar(p[2].value, None, p[4])
            else:
                raise Exception(
                    'Invalid private variable declaration, length=' + str(len(p)))
        # class body

        @self.pg.production('class_body : program')
        @self.pg.production('class_body : class_body program')
        def class_body(p):
            if len(p) == 1:
                ClassBody_ = ClassBody([p[0]])
                ClassBody_.add_child(p[0])
            else:
                ClassBody_ = ClassBody(p[0] + p[1])
                ClassBody_.add_child(p[0])
                ClassBody_.add_child(p[1])
                return ClassBody_

        # classes                        0          1     2     3     4            5             6          7          8                  9          10
        @self.pg.production('statement : IDENTIFIER COLON COLON CLASS OPEN_BRACKET CLOSE_BRACKET IMPLEMENTS IDENTIFIER OPEN_CURLY_BRACKET class_body CLOSE_CURLY_BRACKET')
        @self.pg.production('statement : IDENTIFIER COLON COLON CLASS OPEN_BRACKET IDENTIFIER CLOSE_BRACKET OPEN_CURLY_BRACKET class_body CLOSE_CURLY_BRACKET')
        @self.pg.production('statement : IDENTIFIER COLON COLON CLASS OPEN_BRACKET CLOSE_BRACKET OPEN_CURLY_BRACKET class_body CLOSE_CURLY_BRACKET')
        @self.pg.production('statement : IDENTIFIER COLON COLON CLASS OPEN_BRACKET IDENTIFIER CLOSE_BRACKET IMPLEMENTS IDENTIFIER OPEN_CURLY_BRACKET class_body CLOSE_CURLY_BRACKET')
        def class_statement(p):
            if (len(p) == 12):
                Class_ = Class(p[0].value, p[5].value, p[10], p[8].value)
                Class_.add_child(p[10])
                return Class_
            elif (len(p) == 11):
                Class_ = Class(p[0].value, None, p[9], p[7].value)
                Class_.add_child(p[9])
                return Class_
            elif (len(p) == 10):
                Class_ = Class(p[0].value, p[5], p[8], None)
                Class_.add_child(p[8])
            elif (len(p) == 9):
                Class_ = Class(p[0].value, None, p[7], None)
                Class_.add_child(p[7])
                return Class_
            else:
                raise Exception(
                    'Invalid class statement, length=' + str(len(p)))

        # abstract classes
        @self.pg.production('statement : IDENTIFIER COLON COLON ABSTRACT CLASS OPEN_BRACKET CLOSE_BRACKET IMPLEMENTS IDENTIFIER OPEN_CURLY_BRACKET class_body CLOSE_CURLY_BRACKET')
        @self.pg.production('statement : IDENTIFIER COLON COLON ABSTRACT CLASS OPEN_BRACKET IDENTIFIER CLOSE_BRACKET OPEN_CURLY_BRACKET class_body CLOSE_CURLY_BRACKET')
        @self.pg.production('statement : IDENTIFIER COLON COLON ABSTRACT CLASS OPEN_BRACKET CLOSE_BRACKET OPEN_CURLY_BRACKET class_body CLOSE_CURLY_BRACKET')
        @self.pg.production('statement : IDENTIFIER COLON COLON ABSTRACT CLASS OPEN_BRACKET IDENTIFIER CLOSE_BRACKET IMPLEMENTS IDENTIFIER OPEN_CURLY_BRACKET class_body CLOSE_CURLY_BRACKET')
        def class_statement(p):
            if (len(p) == 13):
                AbClass_ = AbstractClass(
                    p[0].value, p[6].value, p[11], p[9].value)
                AbClass_.add_child(p[11])
                return AbClass_
            elif (len(p) == 12):
                AbClass_ = AbstractClass(p[0].value, None, p[10], p[8].value)
                AbClass_.add_child(p[10])
                return AbClass_
            elif (len(p) == 11):
                AbClass_ = AbstractClass(p[0].value, p[6], p[9].value, None)
                AbClass_.add_child(p[9])
                return AbClass_
            elif (len(p) == 10):
                AbClass_ = AbstractClass(p[0].value, None, p[8].value, None)
                AbClass_.add_child(p[8])
                return AbClass_
            else:
                raise Exception(
                    'Invalid abstract class statement, length=' + str(len(p)))

        @self.pg.production('expression : NULL')
        def null_statement(p):
            return Null()

        @self.pg.production('expression : STR OPEN_BRACKET expression CLOSE_BRACKET')
        def string_statement(p):
            return String(p[2])
        # instanciating classes

        @self.pg.production('expression : NEW IDENTIFIER OPEN_BRACKET parameters_list CLOSE_BRACKET SEMI_COLON')
        @self.pg.production('expression : NEW IDENTIFIER OPEN_BRACKET CLOSE_BRACKET SEMI_COLON')
        def new_class(p):
            # find the class in the global scope
            for class_ in global_scope["classes"]:
                if class_.name == p[1].value:
                    if type(class_) == AbstractClass:
                        raise Exception(
                            'Cannot instantiate abstract class ' + p[1].value)
                    # instanciate the class
                    if len(p) == 6:
                        return class_.instanciate(p[4])
                    elif len(p) == 5:
                        return class_.instanciate([])
                    else:
                        raise Exception(
                            'Invalid new class statement, length=' + str(len(p)))

        @self.pg.error
        def error_handle(token):
            if token.gettokentype() == '$end':
                raise Exception(
                    'Unexpected end of program (tip: are you missing a semi-colon?) ')
            elif token.gettokentype() == 'IDENTIFIER':
                raise Exception('Unexpected identifier "' + token.value +
                                '" (tip: did you forget to put quotes around the name?) ')
            else:
                raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
