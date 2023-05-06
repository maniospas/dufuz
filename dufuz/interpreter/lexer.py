from sly import Lexer


class DufuzLexer(Lexer):
    tokens = {NAME, NUMBER, STRING, NOT, AND, OR, IF, WHILE, ELSE, FOR, IN, IMPORT, FROM, AS, DEF, RETURN, NEQ,
              LE, GE, LT, GT, EQ, ASSIGN, DOT, BREAK}

    ignore = '\t '
    literals = {'+', '-', '/', '*', '(', ')', '[', ']', '?', ':', ','}

    ELSE = r"else"
    DEF = r"def "
    NOT = r"not "
    AND = r"and "
    OR = r"or "
    IF = r"if "
    WHILE = r"while "
    FOR = r"for "
    IN = r"in "
    IMPORT = r"import "
    RETURN = r"return"
    FROM = r"from "
    BREAK = r"break"
    AS = r"as"
    DOT = r"\."
    NEQ = r"\!\="
    GE = r"\>\="
    LE = r"\<\="
    EQ = r"\=\="
    GT = r"\>"
    LT = r"\<"
    ASSIGN = r"\="
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