import pygame
from pygame.locals import *
import sys

from Tela_stilo import *

pygame.init()

# Imagens
screen1_path = "data/imagem/background.png"
screen2_path = "data/imagem/background2.png"

# Tamanho da tela
height = 550
width = 750

# Configuração da tela
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('JOGO DE TRUCO!!!!')
logo = pygame.image.load("data/imagem/logo.png")
pygame.display.set_icon(logo)

# Carregar imagens
screen1 = pygame.image.load(screen1_path)
screen1 = pygame.transform.scale(screen1, (width, height))

def draw_text(text, rect, color, screen):
    main_font = pygame.font.SysFont('Arial', 30)
    text_surf = main_font.render(text, True, color)
    screen.blit(text_surf, (rect.x, rect.y - 30))

class GameContract(ABC):
    '''
        Classe abstrata que define os métodos que
        devem ser implementados pelas classes que a herdam.
    '''
    @property
    @abstractmethod
    def draw_title(self):
        pass

    @abstractmethod
    def draw_input(self):
        pass

    @abstractmethod
    def draw_buttons(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def switch_screen(self):
        pass

class GameState:
    def __init__(self):
        self.current_screen = "PlayerCreation"
        self.running = True

class GameMethods(GameContract):
    def __init__(self):
        pygame.init()
        self.state = GameState()
        self.setup_constants()
        self.setup_display()
        self.setup_fonts()
        self.setup_images()
        self.setup_buttons()
        self.player_creation_screen = self.PlayerCreationScreen(self)
        self.screen_card = self.ScreenCard(self)
        self.rodadas = self.Rodadas(self)
        self.winner = self.Winner(self)

    def setup_constants(self):
        self.size_button = (180, 50)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREY = (196, 213, 230)
        self.RED = (125, 34, 34)
        self.GREEN = (7, 117, 82)
        self.BLUE = (0, 0, 128)
        self.REDClaro = (255, 107, 102)
        self.VerdeClaro = (153, 255, 102)

    def setup_display(self):
        self.logo = pygame.image.load("data/imagem/logo.png")
        self.height = 550
        self.width = 750
        pygame.display.set_caption('JOGO DE TRUCO!!!!')
        pygame.display.set_icon(self.logo)
        self.clock = pygame.time.Clock()
        self.FPS = 45
        self.screen = pygame.display.set_mode((self.width, self.height))

    def setup_fonts(self):
        pygame.font.init()
        self.main_font = pygame.font.Font("data/font/DS-DIGIB.TTF", 32)
        self.custom_font = pygame.font.Font("data/font/stocky.ttf", 32)
        self.button_font = pygame.font.Font(None, 36)

    def setup_images(self):
        self.background_image = pygame.image.load("data/imagem/background.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        self.win_image = pygame.image.load("data/imagem/wallpaper.png")
        self.win_image = pygame.transform.scale(self.win_image, (self.width, self.height))
        self.textbox = pygame.image.load("data/imagem/textbox.png")
        self.textbox = pygame.transform.scale(self.textbox, (300, 50))
        self.telafundo = pygame.image.load("data/imagem/tela_fundo.png")
        self.telafundo = pygame.transform.scale(self.telafundo, (self.width, self.height))

    def setup_buttons(self):
        self.input_boxes = [pygame.Rect(170, 200, 300, 50)]
        self.active_boxes = [False]
        self.box_colors = [self.GREY]
        self.texts = ['']
        self.add_button = pygame.Rect(100, 400, 200, 50)
        self.remove_button = pygame.Rect(400, 400, 200, 50)
        self.play_button = pygame.Rect(500, 200, 100, 50)
        self.button_choose = pygame.Rect(500, 200, 100, 50)

    def draw_text(self, text, font, color, x, y):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        self.screen.blit(text_surf, text_rect)

    def draw_title(self):
        pass

    def draw_input(self):
        pass

    def draw_buttons(self):
        pass

    def draw(self):
        pass

    def run(self):
        while self.state.running:
            if self.state.current_screen == "PlayerCreation":
                self.player_creation_screen.run()
            elif self.state.current_screen == "ScreenCard":
                self.screen_card.run()
            elif self.state.current_screen == "Rodadas":
                self.rodadas.run()
            elif self.state.current_screen == "Winner":
                self.winner.draw()
                pygame.time.wait(5000)
                self.state.running = False

    def switch_screen(self):
        if self.state.current_screen == "PlayerCreation":
            if len(self.player_creation_screen.player_names) >= 2:
                self.state.current_screen = "ScreenCard"
                self.screen_card.player_names = self.player_creation_screen.player_names
        elif self.state.current_screen == "ScreenCard":
            self.state.current_screen = "Rodadas"
            self.rodadas.player_names = self.screen_card.player_names
            self.rodadas.player_cards = self.screen_card.player_cards
            self.rodadas.selected_cards = {player: [] for player in self.rodadas.player_names}
        elif self.state.current_screen == "Rodadas":
            self.state.current_screen = "Winner"
            self.winner.winner = self.rodadas.winner
        elif self.state.current_screen == "Winner":
            self.state.running = False

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
        self.font = pygame.font.SysFont('Arial', 45)
        self.text = text
        self.text_surface = None
        self.text_rect = None
        self.render_text()

    def render_text(self):
        self.text_surface = self.font.render(self.text, True, BLACK)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.image_up.blit(self.text_surface, self.text_rect)
        self.image_down.blit(self.text_surface, self.text_rect)

    def collision_point(self, point):
        return self.rect.collidepoint(point)

    def up(self):
        pass

    def print_display(self, mouse_pos):
        screen.blit(self.image, self.rect.topleft)


class Background:
    def __init__(self, image_surface):
        self.image = image_surface

    def draw_background(self):
        screen.blit(self.image, (0, 0))
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
                pygame.time.wait(5000)
                self.running = False
def menu():
    text1, text2, text3 = "Jogar", "Settings", "Regras"
    size_button = (200, 50)
    button_game = Buttons(text1, size_button)
    button_old = Buttons(text3, size_button)

    button_game.rect.center = (width // 2, height // 2)
    button_old.rect.center = (width // 2, height // 2 + 70)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if button_game.collision_point(pygame.mouse.get_pos()):
                    button_game.up()
                    return "Jogar"
                if button_old.collision_point(pygame.mouse.get_pos()):
                    button_old.up()
                    return "Regras"

        button_game.print_display(pygame.mouse.get_pos())
        button_old.print_display(pygame.mouse.get_pos())

        pygame.display.update()
        clock.tick(60)


clock = pygame.time.Clock()
def quit_game():
    pygame.quit()
    sys.exit()

def main_game_loop():
    while True:
        background = Background(screen1)
        background.draw_background()
        action = menu()

        if action == "Jogar":
            # Iniciar a tela de criação de jogador
            game = Game()
            game.run()
        elif action == "Regras":
            # Ir para as regras
            tosetup = ScreenRules()
            tosetup.run()


if __name__ == "__main__":
    main_game_loop()
