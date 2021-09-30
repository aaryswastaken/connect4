import os


class Pile:
    def __init__(self):
        self.pile = []

    def p(self, x: any, end="\n") -> None:
        self.pile += str(x) + end

    def clear(self):
        self.pile = []

    def __str__(self):
        return "".join([str(e) for e in self.pile])


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def pressEnterToContinue(start="\n\n") -> None:
    input(start + 'Press enter to continue ...')
