from dufuz.interpreter.lexer import DufuzLexer
from sly import Parser


class DufuzParser(Parser):
    tokens = DufuzLexer.tokens

    precedence = (
        ('left', '(', ')'),
        ('left', '[', ']'),
        ('left', ','),
        ('left', ASSIGN),
        ('left', NAME, NUMBER, STRING),
        ('left', RETURN),
        ('left', DEF),
        ('left', WHILE, FOR, IN, IF, ELSE, ':'),
        ('left', NOT),
        ('left', OR),
        ('left', AND),
        ('left', LE, GE, LT, GT, EQ),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('left', FROM, IMPORT, AS),
        ('left', DOT),
    )

    @_('IMPORT namespace')
    def statement(self, p):
        return "importmodule", p.namespace, p.namespace

    @_('IMPORT namespace AS NAME')
    def statement(self, p):
        return "importmodule", p.namespace, p.NAME

    @_('FROM namespace IMPORT NAME')
    def statement(self, p):
        return "importmember", p.namespace, p.NAME, p.NAME

    @_('FROM namespace IMPORT NAME AS NAME')
    def statement(self, p):
        return "importmember", p.namespace, p.NAME0, p.NAME1

    @_('NAME DOT namespace')
    def namespace(self, p):
        return p.NAME + "." + p.namespace

    @_('NAME')
    def namespace(self, p):
        return p.NAME

    @_('assignee ASSIGN expr')
    def statement(self, p):
        return "assign", p.assignee, p.expr

    @_('FOR names IN expr ":"')
    def statement(self, p):
        return "for", p.names, p.expr

    @_('NAME')
    def names(self, p):
        return "assignee", p.NAME

    @_('names "," names')
    def names(self, p):
        return "next", p.names0, p.names1

    @_('DEF NAME "(" args ")" ":"')
    def statement(self, p):
        return "def", p.NAME, p.args

    @_('RETURN expr')
    def statement(self, p):
        return "return", p.expr

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('args "," args')
    def args(self, p):
        return "next", p.args0, p.args1

    @_('expr')
    def args(self, p):
        return p.expr

    @_('NAME ASSIGN expr')
    def args(self, p):
        return "kwarg", p.NAME, p.expr

    @_('expr IF expr ELSE expr')
    def expr(self, p):
        return "condition", p.expr1, p.expr0, p.expr2

    @_('expr DOT NAME')
    def expr(self, p):
        return "attr", p.expr, p.NAME

    @_('expr "(" args ")"')
    def expr(self, p):
        return "call", p.expr, p.args

    @_('expr "(" ")"')
    def expr(self, p):
        return "call", p.expr

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('expr "[" expr "]"')
    def expr(self, p):
        return "get", p.expr0, p.expr1

    @_('"[" elements "]"')
    def expr(self, p):
        return "list", p.elements

    @_('expr')
    def elements(self, p):
        return p.expr

    @_('elements "," elements')
    def elements(self, p):
        return "next", p.elements0, p.elements1

    @_('expr EQ expr')
    def expr(self, p):
        return "eq", p.expr0, p.expr1

    @_('expr LE expr')
    def expr(self, p):
        return "le", p.expr0, p.expr1

    @_('expr GE expr')
    def expr(self, p):
        return "ge", p.expr0, p.expr1

    @_('expr "+" expr')
    def expr(self, p):
        return "add", p.expr0, p.expr1

    @_('expr "-" expr')
    def expr(self, p):
        return "sub", p.expr0, p.expr1

    @_('expr "*" expr')
    def expr(self, p):
        return "mul", p.expr0, p.expr1

    @_('expr "/" expr')
    def expr(self, p):
        return "div", p.expr0, p.expr1

    @_('expr LT expr')
    def expr(self, p):
        return "lt", p.expr0, p.expr1

    @_('expr GT expr')
    def expr(self, p):
        return "gt", p.expr0, p.expr1

    @_('expr NEQ expr')
    def expr(self, p):
        return "ne", p.expr0, p.expr1

    @_('expr AND expr')
    def expr(self, p):
        return "andop", p.expr0, p.expr1

    @_('expr OR expr')
    def expr(self, p):
        return "orop", p.expr0, p.expr1

    @_('assignee "," assignee')
    def assignee(self, p):
        return "next", p.assignee0, p.assignee1

    @_('assignee "[" expr "]"')
    def assignee(self, p):
        return "get", p.assignee, p.expr

    #@_('assignee DOT NAME')
    #def assignee(self, p):
    #    return "attr", p.assignee, p.NAME

    @_('NAME')
    def assignee(self, p):
        return ("assignee", p.NAME)

    @_('NOT expr')
    def expr(self, p):
        return "notop", p.expr

    @_('NUMBER')
    def expr(self, p):
        return "number", p.NUMBER

    @_('NUMBER "?"')
    def expr(self, p):
        return "fuzzy", p.NUMBER, 1

    @_('NUMBER "?" NUMBER')
    def expr(self, p):
        return "fuzzy", p.NUMBER0, p.NUMBER1

    @_('NAME')
    def expr(self, p):
        return "var", p.NAME

    @_('STRING')
    def expr(self, p):
        return "number", p.STRING[1:-1]
