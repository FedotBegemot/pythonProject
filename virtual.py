# MAXMEM = 5
# Массив памяти, который состоит из элементов типа int
import enum

stack = []
# Указатель на положение данных в стеке, сейчас стек не инициализирован
data1 = 5
# stack.pop(data1)

# stack.empty()


class ExprEnum(enum.Enum):
    PUSH = 0,
    # Получить значение со стека.Берется верхушка стека
    POP = 0x00d00205,
    # Сложить два верхних значения стека
    ADD = 0x00d00202,
    # Вычесть два верхних значения стека
    SUB = 0x00d00206,
    # Поделить два значения
    DIV = 0x00d00203,
    # Перемножить два значения. Во всех четырех операциях результат кладется на стек
    MUL = 0x00d00204,
    # Ввести данные
    ENTER = 0x00d00211,
    # Сверка данных с шаблоном
    TEST = 0x00d00209,
    # Вывести верхушку стека
    PRINT = 0x00d00210,
    # Вывести все данные, которые находятся в нашей памяти
    RAM = 0x00d00208,
    # Завершить работy виртуальной машины
    EXIT = 0x00d00207


# Указатель на инструкцию (мнемонику)
ip = 0


def decoder(instr, code):
    if instr == 0:
        code.push(stack[1])
    if instr == 0x00d00202:
        # Берем два верхних значения стека
        a = stack.pop()
        b = stack.pop()
        # Складываем их и кладем результат на стек
        stack.push(a + b)
        # Выводим сообщение
        print("ADD->")
    if instr == 0x00d00206:
        # Берем два верхних значения стека
        a = stack.pop()
        b = stack.pop()
        # Вычитаем их и кладем результат на стек
        stack.push(a - b)
        # Выводим сообщение
        print("SUB->")
    if instr == 0x00d00203:
        # Берем два верхних значения стека
        a = stack.pop()
        b = stack.pop()
        # Делим их и кладем результат на стек
        stack.push(a / b)
        # Выводим сообщение
        print("DIV->")
    if instr == 0x00d00204:
        # Берем два верхних значения стека
        a = stack.pop()
        b = stack.pop()
        # Перемножаем их и кладем результат на стек
        stack.push(a * b)
        # Выводим сообщение
        print("MUL->")
    if instr == 0x00d00208:
        # Это простой цикл вывода всех значений массива
        # x = stack.size()
        for element in stack[::-1]:
            print("RAM[%u]: %u\n", stack.peek())
    # if instr == 0x00d00209:
# stack.peek() == 0x31337 ? print("Good Pass!\n") : print("Bad Pass!\n")
    if instr == 0x00d00210:
        print("PRINT Stack[%u]: %u\n", stack.peek())
    if instr == 0x00d00211:
        print("ENTER Password: ")
        # scanf_s("%i", & stack[sp]);
    if instr == 0x00d00207:
        # Установка глобальной переменной в FALSE, чтобы прервать работу VM
        VM = False
        print("Exit VM\n")


