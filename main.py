import os
from virtual import ExprEnum, decoder


def main():
    code = [ExprEnum.PUSH, 22, ExprEnum.PUSH, 45, ExprEnum.RAM, ExprEnum.SUB, ExprEnum.POP, ExprEnum.PUSH, 23,
            ExprEnum.PUSH, 9, ExprEnum.PUSH, 5, ExprEnum.RAM, ExprEnum.PRINT, ExprEnum.ADD, ExprEnum.POP,
            ExprEnum.PUSH, 7, ExprEnum.PUSH, 7, ExprEnum.RAM, ExprEnum.ADD, ExprEnum.POP, ExprEnum.POP,
            ExprEnum.PRINT, ExprEnum.EXIT]
    ip = 0
    while ip < len(code):
        # Переменная, которая контролирует работу VM
        decoder(code[ip], code)
        ip += 1


if __name__ == "__main__":
    main()
