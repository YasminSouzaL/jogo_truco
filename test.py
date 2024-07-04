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

textbox = pygame.image.load("data/imagem/textbox.png")
textbox = pygame.transform.scale(textbox, (300, 50))

# Caixa de entrada
input_boxes = [pygame.Rect(170, 200, 300, 50), pygame.Rect(170, 300, 300, 50)]
active_boxes = [False, False]
box_colors = [GREY, GREY]
texts = ['', '']
screen = pygame.display.set_mode((width, height))
# Botões
add_button = pygame.Rect(100, 400, 200, 50)
remove_button = pygame.Rect(400, 400, 200, 50)


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
        screen.blit(textbox, (x - 50, y - 25))
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        screen.blit(text_surf, text_rect)

    #Desenha as cartas
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

    def draw(self):
        screen.blit(background_image, (0, 0))
        self.draw_cards()
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
                        if add_button.collidepoint(event.pos):
                            self.cards_drawn = True
                            self.running = False
                        if remove_button.collidepoint(event.pos):
                            self.running = False

class Rodadas:
    '''
    Classe que controla as rodadas do jogo
    Onde o jogador escolhe a carta que deseja jogar
    depois o outro jogador escolhe a carta que deseja jogar
    e por fim a carta vencedora é escolhida
    '''
    def __init__(self):
        self.running = True
        self.deck = Deck()
        self.player_names = []
        self.player_cards = {}
        self.card_width = 80
        self.card_height = 120

    def test(self):
        print("Entrei na classe Rodadas")

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

    # mostra as cartas do 1 jogador e pedir para ele escolher uma carta e depois o outro jogador escolher uma carta
    def choose_card(self):
        x = 50
        y = 50
        for player, cards in self.player_cards.items():
            self.draw_text(player, main_font, BLACK, x, y)
            for card in cards:
                pygame.draw.rect(screen, RED, (x, y + 50, self.card_width, self.card_height))
                x += 100
            y += 200
            x = 50

    def button(self):
        pygame.draw.rect(screen, GREY, (50, 50, 100, 50))
        self.draw_text('Escolher', main_font, BLACK, 100, 75)

    def draw(self):
        screen.fill(WHITE)
        self.test()
        self.choose_card()
        self.test()
        self.button()
        pygame.display.flip()

    def run(self):
        print("Running Rodadas")
        self.running = True
        while self.running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if add_button.collidepoint(event.pos):
                        self.running = False
                    if remove_button.collidepoint(event.pos):
                        self.running = False
class Game:
    def __init__(self):
        self.running = True
        self.current_screen = "PlayerCreation"
        self.player_creation = PlayerCreationScreen()
        self.screen_card = ScreenCard()
        self.rodadas = Rodadas()

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
            print("Switched to Rodadas")
        elif self.current_screen == "Rodadas":
            self.running = False
            print("Game ended")

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

if __name__ == "__main__":
    game = Game()
    game.run()