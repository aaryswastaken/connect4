# Board size is usually 7x6

import random


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
        (q, i) = self.canPlay(col-1)
        if col > self.size[0]:
            return 1

        if q:
            self.board[self.size[1]-i-1][col-1].value = (1 if player_id == 0 else -1)
            return 0

    @staticmethod
    def detectLineWinner(t):
        l = [[l.value for l in c] for c in t]  # For debug purposes
        winner = 0
        for line in t:
            if winner == 0:  # If no winner found
                f = [0, 0]  # player#0 (-> null), 0 times consecutive
                for c in line:
                    if c.value == f[0] and c.value != 0:  # If user is already subscribed and not null player
                        f[1] += 1  # Increment the consecutive
                    else:  # Else, we affect the new player, even if it's the null player
                        f = [c.value, 1]

                    if f[1] == 4:  # Can't be more than 4 if we exit
                        winner = f[0]  # We have a winner
                        break  # Exiting the loop
            else:
                break  # Because of the statement listed at the beginning of this method, only one winner can be decided

        return winner

    def state(self) -> int:  # Making the assumption that if there were no winner last move, only one winner
        # Check lines
        winner = self.detectLineWinner(self.board)

        # Check columns
        if winner == 0:  # If still no winner
            flipped = []
            for x in range(self.size[0]):  # Flip the table to make columns rows
                temp = []
                for y in range(self.size[1]):
                    temp.append(self.board[y][x])
                flipped.append(temp)

            winner = self.detectLineWinner(flipped)

        # Check diagonals
        if winner == 0:
            pass

        return winner

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
