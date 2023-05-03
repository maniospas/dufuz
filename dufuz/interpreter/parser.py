from dufuz.interpreter.lexer import DufuzLexer
from sly import Parser


class DufuzParser(Parser):
    tokens = DufuzLexer.tokens

    precedence = (
        ('left', AND, OR),
        ('nonassoc', '<', '>', '='),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('nonassoc', '.'),
    )

    @_('IMPORT NAME')
    def statement(self, p):
        return ("importmodule", p.NAME, p.NAME)

    @_('IMPORT NAME AS NAME')
    def statement(self, p):
        return ("importmodule", p.NAME0, p.NAME1)

    @_('IMPORT NAME "." NAME AS NAME')
    def statement(self, p):
        return ("importmodule", p.NAME0+"."+p.NAME1, p.NAME2)

    @_('FROM NAME IMPORT NAME')
    def statement(self, p):
        return ("importmember", p.NAME0, p.NAME1, p.NAME1)

    @_('FROM NAME IMPORT NAME AS NAME')
    def statement(self, p):
        return ("importmember", p.NAME0, p.NAME1, p.NAME2)

    @_('expr "=" expr')
    def statement(self, p):
        return ("assign", p.expr0, p.expr1)

    @_('FOR expr IN expr ":"')
    def statement(self, p):
        return ("for", p.expr0, p.expr1)

    @_('DEF NAME "(" args ")" ":"')
    def statement(self, p):
        return ("def", p.NAME, p.args)

    @_('NAME "=" expr')
    def args(self, p):
        return ("kwarg", p.NAME, p.expr)

    @_('args "," args')
    def args(self, p):
        return ("next", p.args0, p.args1)

    @_('expr')
    def args(self, p):
        return p.expr

    @_('RETURN expr')
    def statement(self, p):
        return ("return", p.expr)

    @_('expr IF expr ELSE expr')
    def expr(self, p):
        return ("condition", p.expr1, p.expr0, p.expr2)

    @_('expr')
    def statement(self, p):
        return ("scope", p.expr)

    @_('expr "." expr')
    def expr(self, p):
        return ("attr", p.expr0, p.expr1)

    @_('expr "(" args ")"')
    def expr(self, p):
        return ("call", p.expr, p.args)

    @_('expr "(" ")"')
    def expr(self, p):
        return ("call", p.expr)

    @_('"(" expr ")"')
    def expr(self, p):
        return (p.expr)

    @_('expr "[" expr "]"')
    def expr(self, p):
        return ("get", p.expr0, p.expr1)

    @_('"[" expr "]"')
    def expr(self, p):
        return ("list", p.expr)

    @_('expr "=" "=" expr')
    def expr(self, p):
        return ("eq", p.expr0, p.expr1)

    @_('expr "<" "=" expr')
    def expr(self, p):
        return ("le", p.expr0, p.expr1)

    @_('expr ">" "=" expr')
    def expr(self, p):
        return ("ge", p.expr0, p.expr1)

    @_('expr "+" expr')
    def expr(self, p):
        return ("add", p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ("sub", p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ("mul", p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ("div", p.expr0, p.expr1)

    @_('expr "<" expr')
    def expr(self, p):
        return ("lt", p.expr0, p.expr1)

    @_('expr ">" expr')
    def expr(self, p):
        return ("gt", p.expr0, p.expr1)

    @_('expr "!" "=" expr')
    def expr(self, p):
        return ("ne", p.expr0, p.expr1)

    @_('expr AND expr')
    def expr(self, p):
        return ("andop", p.expr0, p.expr1)

    @_('expr OR expr')
    def expr(self, p):
        return ("orop", p.expr0, p.expr1)

    @_('expr "," expr')
    def expr(self, p):
        return ("next", p.expr0, p.expr1)

    @_('NOT expr')
    def expr(self, p):
        return ("notop", p.expr)

    @_('NUMBER')
    def expr(self, p):
        return ("number", p.NUMBER)

    @_('NUMBER "?"')
    def expr(self, p):
        return ("fuzzy", p.NUMBER, 1)

    @_('NUMBER "?" NUMBER')
    def expr(self, p):
        return ("fuzzy", p.NUMBER0, p.NUMBER1)

    @_('NAME')
    def expr(self, p):
        return ("var", p.NAME)

    @_('STRING')
    def expr(self, p):
        return ("number", p.STRING[1:-1])
