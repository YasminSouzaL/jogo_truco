import pygame
import sys
from BaralhoDeTruco import Deck
from truco_regras import TestDeck

# Inicialização do Pygame
pygame.init()

# Tamanhos dos botões
size_button = (180, 50)

# Cores RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (196, 213, 230)
RED = (125, 34, 34)
GREEN = (113, 146, 100)
BLUE = (34, 34, 125)
REDClaro = (255, 107, 102)
VerdeClaro = (153, 255, 102)

# Fonte
pygame.font.init()
main_font = pygame.font.Font("data/font/DS-DIGIB.TTF", 32)
custom_font = pygame.font.Font("data/font/stocky.ttf", 32)
button_font = pygame.font.Font(None, 36)

# Configurações da tela
logo = pygame.image.load("data/imagem/logo.png")
height = 550
width = 750
pygame.display.set_caption('JOGO DE TRUCO!!!!')
pygame.display.set_icon(logo)

clock = pygame.time.Clock()
FPS = 45

# Imagens
background_image = pygame.image.load("data/imagem/background.png")
background_image = pygame.transform.scale(background_image, (width, height))

win_image = pygame.image.load("data/imagem/wallpaper.png")
win_image = pygame.transform.scale(win_image, (width, height))

textbox = pygame.image.load("data/imagem/textbox.png")
textbox = pygame.transform.scale(textbox, (300, 50))

# Caixa de entrada
input_boxes = [pygame.Rect(170, 200, 300, 50)]
active_boxes = [False]
box_colors = [GREY]
texts = ['']
screen = pygame.display.set_mode((width, height))

# Botões
add_button = pygame.Rect(100, 400, 200, 50)
remove_button = pygame.Rect(400, 400, 200, 50)
play_button = pygame.Rect(500, 200, 100, 50)
button_choose = pygame.Rect(500, 200, 100, 50)


def draw_title():
    title_surf = main_font.render("Criar Jogador", True, RED)
    title_rect = title_surf.get_rect(center=(width // 2, 100))
    screen.blit(title_surf, title_rect)


class PlayerCreationScreen:
    def __init__(self):
        self.running = True
        self.player_names = []
        self.input_name = ''

    def draw_text(self, text, font, color, x, y):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        screen.blit(text_surf, text_rect)

    def draw_input(self):
        # Desenha a caixa de entrada de texto
        self.draw_text('Jogador:', main_font, BLACK, 100, 225)
        self.draw_text(self.input_name, main_font, BLACK, 300, 225)
        pygame.draw.rect(screen, box_colors[0], input_boxes[0], 2)

    def draw_buttons(self):
        # Desenha os botões
        pygame.draw.rect(screen, GREEN, add_button)
        pygame.draw.rect(screen, RED, remove_button)
        self.draw_text('Adicionar', button_font, BLACK, add_button.centerx, add_button.centery)
        self.draw_text('Remover', button_font, BLACK, remove_button.centerx, remove_button.centery)

    def draw(self):
        # Desenha a tela
        screen.blit(background_image, (0, 0))
        draw_title()
        self.draw_input()
        self.draw_buttons()
        pygame.display.flip()

    def add_player(self, player_name):
        print(f"Adicionado jogador: {player_name}")
        if player_name and player_name not in self.player_names:
            self.player_names.append(player_name)
            self.input_name = ''

    def remove_player(self):
        if self.player_names:
            self.player_names.pop()
        self.input_name = ''

    def run(self):
        self.running = True
        while self.running:
            screen.fill(WHITE)
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if add_button.collidepoint(event.pos):
                        self.add_player(self.input_name)
                    if remove_button.collidepoint(event.pos):
                        self.remove_player()
                    for i, box in enumerate(input_boxes):
                        if box.collidepoint(event.pos):
                            active_boxes[i] = not active_boxes[i]
                        else:
                            active_boxes[i] = False
                        box_colors[i] = RED if active_boxes[i] else GREY
                if event.type == pygame.KEYDOWN:
                    if active_boxes[0]:
                        if event.key == pygame.K_BACKSPACE:
                            self.input_name = self.input_name[:-1]
                        else:
                            if len(self.input_name) < 10:
                                self.input_name += event.unicode

            if len(self.player_names) >= 2:
                self.running = False


class ScreenCard:
    # Classe que controla a tela de cartas
    def __init__(self):
        self.running = True
        self.deck = Deck()
        self.player_names = []
        self.player_cards = {}
        self.cards_drawn = False
        self.card_width = 80
        self.card_height = 120

    def draw_title(self):
        title_surf = main_font.render("Cartas", True, RED)
        title_rect = title_surf.get_rect(center=(width // 2, 50))
        screen.blit(title_surf, title_rect)

    def checkplayer(self):
        if len(self.player_names) >= 2:
            self.deck.shuffle()
            self.player_cards = self.generate_player_cards()
            print("Cartas geradas para os jogadores:", self.player_cards)
            return True
        else:
            print("Não há jogadores suficientes.")
            return False

    def generate_player_cards(self):
        player_cards = {}
        for player in self.player_names:
            player_cards[player] = self.deck.deal_hand(3)
        TestDeck(player_cards)
        return player_cards

    def draw_text(self, text, font, color, x, y):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        screen.blit(text_surf, text_rect)

    # Desenha as cartas
    def draw_cards(self):
        x = 50
        y = 50
        for player, cards in self.player_cards.items():
            self.draw_text(player, main_font, BLACK, x, y)
            for card in cards:
                pygame.draw.rect(screen, RED, (x, y + 50, self.card_width, self.card_height))
                self.draw_text(str(card), main_font, BLACK, x + self.card_width // 2, y + self.card_height // 2)
                x += 100
            y += 200
            x = 50

    def button_play(self):
        pygame.draw.rect(screen, GREY, play_button)
        self.draw_text('Jogar', main_font, BLACK, 550, 225)

    def draw(self):
        screen.fill(WHITE)
        self.draw_title()
        self.draw_cards()
        self.button_play()
        pygame.display.flip()

    def run(self):
        print("Running ScreenCard")
        if self.checkplayer():
            self.running = True
            while self.running:
                self.draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if play_button.collidepoint(event.pos):
                            self.cards_drawn = True
                            self.running = False
                        if remove_button.collidepoint(event.pos):
                            self.running = False


class Rodadas:
    def __init__(self):
        self.running = True
        self.player_names = []
        self.player_cards = {}
        self.current_round = 1
        self.selected_cards = {}
        self.round_cards = []
        self.card_width = 130
        self.card_height = 140
        self.current_player_index = 0
        self.round_winners = []
        self.winner = None

    def draw_title(self):
        title_surf = main_font.render("Rodadas", True, RED)
        title_rect = title_surf.get_rect(center=(width // 2, 50))
        screen.blit(title_surf, title_rect)

    def draw_text(self, text, font, color, x, y):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        screen.blit(text_surf, text_rect)

    def draw_cards(self, player):
        x = 100
        y = 200
        card_spacing = 40
        for card in self.player_cards[player]:
            pygame.draw.rect(screen, REDClaro, (x, y, self.card_width, self.card_height))
            self.draw_text(str(card), button_font, BLACK, x + self.card_width // 2, y + self.card_height // 2)
            x += self.card_width + card_spacing
        y += 200

    def draw(self):
        screen.blit(background_image, (0, 0))
        self.draw_title()
        pygame.display.flip()
        for player in self.player_names:
            self.draw_cards(player)
        pygame.display.flip()

    def get_selected_card(self, player, card_index):
        if 0 <= card_index < len(self.player_cards[player]):
            selected_card = self.player_cards[player][card_index]
            self.selected_cards[player].append(selected_card)
            del self.player_cards[player][card_index]
            return selected_card
        return None

    def determine_round_winner(self):
        if self.round_cards:
            winner = max(self.round_cards, key=lambda x: x[1])[0]
            self.round_winners.append(winner)
            self.round_cards = []
        else:
            self.round_winners.append(None)

    def run_round(self):
        while self.current_round <= 3:
            for player in self.player_names:
                if not self.player_cards[player]:
                    self.running = False
                    return
                self.draw()
                pygame.display.flip()
                selected = False
                while not selected:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                card_index = (event.pos[0] - 100) // 100
                                selected_card = self.get_selected_card(player, card_index)
                                if selected_card:
                                    self.round_cards.append((player, selected_card))
                                    selected = True
            self.determine_round_winner()
            print(f"Vencedor da rodada {self.current_round}: {self.round_winners[-1]}")
            self.current_round += 1
        self.reset()

    def reset(self):
        self.current_round = 1
        self.selected_cards = {player: [] for player in self.player_names}
        self.round_cards = []

    def determine_game_winner(self):
        victories = {player: self.round_winners.count(player) for player in self.player_names}
        self.winner = max(victories, key=victories.get)

    def run(self):
        print("Running Rodadas")
        self.running = True
        self.run_round()
        self.determine_game_winner()


class Winner:
    def __init__(self):
        self.running = True
        self.winner = None

    def draw_title(self):
        title_surf = main_font.render("Vencedor", True, BLACK)
        title_rect = title_surf.get_rect(center=(width // 2, 50))
        screen.blit(title_surf, title_rect)

    def draw_text(self, text, font, color, x, y):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        screen.blit(text_surf, text_rect)

    def draw_square(self, x, y, width, height, color):
        pygame.draw.rect(screen, color, (x - width // 2, y - height // 2, width, height))

    def draw(self):
        screen.blit(win_image, (0, 0))
        self.draw_title()
        self.draw_square(width // 2, height // 2, 300, 100, VerdeClaro)
        self.draw_text(f"O vencedor foi: {self.winner}", main_font, BLACK, width // 2, height // 2)
        pygame.display.flip()

class Game:
    def __init__(self):
        self.running = True
        self.current_screen = "PlayerCreation"
        self.player_creation = PlayerCreationScreen()
        self.screen_card = ScreenCard()
        self.rodadas = Rodadas()
        self.winner = Winner()

    def switch_screen(self):
        print(f"Switching screen from {self.current_screen}")
        if self.current_screen == "PlayerCreation":
            if len(self.player_creation.player_names) >= 2:
                self.current_screen = "ScreenCard"
                self.screen_card.player_names = self.player_creation.player_names
                print("Switched to ScreenCard")
        elif self.current_screen == "ScreenCard":
            self.current_screen = "Rodadas"
            self.rodadas.player_names = self.screen_card.player_names
            self.rodadas.player_cards = self.screen_card.player_cards
            self.rodadas.selected_cards = {player: [] for player in self.rodadas.player_names}
            print("Switched to Rodadas")
        elif self.current_screen == "Rodadas":
            self.current_screen = "Winner"
            self.winner.winner = self.rodadas.winner
            print("Switched to Winner")
        elif self.current_screen == "Winner":
            self.running = False
            print("Game ended.")

    def run(self):
        while self.running:
            if self.current_screen == "PlayerCreation":
                self.player_creation.run()
                self.switch_screen()
            elif self.current_screen == "ScreenCard":
                self.screen_card.run()
                self.switch_screen()
            elif self.current_screen == "Rodadas":
                self.rodadas.run()
                self.switch_screen()
            elif self.current_screen == "Winner":
                self.winner.draw()
                pygame.time.wait(5000)  # Espera 5 segundos antes de encerrar
                self.running = False

game = Game()
game.run()