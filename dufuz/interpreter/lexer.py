from sly import Lexer


class DufuzLexer(Lexer):
    tokens = {NAME, NUMBER, STRING, NOT, AND, OR, IF, WHILE, ELSE, FOR, IN, IMPORT, FROM, AS, DEF, RETURN}
    ignore = '\t '
    literals = {'.', '=', '+', '-', '/', '*', '(', ')', ',', ';', '<', '>', '[', ']', '?', '!', ':', '\n'}

    ELSE = "else"
    DEF = "def "
    NOT = "not"
    AND = "and"
    OR = "or"
    IF = "if"
    WHILE = "while"
    FOR = "for"
    IN = "in"
    IMPORT = "import"
    RETURN = "return"
    FROM = "from"
    AS = "as"
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'

    @_(r'\d*(\.)?\d+')
    def NUMBER(self, t):
        # convert it into a python integer
        if "." in t.value or "e" in t.value or "E" in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t

    @_(r'#.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')