
from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Type Detector
        self.lexer.add('INTEGER', '-?\d+')
        self.lexer.add('FLOAT', '-?\d+.\d+')
        self.lexer.add('STRING', '"(.*?)"|\'(.*?)\'')
        self.lexer.add('BOOLEAN', "true(?!\w)|false(?!\w)")
        # Keywords
        self.lexer.add('IF', 'if(?!\w)')
        self.lexer.add('ELSE', 'else(?!\w)')
        self.lexer.add('END', 'end(?!\w)')
        self.lexer.add('AND', r"and(?!\w)")
        self.lexer.add('OR', r"or(?!\w)")
        self.lexer.add('NOT', r"not(?!\w)")
        self.lexer.add('LET', r'let(?!\w)')
        self.lexer.add('VAR', r'var(?!\w)')
        self.lexer.add('PRINT', r"print(?!\w)")
        self.lexer.add('FUNCTION', r'func(?!\w)')
        self.lexer.add('MODULE', r'mod(?!\w)')
        self.lexer.add('IMPORT', r'import(?!\w)')
        self.lexer.add('RETURN', r'return(?!\w)')
        self.lexer.add('IN', r'in(?!\w)')
        self.lexer.add('AS', r'as(?!\w)')
        self.lexer.add('WHILE', r'while(?!\w)')
        self.lexer.add('FOR', r'for(?!\w)')
        self.lexer.add('BREAK', r'break(?!\w)')
        self.lexer.add('CONTINUE', r'continue(?!\w)')
        self.lexer.add('TYPEOF', r'typeof(?!\w)')
        self.lexer.add('TYPE', r'Type(?!\w)')
        self.lexer.add('CLASS', r'Class(?!\w)')
        self.lexer.add('EXTENDS', r'extends(?!\w)')
        self.lexer.add('IMPLEMENTS', r'implements(?!\w)')
        self.lexer.add('ABSTRACT', r'abstract(?!\w)')
        self.lexer.add('PRIVATE', r'private(?!\w)')
        self.lexer.add('NEW', r'new(?!\w)')

        self.lexer.add('STR', r'str(?!\w)')
        self.lexer.add('INT', r'int(?!\w)')
        self.lexer.add('FLOAT', r'float(?!\w)')
        self.lexer.add('BOOL', r'bool(?!\w)')
        self.lexer.add('NULL', r'Null(?!\w)')

        self.lexer.add('DEBUG_PRINT_STACK', r'dps(?!\w)')
        self.lexer.add('PRINT_SCOPES', r'ps(?!\w)')

        # Identifiers (var, function names)
        self.lexer.add('IDENTIFIER', r"[a-zA-Z_][a-zA-Z0-9_]*")

        # Signs
        self.lexer.add('EQ', '==')
        self.lexer.add('NEQ', '!=')
        self.lexer.add('GREATER_THAN_EQ', '>=')
        self.lexer.add('LESS_THAN_EQ', '<=')
        self.lexer.add('GREATER_THAN', '>')
        self.lexer.add('LESS_THAN', r'\<')
        self.lexer.add('LEFT_SHIFT', r'\<\<')
        self.lexer.add('RIGHT_SHIFT', r'\>\>')
        self.lexer.add('PERCENT', r'\%')
        self.lexer.add("SINGLE_LINE_COMMENT", r'//.*')
        self.lexer.add("MULTI_LINE_COMMENT", r'\/\*(.*?)\*\/')

        self.lexer.add('EQUAL', r'\=')
        self.lexer.add('OPEN_SQUARE-BRACKET', r'\[')
        self.lexer.add('CLOSE_SQUARE_BRACKET', r'\]')
        self.lexer.add('OPEN_CURLY_BRACKET', r'\{')
        self.lexer.add('CLOSE_CURLY_BRACKET', r'\}')
        self.lexer.add('|', r'\|')
        self.lexer.add('COMMA', r'\,')
        self.lexer.add('DOT', r'\.')
        self.lexer.add('COLON', r'\:')
        self.lexer.add('PLUS', r'\+')
        self.lexer.add('MINUS', '-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'\/')
        self.lexer.add('MOD', r'\%')
        self.lexer.add('OPEN_BRACKET', r'\(')
        self.lexer.add('CLOSE_BRACKET', r'\)')
        self.lexer.add('SEMI_COLON', r'\;')

        # ignore whitespace
        self.lexer.ignore('[ \t\r\f\v\n]+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
