import sys
import pygame
from pygame.locals import *
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
textbox = pygame.transform.scale(textbox, (150, 40))

# Caixa de entrada
input_boxes = [pygame.Rect(170, 200, 300, 50), pygame.Rect(170, 300, 300, 50)]
active_boxes = [False, False]
box_colors = [GREY, GREY]
texts = ['', '']
screen = pygame.display.set_mode((width, height))
# Botões
add_button = pygame.Rect(100, 400, 200, 50)
remove_button = pygame.Rect(400, 400, 200, 50)
play_button = pygame.Rect(500, 200, 100, 50)
button_choose = pygame.Rect(500, 200, 100, 50)

def draw_text(text, rect, color, screen):
    text_surf = main_font.render(text, True, color)
    screen.blit(text_surf, (rect.x, rect.y - 30))

class Background:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.smoothscale(self.image, (width, height))

    def draw_background(self):
        screen.blit(self.image, (0, 0))
        clock.tick(250)
class Buttons(pygame.sprite.Sprite):
    def __init__(self, text, size):
        super().__init__()

        self.image_up = pygame.image.load("data/imagem/button1.png").convert()
        self.image_down = pygame.image.load("data/imagem/button2.png").convert()

        self.image_up = pygame.transform.scale(self.image_up, size)
        self.image_down = pygame.transform.scale(self.image_down, size)

        self.image = self.image_up
        self.rect = self.image.get_rect()

        self.click = False

        self.font = pygame.font.SysFont('padrão', 50)
        self.text = text
        self.text_surface = None
        self.text_rect = None
        self.render_text()

    def render_text(self):
        self.text_surface = self.font.render(self.text, True, BLACK)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.image_up.blit(self.text_surface, self.text_rect)
        self.image_down.blit(self.text_surface, self.text_rect)
        clock.tick(FPS)

    def update(self):
        self.image = self.image_up if not self.click else self.image_down

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        # Centralizar o texto no botão
        self.text_rect.center = self.rect.center
        screen.blit(self.text_surface, self.text_rect)

    def print_display(self, pos):
        self.update()
        self.draw(screen)
        self.collision_point(pos)

    def collision_point(self, pos):
        if self.rect.collidepoint(pos):
            self.click = True
        else:
            self.click = False

    def up(self):
        self.click = False


class PlayerCreationScreen:
    def __init__(self):
        self.running = True
        self.player_names = []
        self.input_name = ''

    def draw_title(self):
        title_surf = main_font.render("Criar Jogador", True, RED)
        title_rect = title_surf.get_rect(center=(width // 2, 100))
        screen.blit(title_surf, title_rect)

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
        self.draw_title()
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
    #Classe que controla a tela de cartas
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
        screen.blit(textbox, (x - 100, y - 30))
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        screen.blit(text_surf, text_rect)


    def draw_texto(self, text, font, color, x, y):
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
                x += 100
            y += 200
            x = 50

    def button_play(self):
        pygame.draw.rect(screen, GREY, play_button)
        self.draw_texto('Jogar', main_font, BLACK, 550, 225)

    def draw(self):
        screen.blit(background_image, (0, 0))
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

class ScreenSettings:
    def __init__(self):
        self.running = True

    def draw_title(self):
        title_surf = main_font.render("Configurações", True, RED)
        title_rect = title_surf.get_rect(center=(width // 2, 200))
        screen.blit(title_surf, title_rect)

    def draw_emoji(self):
        emoji = pygame.image.load("data/imagem/config.png")
        emoji = pygame.transform.scale(emoji, (100, 100))
        screen.blit(emoji, (width // 2, 300))

    def draw(self):
        screen.fill(WHITE)
        self.draw_title()
        self.draw_emoji()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        pygame.quit()
        sys.exit()