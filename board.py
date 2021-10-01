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

    # def nestedDiagonalSearch(self, t: list[list[Cell]], p: list[list[int]], w: list[int], l: Linker):
    #     """"The Idea here is to build a tree of possibilities. This function is ran on every cell at the bottom and
    #     then will launch itself on diagonals cases and so one. Recursive search !
    #     t is the table, persistant parameter
    #     p are the diagonals coordinates history, list[ [x, y, d] ]. Append if coherent direction, overwritten if
    #       direction changes
    #     w is the item containing who is winning [playerId, count] """
    #
    #     # If we are in the 4th occurrence, return the winning user
    #     print(p, w)
    #     if w[1] == 4:
    #         return w
    #
    #     # Define the {case} as the value of the target cell. Used many times and rather complex
    #     case = t[self.size[1] - p[-1][1] - 1][p[-1][0]].value
    #     l.data.append(p[-1])
    #     # y: self.size[1] - p[-1][1] - 1 -> As the board variable is starting wit lines at the top, we subtract the
    #     #   actual dimension to make it correct
    #     # x: p[-1][0] -> select the targeted cell's column
    #
    #     if p[-1][1] == 0 or w[0] == 0:  # If we're on the bottom line or last case was null
    #         w = [case, 1]  # Initialise the like with current player
    #
    #     # If we are on an empty case, no winner can be found
    #     if case == 0:
    #         print(f"Empty case at {str(p)}")
    #         return [0, 0]
    #
    #     # Compute next directions
    #     directions = [0]  # X offsets available
    #     if p[-1][1] != 0:  # If we are on top
    #         return [0, 0]  # No winner (if there were a winner, there is a `return w` before
    #
    #     if p[-1][0] != 0:  # If we're not on the left side
    #         directions.append(-1)  # -1 -> left direction
    #
    #     if p[-1][0] != (self.size[0] - 1):  # Same but for right
    #         directions.append(1)
    #         directions.append(2)  # Going horizontal shall we ----->
    #
    #     # Check actual case
    #     if case == w[0]:
    #         w[1] += 1
    #     else:
    #         w = [case, 1]  # We're on the first occurrence of the userid contained in {case}
    #
    #     # Launch more !!
    #     r = []  # Results
    #     print(f"Directions : {str(directions)} at pos : {str(p[-1])}")
    #     loopHash = random.randint(0, 1000000)
    #     for d in directions:
    #         print(f"Looping on loop #{loopHash}")
    #         # pN = [pos for pos in p]  # Do deep copy bc we edit this list
    #         # pN.append([pN[-1][0] + 1, pN[-1][1] + d, d])  # The position at which the next iteration will be launched
    #
    #         if d == p[-1][2]:   # If we're on the same direction as before
    #             wN = w          # Just use last {w}
    #         else:
    #             wN = [0, 1]  # Else, reset the w
    #
    #         # Launch the new iteration and store the result in r
    #         if d == 0:
    #             print(f"Launching new direct vertical worker for level {p[-1][1] + 1}")
    #
    #         r.append(self.nestedDiagonalSearch(t, [*p, [p[-1][0] + d, p[-1][1] + 1, d]], wN, l))
    #         # p[-1][0] + d -> X change
    #         # p[-1][1] + 1 -> One level higher
    #
    #         if d == 2:  # If we do a diagonal, we need to do a horizontal too !
    #             # The == 1 and not != 0 is to prevent infinite loops (left -> right -> left -> right ...)
    #             # + no matter what direction (left to right / right to left), the same information is contained
    #             r.append(self.nestedDiagonalSearch(t, [*p, [p[-1][0] + d, p[-1][1], d]], wN, l))
    #             # p[-1][0] + 1 -> deltaX = 1
    #             # p[-1][1] -> Same line
    #
    #     R = [0, 0]  # THE result (if no found, fall back to default : [0, 0] => Null user, no occurrences
    #     for result in r:
    #         if result[0] != 0:  # If one user is actually found
    #             R = result
    #             break
    #
    #     return R  # Return the winner to the precedent generation

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

        print(f"results ! : {R}")
        print(f"Linker data : {len(l.data)}")

    def state(self) -> int:  # Making the assumption that if there were no winner last move, only one winner
        # Check lines
        # winner = self.detectLineWinner(self.board)
        #
        # # Check columns
        # if winner == 0:  # If still no winner
        #     flipped = []
        #     for x in range(self.size[0]):  # Flip the table to make columns rows
        #         temp = []
        #         for y in range(self.size[1]):
        #             temp.append(self.board[y][x])
        #         flipped.append(temp)
        #
        #     winner = self.detectLineWinner(flipped)
        #
        # # Check diagonals
        # if winner == 0:
        #     pass
        winner = 0

        r = self.search()

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
