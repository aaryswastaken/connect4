# Board size is usually 7x6
import os
import random

class Linker:
    def __init__(self):
        self.data = []


class Cell:
    def __init__(self, board):
        self.board = board

        self.value = 0

    def __str__(self):
        if self.value == -1:
            return self.board.chars[0]
        elif self.value == 1:
            return self.board.chars[1]
        else:
            return " "


class Board:
    def __init__(self, size=None):
        if size is None:
            size = [7, 6]
        self.size = size

        self.board = [[Cell(self) for n in range(size[0])] for m in range(size[1])]
        self.chars = ["X", "O"]
        self.settings = {
            "header": 1
        }

    def configure(self, c: dict) -> dict:
        self.settings = {**self.settings, **c}
        return self.settings

    def play(self, col, player_id):
        (q, i) = self.canPlay(col - 1)
        if col > self.size[0]:
            return 1

        if q:
            self.board[self.size[1] - i - 1][col - 1].value = (1 if player_id == 0 else -1)
            return 0

    def nestedDiagonalSearch(self, t: list[list[Cell]], p: list[list[int]], w: list[int], l: Linker):
        """
        This function is designed to recursively find every occurrences of winning player on the board t
        :param t: Board
        :param p: Position history [x, y, d] (in coords 0 -> size-1)
        :param w: Winning result [id, count]
        :param l: linker
        :return: Winning informations
        """

        currentPos = p[-1]
        case = t[self.size[1] - currentPos[1] - 1][currentPos[0]].value

        if case == w[0] and w[0] != 0:
            w[1] += 1
            print(f"Check on {w}")

        if w[1] == 4 or (w[1] == 3 and currentPos[2] == 0 and currentPos[0] == 0):
            # Don't know why but only has 3 for the first column on horizontal so it's a crappy hack but it works
            print(f"FOUND !! {w}")
            return w

        if currentPos[1] >= (self.size[1] - 1):  # If we're at the top
            return [0, 0]

        # Compute the w value for the function according to the direction it takes
        def computeW(direction):
            if currentPos[2] == direction:
                return w
            else:
                return [case, 1]

        S = []

        if currentPos[0] < self.size[0] - 1:  # Can go to the right
            # Go to the horizontal/right
            S.append(self.nestedDiagonalSearch(t, [*p, [currentPos[0] + 1, currentPos[1], 2]], computeW(2), l))

        if currentPos[1] < self.size[1] - 1:  # Is not on top
            if case != 0:  # If the actual case is empty, there is no cell containing any value on top
                # Go to the top
                S.append(self.nestedDiagonalSearch(t, [*p, [currentPos[0], currentPos[1] + 1, 0]], computeW(0), l))

            if currentPos[0] > 0:  # Can go to the left
                # Go to the diagonal/left
                S.append(
                    self.nestedDiagonalSearch(t, [*p, [currentPos[0] - 1, currentPos[1] + 1, -1]], computeW(-1), l))

            if currentPos[0] < self.size[0] - 1:  # Can go to the right
                # Go to the diagonal/right
                S.append(self.nestedDiagonalSearch(t, [*p, [currentPos[0] + 1, currentPos[1] + 1, 1]], computeW(1), l))

        s = [0, 0]
        for result in S:
            if result[0] != 0:
                s = result
                print(f"Checking with w[1] = {w[1]}, w[0] = {w[0]}")

        l.data.append(s)

        return s

    def search(self):
        R = [0, 0]  # Same as Board.nestedDiagonalSearch()

        l = Linker()

        for col in range(self.size[0]):
            print(f"Launching on col {str(col)}")
            r = self.nestedDiagonalSearch(self.board, p=[[col, 0, 0]], w=[0, 0], l=l)
            if r[0] != 0:
                R = r
                break

        return R[0]

    def state(self) -> int:  # Making the assumption that if there were no winner last move, only one winner
        r = self.search()

        return r

    def __str__(self, delimiter="\n") -> str:
        output = ""

        if self.settings["header"] == 1:
            output = f"  {' '.join([str(i) for i in range(1, self.size[0] + 1)])} \n"

        for line in self.board:
            output += f'| {" ".join([str(cell) for cell in line])} |\n'
        output += "-" * (self.size[0] * 2 + 3)

        return output

    def canPlay(self, col: int) -> tuple[bool, int]:
        col = [x[col] for x in self.board]
        colF = [int(x.value != 0) for x in col]

        return not (sum(colF) == self.size[1]), sum(colF)


class Log:
    def __init__(self):
        self.log = []

    def append(self, message):
        self.log.append(message)

    def format(self, x, spaces=3):
        maxLen = max([len(l) for l in x.split("\n")])
        x = [s + (" " * (maxLen - len(s) + spaces)) + "| " for s in x.split("\n")]  # Add the spaces, the bar
        iL = [l for l in self.log]  # Deep copy

        # Reverse them all
        iL.reverse()
        x.reverse()

        for i, l in enumerate(iL[:(len(x) - 2)]):
            x[i + 1] += l

        x.reverse()

        return "\n".join(x)


if __name__ == "__main__":
    b = Board()
    log = Log()
    print(log.format(str(b)))
