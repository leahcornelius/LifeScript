from rply import ParserGenerator, Token
from pprint import pprint
from ast_objects import *


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
             "TYPE", "CLASS", "IMPLEMENTS", "EXTENDS", "ABSTRACT", "PRIVATE", "NEW"
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
        # Main function.
        @self.pg.production('program : statement_list')
        def program(p):
            return p[0]

        @self.pg.production('statement_list : statement SEMI_COLON')
        @self.pg.production('statement_list : statement')
        def statement_list(p):
            return StatmentList([p[0]])

        @self.pg.production('statement_list : statement_list statement SEMI_COLON')
        @self.pg.production('statement_list : statement_list statement')
        def statement_list(p):
            return StatmentList([p[0], p[1]])

        @self.pg.production('expression : IDENTIFIER')
        def statement(p):
            return Identifier(p[0].getstr())

        @self.pg.production('statement : PRINT OPEN_BRACKET expression CLOSE_BRACKET SEMI_COLON')
        def statement(p):
            return Print(p[2])

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
            return ConditionResolver(p[0], p[1].gettokentype(), p[2])

        @self.pg.production('expression : expression PLUS expression')
        @self.pg.production('expression : expression MINUS expression')
        @self.pg.production('expression : expression MUL expression')
        @self.pg.production('expression : expression DIV expression')
        def expression(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'PLUS':
                return Sum(left, right)
            elif operator.gettokentype() == 'MINUS':
                return Sub(left, right)
            elif operator.gettokentype() == 'MUL':
                return Multiply(left, right)
            elif operator.gettokentype() == 'DIV':
                return Divide(left, right)
            else:
                raise Exception("Unknown operator: " + operator.gettokentype())

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

        @self.pg.production('statement : OPEN_CURLY_BRACKET statement CLOSE_CURLY_BRACKET')
        def expression_curly(p):
            return p[1]

        @self.pg.production('expression : STRING')
        def string(p):
            return String(p[0].value)

        @self.pg.production('expression : condition')
        def expression_condition(p):
            return p[0]

        @self.pg.production('statement : expression')
        def debug_statement(p):
            return Print(p[0])

        @self.pg.production('expression : expression PERCENT expression')
        def expression_modulo(p):
            left = p[0]
            right = p[2]
            return Modulo(left, right)

        @self.pg.production('statement : VAR IDENTIFIER EQUAL expression SEMI_COLON')
        @self.pg.production('statement : LET IDENTIFIER EQUAL expression SEMI_COLON')
        @self.pg.production('statement : LET IDENTIFIER COLON LESS_THAN expression GREATER_THAN EQUAL expression SEMI_COLON')
        def expression_assign(p):
            # Check if the type has been declared
            if p[2].gettokentype() == 'COLON' and p[3].gettokentype() == 'LESS_THAN' and p[5].gettokentype() == 'GREATER_THAN':
                return Assign(p[1].value, p[7], p[4])
            name = p[1].value
            value = p[3]
            return Assign(name, value, None)
        #                                0  1            2         3             4                  5       6                   7                  8       9

        @self.pg.production('statement : IF OPEN_BRACKET condition CLOSE_BRACKET OPEN_CURLY_BRACKET program CLOSE_CURLY_BRACKET OPEN_CURLY_BRACKET program CLOSE_CURLY_BRACKET')
        @self.pg.production('statement : IF OPEN_BRACKET condition CLOSE_BRACKET OPEN_CURLY_BRACKET program CLOSE_CURLY_BRACKET')
        def expression_if(p):
            condition = p[3].gettokentype()
            if len(p) == 10:
                return If(condition, p[6], p[8])
            elif len(p) == 7:
                return If(p[2], p[5], None)
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
                return Arg(p[0].value, p[2])
            elif (p[1].gettokentype() == 'COLON'):
                return Parameter(p[0].value, p[2])

        @self.pg.production('parameters_list : parameters')
        @self.pg.production('parameters_list : parameters_list COMMA parameters')
        def parameters_list(p):
            if len(p) == 3:
                return ArgList(p[0].args + [p[2]])
            return ArgList([p[0]])

        # function declaration

        @self.pg.production('statement : FUNCTION IDENTIFIER OPEN_BRACKET CLOSE_BRACKET OPEN_CURLY_BRACKET program CLOSE_CURLY_BRACKET')
        @self.pg.production('statement : FUNCTION IDENTIFIER OPEN_BRACKET parameters_list CLOSE_BRACKET OPEN_CURLY_BRACKET program CLOSE_CURLY_BRACKET')
        def function_declaration(p):
            if (len(p) == 7):
                return AssignFunction(p[1].value, [], p[5])
            return AssignFunction(p[1].value, p[3], p[6])

        # function call
        @self.pg.production('statement : IDENTIFIER OPEN_BRACKET CLOSE_BRACKET SEMI_COLON')
        @self.pg.production('statement : IDENTIFIER OPEN_BRACKET parameters_list CLOSE_BRACKET SEMI_COLON')
        def function_call(p):
            if (len(p) == 4):
                return CallFunction(p[0].value, [])
            return CallFunction(p[0].value, p[2])

        @self.pg.production('statement : DEBUG_PRINT_STACK OPEN_BRACKET CLOSE_BRACKET SEMI_COLON')
        def print_stack(p):
            return DebugPrintStack()

        @self.pg.production('expression : TYPEOF IDENTIFIER')
        @self.pg.production('expression : TYPEOF expression')
        def typeof(p):
            if type(p[1]) == Token and p[1].gettokentype() == 'IDENTIFIER':
                return TypeOf(Identifier(p[0].value))
            elif type(p[1]) != Token:
                return TypeOf(p[1])

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
                return PrivateVar(p[2].value, p[6], p[4])
            elif len(p) == 6:
                return PrivateVar(p[2].value, p[4], None)
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
                return ClassBody([p[0]])
            else:
                return ClassBody(p[0] + p[1])

        # classes                        0          1     2     3     4            5             6          7          8                  9          10
        @self.pg.production('statement : IDENTIFIER COLON COLON CLASS OPEN_BRACKET CLOSE_BRACKET IMPLEMENTS IDENTIFIER OPEN_CURLY_BRACKET class_body CLOSE_CURLY_BRACKET')
        @self.pg.production('statement : IDENTIFIER COLON COLON CLASS OPEN_BRACKET IDENTIFIER CLOSE_BRACKET OPEN_CURLY_BRACKET class_body CLOSE_CURLY_BRACKET')
        @self.pg.production('statement : IDENTIFIER COLON COLON CLASS OPEN_BRACKET CLOSE_BRACKET OPEN_CURLY_BRACKET class_body CLOSE_CURLY_BRACKET')
        @self.pg.production('statement : IDENTIFIER COLON COLON CLASS OPEN_BRACKET IDENTIFIER CLOSE_BRACKET IMPLEMENTS IDENTIFIER OPEN_CURLY_BRACKET class_body CLOSE_CURLY_BRACKET')
        def class_statement(p):
            if (len(p) == 12):
                return Class(p[0].value, p[5].value, p[10], p[8].value)
            elif (len(p) == 11):
                return Class(p[0].value, None, p[9], p[7].value)
            elif (len(p) == 10):
                return Class(p[0].value, p[5], p[8], None)
            elif (len(p) == 9):
                return Class(p[0].value, None, p[7], None)
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
                return AbstractClass(p[0].value, p[6].value, p[11], p[9].value)
            elif (len(p) == 12):
                return AbstractClass(p[0].value, None, p[10], p[8].value)
            elif (len(p) == 11):
                return AbstractClass(p[0].value, p[6], p[9].value, None)
            elif (len(p) == 10):
                return AbstractClass(p[0].value, None, p[8].value, None)
            else:
                raise Exception(
                    'Invalid abstract class statement, length=' + str(len(p)))

        # instanciating classes
        @self.pg.production('expression : NEW IDENTIFIER OPEN_BRACKET parameters_list CLOSE_BRACKET SEMI_COLON')
        @self.pg.production('expression : NEW IDENTIFIER OPEN_BRACKET CLOSE_BRACKET SEMI_COLON')
        def new_class(p):
            # find the class in the global scope
            for class_ in global_scope["classes"]:
                if class_.name == p[1].value:
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
