import board
import utils


b = board.Board()

# CREATE DEFAULT BOARD
# such as :
#
# X X X
# O O O

b.board[5][0].value = 1
b.board[4][0].value = 1
b.board[3][0].value = 1

b.board[5][1].value = -1
b.board[4][1].value = -1
b.board[3][1].value = -1

log = board.Log()

pile = utils.Pile()

player = 0
max_row = b.size[0]

while True:
    col = -1
    while True:
        utils.clear()
        pile.clear()
        pile.p(" ***** CONNECT4 ***** \n")
        pile.p(log.format(str(b)), end="\n\n")

        print(pile)
        ip = input(f"\nplayer{player}$ ")
        try:
            c = int(ip)
            if c <= 0:
                int("a")  # throws an error
            elif c > max_row:
                int("a")
            else:
                col = c
                break
        except ValueError as e:
            print("\nYou've entered an illegal input")
            utils.pressEnterToContinue(start="\n")
            utils.clear()

    r = b.play(col, player)
    if not r:
        log.append(f'player{player} played {col}')

    w = b.state()
    if w != 0:
        log.append(f'[!] player{int(w!=1)} ({b.chars[w==1]}) won !')
        break

    player = int(not player)

utils.clear()
pile.clear()
print("Game finished with board : ")
print(log.format(str(b)), end="\n\n")
utils.pressEnterToContinue()