from rply import ParserGenerator

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
             '$end', 'NEWLINE', 'FUNCTION', 'SEMI_COLON', 'PRINT', 'PERCENT', "DOT"

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

        @self.pg.production('statement : expression')
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
        def expression(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'PLUS':
                return Sum(left, right)
            elif operator.gettokentype() == 'MINUS':
                return Sub(left, right)

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

        # type
        @self.pg.production('type : STRING')
        def type(p):
            return Type(p[0].value)
        # parameters

        @self.pg.production('parameters : IDENTIFIER COLON type')
        @self.pg.production('parameters : IDENTIFIER EQUAL expression')
        def parameters(p):
            if (len(p) == 3):
                return Arg(p[0].value, p[2])
            return ParameterDeclaration(p[0].value, p[2])

        # function declaration
        @self.pg.production('statement : FUNCTION IDENTIFIER OPEN_BRACKET CLOSE_BRACKET OPEN_CURLY_BRACKET statement CLOSE_CURLY_BRACKET')
        @self.pg.production('statement : FUNCTION IDENTIFIER OPEN_BRACKET parameters CLOSE_BRACKET OPEN_CURLY_BRACKET statement CLOSE_CURLY_BRACKET')
        def function_declaration(p):
            if (len(p) == 7):
                return AssignFunction(p[1].value, None, p[5])
            return AssignFunction(p[1].value, p[3], p[6])

        # function call
        @self.pg.production('statement : IDENTIFIER OPEN_BRACKET CLOSE_BRACKET SEMI_COLON')
        @self.pg.production('statement : IDENTIFIER OPEN_BRACKET parameters CLOSE_BRACKET SEMI_COLON')
        def function_call(p):
            if (len(p) == 4):
                return CallFunction(p[0].value, None)
            return CallFunction(p[0].value, p[2])

        @self.pg.production('statement : STRING OPEN_BRACKET CLOSE_BRACKET')
        def print_stack(p):
            return DebugPrintStack()

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
