import enum
from typing import Optional, List


class SimpleType(enum.Enum):
    NUMBER = 'number'
    STRING = 'string'
    BOOL = 'bool'
    NULL = 'null'


class CmdCode(enum.Enum):
    PUSH = 0,
    # Получить значение со стека.Берется верхушка стека
    POP = 1,
    # Сложить два верхних значения стека
    ADD = 2,
    # Вычесть два верхних значения стека
    SUB = 3,
    # Поделить два значения
    DIV = 4,
    # Перемножить два значения. Во всех четырех операциях результат кладется на стек
    MUL = 5,
    # Ввести данные
    ENTER = 6,
    # Сверка данных с шаблоном
    TEST = 7,
    # Вывести верхушку стека
    PRINT = 8,
    # Вывести все данные, которые находятся в нашей памяти
    RAM = 9,
    # Завершить работy виртуальной машины
    EXIT = 10

    READ = 20
    WRITE = 21
    ENTER_SCOPE = 22
    EXIT_SCOPE = 23



class JSValue:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def _type(self):
        if isinstance(self.value, int) or isinstance(self.value, float):
            return SimpleType.NUMBER
        if isinstance(self.value, str):
            return SimpleType.STRING
        if isinstance(self.value, bool):
            return SimpleType.BOOL
        return SimpleType.NULL

    def __add__(self, other):
        if self._type() == SimpleType.NULL:
            raise Exception('null value')

        if self._type() == SimpleType.NUMBER:
            return self.value + float(other.value)
        if self._type() == SimpleType.STRING:
            return str(self.value) + str(other.value)


class Cmd:
    def __init__(self, code: CmdCode, params: Optional[List] = None):
        self.code = code
        self.params = params
        self.index = None
        self.label = None


class JSScope:
    def __init__(self, parent: Optional[JSValue] = None):
        self.parent = parent
        self.vars = {}

    def add_var(self, name: str):
        self.vars[name] = JSValue(None)

    def read_var(self, name: str):
        curr = self
        while curr:
            if name in curr.vars:
                return curr.vars[name]
            curr = curr.parent
        return JSValue(None)

    def write_var(self, name: str, value: JSValue):
        curr = self
        last = curr
        while curr:
            if name in curr.vars:
                curr.vars[name] = value
                return
            last = curr
            curr = curr.parent
        last.vars[name] = value


class Interpreter:
    @staticmethod
    def execute(program: List[Cmd]):
        index = -1
        scope = JSScope()
        stack: List[JSValue] = []
        while index < len(program):
            index += 1
            cmd = program[index]

            if cmd.code == CmdCode.PUSH:
                stack.append(JSValue(cmd.params[0]))
                continue

            if cmd.code == CmdCode.READ:
                name = stack.pop()
                if name._type() != SimpleType.STRING:
                    raise Exception(f'name {name.value} is not string')
                value = scope.read_var(name.value)
                stack.append(value)
                continue

            if cmd.code == CmdCode.WRITE:
                name = stack.pop()
                if name._type() != SimpleType.STRING:
                    raise Exception(f'name {name.value} is not string')
                value = stack.pop()
                scope.write_var(name.value, value)
                continue

            if cmd.code == CmdCode.ENTER_SCOPE:
                scope = JSScope(scope)
                continue

            if cmd.code == CmdCode.EXIT_SCOPE:
                if not scope.parent:
                    raise Exception('no parent scope')
                scope = scope.parent
                continue

            if cmd.code == CmdCode.ADD:
                param2 = stack.pop()
                param1 = stack.pop()
                result = param1 + param2
                stack.append(result)
                continue

            if cmd.code == CmdCode.PRINT:
                param = stack.pop()
                print(str(param))
                continue

            if cmd.code == CmdCode.EXIT:
                break

            raise Exception(f'Unknown cmd {cmd.code}')


program = [
    Cmd(CmdCode.PUSH, [3]),
    Cmd(CmdCode.PUSH, ["a"]),
    Cmd(CmdCode.WRITE),
    Cmd(CmdCode.PUSH, [4]),
    Cmd(CmdCode.PUSH, ["b"]),
    Cmd(CmdCode.WRITE),
    Cmd(CmdCode.PUSH, ["a"]),
    Cmd(CmdCode.READ),
    Cmd(CmdCode.PUSH, ["b"]),
    Cmd(CmdCode.READ),
    Cmd(CmdCode.ADD),
    Cmd(CmdCode.PUSH, ["c"]),
    Cmd(CmdCode.WRITE),
    Cmd(CmdCode.PUSH, ["c"]),
    Cmd(CmdCode.READ),
    Cmd(CmdCode.PRINT),
    Cmd(CmdCode.EXIT),
]

Interpreter.execute(program)
