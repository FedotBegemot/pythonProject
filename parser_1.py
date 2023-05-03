import enum
from typing import Optional, List


class SimpleType(enum.Enum):
    NUMBER = 'number'
    STRING = 'string'
    BOOL = 'bool'
    NULL = 'null'

class ObjectType(enum.Enum):
    DICT = 'dictionary'
    LIST = 'list'
    FUNC = 'function'

class CmdCode(enum.Enum):
    PUSH = 0
    # Получить значение со стека.Берется верхушка стека
    POP = 1
    # Сложить два верхних значения стека
    ADD = 2
    # Вычесть два верхних значения стека
    SUB = 3
    # Поделить два значения
    FLOOR_DIV = 4
    TRUE_DIV = 11
    # Перемножить два значения. Во всех четырех операциях результат кладется на стек
    MUL = 5
    # Ввести данные
    ENTER = 6
    # Сверка данных с шаблоном
    TEST = 7
    # Вывести верхушку стека
    PRINT = 8
    # Вывести все данные, которые находятся в нашей памяти
    RAM = 9
    # Завершить работy виртуальной машины
    EXIT = 10
    POW = 12
    MODULE = 13
    COMPARISON = 14
    EQUAL = 15
    NEGATIVE = 16
    JUMP = 17

    READ = 20
    WRITE = 21
    ENTER_SCOPE = 22
    EXIT_SCOPE = 23
    CALL = 24
    DEF_FUNC = 25


class JSValue:
    def __init__(self, value, func_addr: Optional[int] = None):
        self.value = value
        self.func_addr = func_addr

    def __str__(self):
        return str(self.value)

    def _type(self):
        if isinstance(self.value, bool):
            return SimpleType.BOOL
        if isinstance(self.value, int) or isinstance(self.value, float):
            return SimpleType.NUMBER
        if isinstance(self.value, str):
            return SimpleType.STRING
        if isinstance(self.value, function):
            return ObjectType.FUNC
        if isinstance(self.value, dict):
            return ObjectType.DICT
        if isinstance(self.value, list):
            return ObjectType.LIST
        return SimpleType.NULL


    def __add__(self, other):
        if self._type() == SimpleType.NULL:
            raise Exception('null value')
        if self._type() == SimpleType.BOOL:
            return bool(self.value) or bool(other.value)
        if self._type() == SimpleType.NUMBER:
            return self.value + float(other.value)
        if self._type() == SimpleType.STRING:
            return str(self.value) + str(other.value)

    def __sub__(self, other):
        if self._type() == SimpleType.NULL:
            raise Exception('null value')
        if self._type() == SimpleType.NUMBER:
            return self.value - float(other.value)
        if self._type() == SimpleType.STRING:
            return Exception('subtraction for strings is prohibited')

    def __mul__(self, other):
        if self._type() == SimpleType.NULL:
            raise Exception('null value')
        if self._type() == SimpleType.NUMBER:
            return self.value * float(other.value)
        if self._type() == SimpleType.STRING:
            return Exception('multiplication for strings is prohibited')
        if self._type == SimpleType.BOOL:
            return bool(self.value) and bool(other.value)

    def __floordiv__(self, other):
        if self._type() == SimpleType.NULL:
            raise Exception('null value')
        if self._type() == SimpleType.NUMBER:
            return self.value // float(other.value)
        if self._type() == SimpleType.STRING:
            return Exception('division for strings is prohibited')

    def __truediv__(self, other):
        if self._type() == SimpleType.NULL:
            raise Exception('null value')
        if self._type() == SimpleType.NUMBER:
            return self.value / float(other.value)
        if self._type() == SimpleType.STRING:
            return Exception('division for strings is prohibited')

    def __pow__(self, power, modulo=None):
        if self._type() == SimpleType.NULL:
            raise Exception('null value')
        if self._type() == SimpleType.NUMBER:
            return self.value ** float(power.value)
        if self._type() == SimpleType.STRING:
            return Exception('exponentiation for strings is prohibited')

    def __mod__(self, other):
        if self._type() == SimpleType.NULL:
            raise Exception('null value')
        if self._type() == SimpleType.NUMBER:
            return self.value % float(other.value)
        if self._type() == SimpleType.STRING:
            return Exception('module operation for strings is prohibited')

    def __lt__(self, other):
        if self._type() == SimpleType.NULL:
            raise Exception('null value')
        if self._type() == SimpleType.NUMBER:
            return self.value < float(other.value)
        if self._type() == SimpleType.STRING:
            return Exception('module operation for strings is prohibited')

    def __eq__(self, other):
        if self._type() == SimpleType.NULL:
            raise Exception('null value')
        if self._type() == SimpleType.NUMBER:
            return self.value == float(other.value)
        if self._type() == SimpleType.STRING:
            return str(self.value) == str(other.value)
        if self._type() == SimpleType.BOOL:
            return bool(self.value) == bool(other.value)

    # def __neg__(self):
    #     if self._type() == SimpleType.BOOL:
    #         return not (bool(self.value))
    #     if self._type() == SimpleType.NULL:
    #         raise Exception('null value')

    def __call__(self, *args, **kwargs):
        self.value = self.value


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

    # def add_func(self, name: str):
    #     self.vars[name] = JSValue(None)

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
        func_dict = dict()
        index = -1
        scope = JSScope()
        stack: List[JSValue] = []
        while index < len(program):
            index += 1
            cmd = program[index]
            cmd.index = index

            if cmd.code == CmdCode.PUSH:
                # stack.append(JSValue(cmd.params[0]))

                for i in cmd.params:
                    stack.append(JSValue(i))
                continue

            if cmd.code == CmdCode.POP:
                stack.pop()
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

            if cmd.code == CmdCode.SUB:
                param2 = stack.pop()
                param1 = stack.pop()
                result = param1 - param2
                stack.append(result)
                continue

            if cmd.code == CmdCode.MUL:
                param2 = stack.pop()
                param1 = stack.pop()
                result = param1 * param2
                stack.append(result)
                continue

            if cmd.code == CmdCode.FLOOR_DIV:
                param2 = stack.pop()
                param1 = stack.pop()
                result = param1 // param2
                stack.append(result)
                continue

            if cmd.code == CmdCode.TRUE_DIV:
                param2 = stack.pop()
                param1 = stack.pop()
                result = param1 / param2
                stack.append(result)
                continue

            if cmd.code == CmdCode.POW:
                param2 = stack.pop()
                param1 = stack.pop()
                result = param1 ** param2
                stack.append(result)
                continue

            if cmd.code == CmdCode.MODULE:
                param2 = stack.pop()
                param1 = stack.pop()
                result = param1 % param2
                stack.append(result)
                continue

            if cmd.code == CmdCode.COMPARISON:
                param2 = stack.pop()
                param1 = stack.pop()
                result = param1 < param2
                stack.append(result)
                continue

            if cmd.code == CmdCode.EQUAL:
                param2 = stack.pop()
                param1 = stack.pop()
                result = param1 == param2
                stack.append(result)
                continue

            if cmd.code == CmdCode.NEGATIVE:
                param = stack.pop()
                result = not param
                stack.append(result)
                continue

            if cmd.code == CmdCode.JUMP:
                cmd.index = index

            if cmd.code == CmdCode.DEF_FUNC:
                f = stack.pop()
                func_dict[f] = index
                cmd.label = f.value
                continue
##TODO Сделать ссылку прямком на DEF_FUNC, т.к будем из любой точки ссылаться на объявление и высчитывать кол-во параметров и результат выполения ф-ции
            if cmd.code == CmdCode.CALL:
                jump_address = func_dict.get(cmd.label)
                cmd.index = jump_address
                continue

            if cmd.code == CmdCode.PRINT:
                param = stack.pop()
                print(str(param))
                continue

            if cmd.code == CmdCode.EXIT:
                break

            raise Exception(f'Unknown cmd {cmd.code}')


program = [
    Cmd(CmdCode.PUSH, [5, 6, 7]),
    Cmd(CmdCode.PUSH, ["a"]),
    Cmd(CmdCode.WRITE),
    Cmd(CmdCode.PUSH, [6]),
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

    # Cmd(CmdCode.PUSH, [False]),
    # Cmd(CmdCode.PUSH, ["val"]),
    # Cmd(CmdCode.WRITE),
    # Cmd(CmdCode.PUSH, ["val"]),
    # Cmd(CmdCode.READ),
    # Cmd(CmdCode.NEGATIVE),
    # Cmd(CmdCode.PRINT),


    # Cmd(CmdCode.PUSH, ["Вася"]),
    # Cmd(CmdCode.PUSH, [1]),
    # Cmd(CmdCode.PUSH, ["f"]),
    # Cmd(CmdCode.CALL),
    # Cmd(CmdCode.POP, ["b"]),
    # Cmd(CmdCode.PRINT),

    Cmd(CmdCode.EXIT),
]

    # TODO func f (phrase) { var phrase = "Say " + phrase; alert phrase}  b = f("Hi") (="Say Hi")

    # func f(a, b)
    # push a
    # write
    # push b
    # write
    # push b
    # read
    # push a
    # read
    # push f
    # add_func
    #
    # f(3,5)
    # push 3
    # push 5
    # push f
    # call
    #
    # var b = a;
    # push b
    # add_var
    # push b
    # push a
    # read
    # write

Interpreter.execute(program)
