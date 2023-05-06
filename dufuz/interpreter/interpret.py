from dufuz.interpreter.lexer import DufuzLexer
from dufuz.interpreter.parser import DufuzParser
from dufuz.core import Number, Domain
import operator
import torch


class Range:
    def __init__(self, env):
        self.env = env

    def __call__(self, a, b=None, inc=None):
        if b is None:
            a, b = 0, a
        if inc is None:
            inc = 1
        x = a if isinstance(a, Number) else Number([1], Domain([a], self.env.spawner))
        while True:
            next_x = x+inc
            comparison = self.env.spawner.apply(operator.lt, next_x, b)  # treat crisp arithmetics as fuzzy too
            if comparison.todict().get(True, 0) <= 0:
                break
            toyield = self.env.spawner.If(comparison, x, None)
            yield toyield
            x = next_x


class Variable:
    def __init__(self, executor, name):
        self.executor = executor
        self.name = name

    def __str__(self):
        return self.name + " = " + str(self.executor.env.get(self.name, "None"))

    def assign(self, value):
        self.executor.env[self.name] = value

    def get(self):
        return self.executor.env[self.name]


class Element:
    def __init__(self, executor, values, element):
        self.executor = executor
        if isinstance(values, Variable):
            values = values.get()
        self.values = values
        if isinstance(element, Variable):
            element = element.get()
        self.element = element

    def assign(self, value):
        self.executor.spawner.setlist(self.values, self.element, value)


class Iter:
    def __init__(self, list):
        self.list = list

    def __add__(self, other):
        return Iter(self.list + other.list)

    def __str__(self):
        return "iter "+str(self.list)

    def assign(self, vals):
        for var, val in zip(self.list, vals):
            var.assign(val)

_DUFUZKWARG = list()


class Executor:
    def __init__(self, spawner):
        self.spawner = spawner
        self.env = {"print": print,
                    "int": int,
                    "float": float,
                    "range": Range(self),
                    "list": list,
                    "map": map,
                    "len": len,
                    "str": str,
                    "zip": zip,
                    "True": True,
                    "False": False}
        self.asvar = False
        self.asname = False
        self.callenv = list()

    def run(self, tree, asvar=None):
        if not isinstance(tree, tuple):
            return tree
        if asvar is not None:
            self.asvar = asvar
        #if tree[0] == "kwarg" and not self.callenv:  # this is a fix for parsing conflict
        #    tree = ("assign", ("var", tree[1]), tree[2])
        if tree[0] == "assign":
            self.asvar = True
            var = self.run(tree[1])
            self.asvar = False
            val = self.run(tree[2])
            var.assign(val)
            return None
        if tree[0] == "kwarg":
            var = tree[1]
            val = self.run(tree[2])
            self.callenv[-1][var] = val
            return _DUFUZKWARG
        elif tree[0] == "attr":
            if isinstance(tree[2], tuple) and tree[2][0] == "var":
                tree = (tree[0], tree[1], tree[2][1])
            var = self.run(tree[1])
            val = self.run(tree[2])
            return getattr(var, val)
        elif tree[0] == "call":
            self.callenv.append(dict())
            args = tree[1:]
            args = [self.run(arg) for arg in args]
            ret = getattr(self, tree[0])(*args, **self.callenv[-1])
            self.callenv.pop()
            if asvar is not None:
                self.asvar = False
            return ret
        args = tree[1:]
        args = [self.run(arg) for arg in args]
        ret = getattr(self, tree[0])(*args)
        if asvar is not None:
            self.asvar = False
        return ret

    def notop(self, value):
        return self.spawner.Not(value)

    def list(self, iterator):
        if not isinstance(iterator, Iter):
            return [iterator]
        return iterator.list

    def next(self, element, next):
        if not isinstance(next, Iter):
            next = Iter([next])
        if not isinstance(element, Iter):
            element = Iter([element])
        return element + next

    def get(self, values, element):
        if self.asvar:
            return Element(self, values, element)
        if isinstance(values, tuple):
            return values[element]
        return self.spawner.getlist(values, element)

    def number(self, number):
        return self.spawner.number(number, breadth=0)

    def scope(self, result):
        return result

    def fuzzy(self, number, breadth):
        return self.spawner.number(number, breadth=breadth)

    def assignee(self, name):
        if self.asname:
            return name
        return Variable(self, name)

    def var(self, name):
        if self.asname:
            return name
        if self.asvar:
            return Variable(self, name)
        return self.env[name]

    def call(self, func, *args, **kwargs):
        assert len(args) <= 1
        if args:
            args = args[0]
            if isinstance(args, Iter):
                args = args.list
            else:
                args = [args]
        if args:
            args = [arg for arg in args if id(arg) != id(_DUFUZKWARG)]
        return func(*args, **kwargs)

    def eq(self, x, y):
        return x == y

    def mul(self, x, y):
        return x * y

    def add(self, x, y):
        return x + y

    def andop(self, x, y):
        return x & y

    def orop(self, x, y):
        return x | y

    def sub(self, x, y):
        return x - y

    def neg(self, x):
        return -x

    def div(self, x, y):
        return x / y

    def le(self, x, y):
        return x <= y

    def ge(self, x, y):
        return x >= y

    def lt(self, x, y):
        return x < y

    def gt(self, x, y):
        return x > y

    def ne(self, x, y):
        return x != y

    def condition(self, cond, primary, secondary):
        return cond.choose(primary, secondary)

    def importmodule(self, name, alias):
        import importlib
        self.env[alias] = importlib.import_module(name)

    def importmember(self, module, name, alias):
        import importlib
        module = importlib.import_module(module)
        self.env[alias] = getattr(module, name)


class Func:
    def __init__(self, path, executor, parser, lexer, lines, args, ret_env=False):
        self.path = path
        self.executor = executor
        self.lines = lines
        self.parser = parser
        self.lexer = lexer
        self.args = args
        self.ret_env = ret_env

    def __call__(self, *args, **kwargs):
        prev_env = self.executor.env
        self.executor.env = {k: v for k, v in self.executor.env.items()}
        loops = list()
        parser = self.parser
        lexer = self.lexer
        executor = self.executor
        lines = self.lines
        for name, val in zip(self.args, args):
            self.executor.env[name] = val
        i = 0
        while i < len(lines):
            line = lines[i]
            #print(i, line, len(loops))
            stripped_line = line.lstrip()
            block = len(line)-len(stripped_line)
            repeat_loop = None
            while loops and loops[-1][2] >= block:
                try:
                    element = next(loops[-1][4])
                    repeat_loop = loops[-1][1]
                    var = loops[-1][3]
                    if isinstance(var, Iter):
                        for var, element in zip(var.list, element):
                            var.assign(element)
                    else:
                        var.assign(element)
                    break
                except StopIteration:
                    loops.pop()
            if repeat_loop:
                i = repeat_loop
                continue
            if not line.strip():
                i += 1
                continue
            tree = parser.parse(lexer.tokenize(stripped_line))
            #print(list(lexer.tokenize(stripped_line)))
            if not tree:
                print(line)
                raise Exception("Invalid expression at file\""+self.path+"\", line "+str(i))
            if tree[0] == "def":
                func_name = tree[1]
                func_lines = list()
                func_args = executor.run(tree[2], asvar=True).list if isinstance(tree[2], tuple) and tree[2][0] == "next" else [executor.run(tree[2], asvar=True)]
                func_args = [arg.name for arg in func_args]
                i += 1
                while i < len(lines):
                    if not lines[i].strip():
                        i += 1
                        continue
                    depth = len(lines[i])-len(lines[i].lstrip())
                    if depth <= block:
                        break
                    func_lines.append(lines[i])
                    i += 1
                func_lines.append("")
                executor.env[func_name] = Func(func_name, executor, parser, lexer, func_lines, func_args)
                i -= 1
            if tree[0] == "while":
                while_condition = tree[1]
                while_lines = list()
                i += 1
                while i < len(lines):
                    if not lines[i].strip():
                        i += 1
                        continue
                    depth = len(lines[i])-len(lines[i].lstrip())
                    if depth <= block:
                        break
                    while_lines.append(lines[i])
                    i += 1
                while_lines.append("")
                loop = Func(str(while_condition), executor, parser, lexer, while_lines, [], ret_env=True)
                appended_env = dict()#{k: v for k, v in self.executor.env.items()}
                prev_cond = Number([1], Domain([True], self.executor.spawner))
                while True:
                    condition = self.executor.run(while_condition)
                    if not isinstance(condition, Number):
                        condition = Number([1], Domain([condition], self.executor.spawner))
                    residual = Number([prev_cond.todict().get(True, 0), 1-prev_cond.todict().get(True, 0)], Domain([True, False], self.executor.spawner))
                    prev_cond = self.executor.spawner.And(condition, residual)
                    print(residual, condition, prev_cond)
                    condition = prev_cond
                    for k, v in self.executor.env.items():
                        if isinstance(v, Number) or isinstance(appended_env.get(k, None), Number):
                            v = condition.choose(None, v)
                            if k in appended_env:
                                appended_env[k] = self.executor.spawner.combine(v, appended_env[k])
                            else:
                                appended_env[k] = condition.choose(None, v)
                        else:
                            appended_env[k] = v
                    if condition.todict().get(True, 0) == 0:
                        break
                    self.executor.env = loop()
                i -= 1
                for k, v in appended_env.items():
                    self.executor.env[k] = v
            elif tree[0] == "return":
                ret = executor.run(tree[1])
                self.executor.env = prev_env
                return ret
            elif tree[0] == "break":
                self.executor.env = prev_env
                internal_env = self.executor.env
                self.executor.env = prev_env
                if self.ret_env:
                    return internal_env
                return
            elif tree[0] == "for":
                loops.append(("for", i+1, block, executor.run(tree[1], asvar=True), iter(executor.run(tree[2]))))
                try:
                    element = next(loops[-1][4])
                    var = loops[-1][3]
                    if isinstance(var, Iter):
                        for var, element in zip(var.list, element):
                            var.assign(element)
                    else:
                        var.assign(element)
                except StopIteration:
                    loops.pop()
            else:
                executor.run(tree)
            i += 1
        internal_env = self.executor.env
        self.executor.env = prev_env
        if self.ret_env:
            return internal_env
        return None


def interpret(environment, path):
    lexer = DufuzLexer()
    parser = DufuzParser()
    executor = Executor(environment)
    with open(path) as file:
        lines = [line for line in file]+[""]
    return Func(path, executor, parser, lexer, lines, [])()