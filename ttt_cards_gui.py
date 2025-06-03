# Pygame GUI version of Tic Tac Toe Cards with simple AI
import pygame
import random
from typing import List, Tuple

BOARD_SIZE = 4
CELL_SIZE = 80
CARD_WIDTH = 70
CARD_HEIGHT = 90

def make_positions() -> List[Tuple[int, int]]:
    return [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)]

def make_combos() -> List[List[Tuple[int, int]]]:
    combos: List[List[Tuple[int, int]]] = []
    for r in range(BOARD_SIZE):
        combos.append([(r, c) for c in range(BOARD_SIZE)])
    for c in range(BOARD_SIZE):
        combos.append([(r, c) for r in range(BOARD_SIZE)])
    combos.append([(i, i) for i in range(BOARD_SIZE)])
    combos.append([(i, BOARD_SIZE - 1 - i) for i in range(BOARD_SIZE)])
    return combos

POSITIONS = make_positions()
COMBOS = make_combos()

WIDTH = CELL_SIZE * BOARD_SIZE
HEIGHT = CELL_SIZE * BOARD_SIZE + CARD_HEIGHT + 20

pygame.init()
FONT = pygame.font.SysFont(None, 36)
SMALL = pygame.font.SysFont(None, 28)

CARD_COLORS = {
    'place': (255, 255, 255),
    'remove': (255, 200, 200),
    'swap': (200, 255, 200),
    'block': (200, 200, 255),
    'wild': (255, 255, 180),
}


def draw_text(surf, text, pos, color=(0, 0, 0)):
    img = SMALL.render(text, True, color)
    surf.blit(img, pos)


class TicTacToeCardsGUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic Tac Toe Cards")
        self.board = {pos: ' ' for pos in POSITIONS}
        self.blocked = {}
        self.deck = self._init_deck()
        random.shuffle(self.deck)
        self.hands = {'Player': [], 'AI': []}
        self.symbols = {'Player': 'X', 'AI': 'O'}
        for p in self.hands:
            self._draw(p, 3)
        self.turn = 'Player'
        self.selected_card_index = None
        self.swap_buffer: List[Tuple[int, int]] = []
        self.message = ''

    def _init_deck(self):
        cards = ['place'] * 10 + ['remove'] * 4 + ['swap'] * 4 + ['block'] * 4 + ['wild'] * 2
        return cards

    def _draw(self, player, count=1):
        for _ in range(count):
            if self.deck:
                self.hands[player].append(self.deck.pop())

    def _decrement_blocks(self):
        to_remove = []
        for c in self.blocked:
            self.blocked[c] -= 1
            if self.blocked[c] <= 0:
                to_remove.append(c)
        for c in to_remove:
            del self.blocked[c]

    def available(self, cell: Tuple[int, int]):
        return cell in POSITIONS and self.board[cell] == ' ' and cell not in self.blocked

    def remove_opponent(self, player, cell: Tuple[int, int]):
        opp = 'AI' if player == 'Player' else 'Player'
        if cell in POSITIONS and self.board[cell] == self.symbols[opp] and cell not in self.blocked:
            self.board[cell] = ' '
            return True
        return False

    def swap_cells(self, c1: Tuple[int, int], c2: Tuple[int, int]):
        if all(c in POSITIONS and c not in self.blocked for c in (c1, c2)):
            self.board[c1], self.board[c2] = self.board[c2], self.board[c1]
            return True
        return False

    def block_cell(self, cell: Tuple[int, int]):
        if cell in POSITIONS and cell not in self.blocked:
            self.blocked[cell] = 2
            return True
        return False

    def check_win(self, symbol: str) -> bool:
        for combo in COMBOS:
            if all(self.board[p] == symbol for p in combo):
                return True
        return False

    def board_full(self) -> bool:
        return all(self.board[p] != ' ' for p in POSITIONS)

    def winning_move(self, symbol: str) -> Tuple[int, int] | None:
        need = BOARD_SIZE - 1
        for combo in COMBOS:
            cells = [self.board[p] for p in combo]
            if cells.count(symbol) == need and cells.count(' ') == 1:
                empty = combo[cells.index(' ')]
                if self.available(empty):
                    return empty
        return None

    def score_board(self, symbol: str) -> int:
        opp = self.symbols['Player'] if symbol == self.symbols['AI'] else self.symbols['AI']
        score = 0
        for combo in COMBOS:
            cells = [self.board[p] for p in combo]
            if opp in cells and symbol in cells:
                continue
            count_sym = cells.count(symbol)
            count_opp = cells.count(opp)
            if count_opp == 0:
                score += count_sym * count_sym
            elif count_sym == 0:
                score -= count_opp * count_opp
        return score

    def choose_best_cell(self, symbol: str) -> Tuple[int, int] | None:
        best = None
        best_score = -float('inf')
        for cell in POSITIONS:
            if not self.available(cell):
                continue
            self.board[cell] = symbol
            val = self.score_board(symbol)
            self.board[cell] = ' '
            if val > best_score:
                best_score = val
                best = cell
        return best

    def ai_turn(self):
        self._draw('AI')
        hand = self.hands['AI']
        # try to win
        place_cards = [i for i, c in enumerate(hand) if c == 'place']
        wild_cards = [i for i, c in enumerate(hand) if c == 'wild']
        target = self.winning_move(self.symbols['AI'])
        if target and place_cards:
            card_index = place_cards[0]
            self.use_place('AI', target, card_index)
            return
        if target and wild_cards:
            card_index = wild_cards[0]
            self.use_place('AI', target, card_index)
            return
        # block player win
        target = self.winning_move(self.symbols['Player'])
        if target and place_cards:
            card_index = place_cards[0]
            self.use_place('AI', target, card_index)
            return
        if target and wild_cards:
            card_index = wild_cards[0]
            self.use_place('AI', target, card_index)
            return
        # choose best scoring move
        if place_cards or wild_cards:
            card_index = place_cards[0] if place_cards else wild_cards[0]
            cell = self.choose_best_cell(self.symbols['AI'])
            if cell is None:
                cell = random.choice([c for c in POSITIONS if self.available(c)])
            self.use_place('AI', cell, card_index)
            return
        # try remove if available
        rem_cards = [i for i, c in enumerate(hand) if c == 'remove']
        if rem_cards:
            opp_cells = [p for p in POSITIONS if self.board[p] == self.symbols['Player']]
            if opp_cells:
                cell = random.choice(opp_cells)
                self.hands['AI'].pop(rem_cards[0])
                self.remove_opponent('AI', cell)
                self.message = f"AI removes {cell}"
                return
        # nothing useful
        self.message = "AI skips"

    def use_place(self, player, cell, index):
        self.hands[player].pop(index)
        self.animate_piece(player, cell)
        self.board[cell] = self.symbols[player]
        self.message = f"{player} placed on {cell}"

    def animate_piece(self, player: str, cell: Tuple[int, int]):
        r, c = cell
        dest = (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2)
        start_y = -CELL_SIZE
        for step in range(15):
            self.draw_board()
            pos_y = int(start_y + (dest[1] - start_y) * (step / 14))
            text = FONT.render(self.symbols[player], True, (0, 0, 0))
            rect = text.get_rect(center=(dest[0], pos_y))
            self.screen.blit(text, rect)
            pygame.display.flip()
            pygame.time.delay(30)

    def draw_board(self):
        self.screen.fill((255, 255, 255))
        # grid
        for x in range(1, BOARD_SIZE):
            pygame.draw.line(self.screen, (0, 0, 0), (x*CELL_SIZE, 0), (x*CELL_SIZE, CELL_SIZE*BOARD_SIZE), 2)
        for y in range(1, BOARD_SIZE):
            pygame.draw.line(self.screen, (0, 0, 0), (0, y*CELL_SIZE), (CELL_SIZE*BOARD_SIZE, y*CELL_SIZE), 2)
        # cells
        for pos in POSITIONS:
            r, c = pos
            x = c * CELL_SIZE
            y = r * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            val = '#'
            if pos not in self.blocked:
                val = self.board[pos]
            text = FONT.render(val if val != ' ' else '', True, (0, 0, 0))
            t_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, t_rect)
        # hand
        hand = self.hands['Player']
        for i, card in enumerate(hand):
            rect = pygame.Rect(i*CARD_WIDTH+5, CELL_SIZE*BOARD_SIZE+10, CARD_WIDTH-10, CARD_HEIGHT-10)
            color = CARD_COLORS.get(card, (200, 200, 200))
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
            if i == self.selected_card_index:
                pygame.draw.rect(self.screen, (255, 0, 0), rect, 3)
            draw_text(self.screen, card, (rect.x+5, rect.y+5))
        if self.message:
            draw_text(self.screen, self.message, (10, HEIGHT - CARD_HEIGHT//2))
        pygame.display.flip()

    def cell_from_pos(self, pos: Tuple[int, int]):
        x, y = pos
        if x < 0 or x >= CELL_SIZE*BOARD_SIZE or y < 0 or y >= CELL_SIZE*BOARD_SIZE:
            return None
        col = x // CELL_SIZE
        row = y // CELL_SIZE
        idx = row * BOARD_SIZE + col
        if idx < len(POSITIONS):
            return POSITIONS[idx]
        return None

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(30)
            self._decrement_blocks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif self.turn == 'Player':
                    self.handle_player_event(event)
            if self.turn == 'AI' and running:
                pygame.time.delay(500)
                self.ai_turn()
                if self.check_win(self.symbols['AI']):
                    self.message = 'AI wins!'
                    self.turn = None
                elif self.board_full():
                    self.message = "It's a draw"
                    self.turn = None
                else:
                    self.turn = 'Player'
            self.draw_board()
        pygame.quit()

    def handle_player_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            # select card
            if my >= CELL_SIZE*BOARD_SIZE:
                index = mx // CARD_WIDTH
                if index < len(self.hands['Player']):
                    self.selected_card_index = index
            else:
                if self.selected_card_index is None:
                    return
                card = self.hands['Player'][self.selected_card_index]
                cell = self.cell_from_pos((mx, my))
                if not cell:
                    return
                if card == 'place':
                    if self.available(cell):
                        self.use_place('Player', cell, self.selected_card_index)
                        self.end_player_turn()
                elif card == 'remove':
                    if self.remove_opponent('Player', cell):
                        self.hands['Player'].pop(self.selected_card_index)
                        self.message = f"Player removed {cell}"
                        self.end_player_turn()
                elif card == 'block':
                    if self.block_cell(cell):
                        self.hands['Player'].pop(self.selected_card_index)
                        self.message = f"Player blocked {cell}"
                        self.end_player_turn()
                elif card == 'swap':
                    if cell not in self.swap_buffer:
                        self.swap_buffer.append(cell)
                    if len(self.swap_buffer) == 2:
                        if self.swap_cells(self.swap_buffer[0], self.swap_buffer[1]):
                            self.hands['Player'].pop(self.selected_card_index)
                            self.message = f"Player swapped {self.swap_buffer[0]} and {self.swap_buffer[1]}"
                            self.end_player_turn()
                        self.swap_buffer = []
                elif card == 'wild':
                    # default to place
                    if self.available(cell):
                        self.use_place('Player', cell, self.selected_card_index)
                        self.end_player_turn()
        elif event.type == pygame.KEYDOWN and self.selected_card_index is not None:
            card = self.hands['Player'][self.selected_card_index]
            if card == 'wild':
                if event.key == pygame.K_r:
                    self.hands['Player'][self.selected_card_index] = 'remove'
                elif event.key == pygame.K_s:
                    self.hands['Player'][self.selected_card_index] = 'swap'
                elif event.key == pygame.K_b:
                    self.hands['Player'][self.selected_card_index] = 'block'

    def end_player_turn(self):
        if self.check_win(self.symbols['Player']):
            self.message = 'Player wins!'
            self.turn = None
        elif self.board_full():
            self.message = "It's a draw"
            self.turn = None
        else:
            self._draw('Player')
            self.turn = 'AI'
        self.selected_card_index = None


if __name__ == '__main__':
    game = TicTacToeCardsGUI()
    game.run()
