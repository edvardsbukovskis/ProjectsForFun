import random

# Board representation
POSITIONS = [
    'TopLeft', 'TopMid', 'TopRight',
    'MidLeft', 'MidMid', 'MidRight',
    'BotLeft', 'BotMid', 'BotRight'
]


class TicTacToeCards:
    def __init__(self):
        self.board = {pos: ' ' for pos in POSITIONS}
        self.blocked = {}
        self.deck = self._init_deck()
        random.shuffle(self.deck)
        self.hands = {'P1': [], 'P2': []}
        self.symbols = {'P1': 'X', 'P2': 'O'}
        for player in self.hands:
            self._draw(player, 3)
        self.turn = 'P1'

    def _init_deck(self):
        # create a small deck with action cards
        cards = ['place'] * 10 + ['remove'] * 4 + ['swap'] * 4 + ['block'] * 4 + ['wild'] * 2
        return cards

    def _draw(self, player, count=1):
        for _ in range(count):
            if self.deck:
                card = self.deck.pop()
                self.hands[player].append(card)

    def _decrement_blocks(self):
        to_remove = []
        for cell in self.blocked:
            self.blocked[cell] -= 1
            if self.blocked[cell] <= 0:
                to_remove.append(cell)
        for cell in to_remove:
            del self.blocked[cell]

    def print_board(self):
        b = self.board
        def val(p):
            if p in self.blocked:
                return '#'
            return b[p]
        print(f"{val('TopLeft')}|{val('TopMid')}|{val('TopRight')}")
        print('-+-+-')
        print(f"{val('MidLeft')}|{val('MidMid')}|{val('MidRight')}")
        print('-+-+-')
        print(f"{val('BotLeft')}|{val('BotMid')}|{val('BotRight')}")

    def check_win(self, symbol):
        combos = [
            ('TopLeft', 'TopMid', 'TopRight'),
            ('MidLeft', 'MidMid', 'MidRight'),
            ('BotLeft', 'BotMid', 'BotRight'),
            ('TopLeft', 'MidLeft', 'BotLeft'),
            ('TopMid', 'MidMid', 'BotMid'),
            ('TopRight', 'MidRight', 'BotRight'),
            ('TopLeft', 'MidMid', 'BotRight'),
            ('TopRight', 'MidMid', 'BotLeft'),
        ]
        for combo in combos:
            if all(self.board[pos] == symbol for pos in combo):
                return True
        return False

    def board_full(self):
        return all(self.board[p] != ' ' for p in POSITIONS)

    def available(self, cell):
        return cell in POSITIONS and self.board[cell] == ' ' and cell not in self.blocked

    def remove_opponent(self, player, cell):
        opp = 'P2' if player == 'P1' else 'P1'
        if cell in POSITIONS and self.board[cell] == self.symbols[opp] and cell not in self.blocked:
            self.board[cell] = ' '
            return True
        return False

    def swap_cells(self, cell1, cell2):
        if all(c in POSITIONS and c not in self.blocked for c in [cell1, cell2]):
            self.board[cell1], self.board[cell2] = self.board[cell2], self.board[cell1]
            return True
        return False

    def block_cell(self, cell):
        if cell in POSITIONS and cell not in self.blocked:
            self.blocked[cell] = 2
            return True
        return False

    def play(self):
        print("Welcome to Tic Tac Toe Cards!")
        while True:
            self._decrement_blocks()
            player = self.turn
            symbol = self.symbols[player]
            self._draw(player)
            print(f"\n{player}'s turn ({symbol})")
            self.print_board()
            print(f"Hand: {self.hands[player]}")
            card = None
            while card not in self.hands[player]:
                card = input("Choose a card to play: ")
            self.hands[player].remove(card)
            if card == 'place' or (card == 'wild' and input("Use as place? (y/n): ") == 'y'):
                cell = None
                while not (cell and self.available(cell)):
                    cell = input("Choose empty cell: ")
                self.board[cell] = symbol
            elif card == 'remove' or (card == 'wild' and input("Use as remove? (y/n): ") == 'y'):
                cell = None
                while not (cell and self.remove_opponent(player, cell)):
                    cell = input("Choose opponent cell to remove: ")
            elif card == 'swap' or (card == 'wild' and input("Use as swap? (y/n): ") == 'y'):
                while True:
                    c1 = input("Cell 1: ")
                    c2 = input("Cell 2: ")
                    if self.swap_cells(c1, c2):
                        break
                    print("Invalid cells")
            elif card == 'block' or (card == 'wild' and input("Use as block? (y/n): ") == 'y'):
                cell = None
                while not (cell and self.block_cell(cell)):
                    cell = input("Choose cell to block: ")
            else:
                print("Card wasted!")

            if self.check_win(symbol):
                self.print_board()
                print(f"{player} wins!")
                break
            if self.board_full():
                self.print_board()
                print("It's a draw!")
                break

            self.turn = 'P2' if self.turn == 'P1' else 'P1'


if __name__ == '__main__':
    game = TicTacToeCards()
    game.play()
