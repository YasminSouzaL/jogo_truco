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

        self.font = pygame.font.SysFont('Arial', 50)
        self.text = text
        self.text_surface = None
        self.text_rect = None
        self.render_text()

    def render_text(self):
        BLACK = (0, 0, 0)
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

def menu():
    text1, text2, text3 = "Jogar", "Settings", "Antigo"
    size_button = (200, 50)

    button_game = Buttons(text1, size_button)
    button_setting = Buttons(text2, size_button)
    button_old = Buttons(text3, size_button)

    button_game.rect.center = (width // 2, height // 2 - 50)
    button_setting.rect.center = (width // 2, height // 2 + 25)
    button_old.rect.center = (width // 2, height // 2 + 100)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if button_game.collision_point(pygame.mouse.get_pos()):
                    button_game.up()
                    return "Jogar"
                if button_setting.collision_point(pygame.mouse.get_pos()):
                    button_setting.up()
                    return "Settings"
                if button_old.collision_point(pygame.mouse.get_pos()):
                    button_old.up()
                    return "Antigo"

        button_game.print_display(pygame.mouse.get_pos())
        button_setting.print_display(pygame.mouse.get_pos())
        button_old.print_display(pygame.mouse.get_pos())

        pygame.display.update()

def display_message(message):
    font = pygame.font.Font(None, 74)
    text = font.render(message, True, (255, 0, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)

def quit_game():
    pygame.quit()
    sys.exit()

def main_game_loop():
    background = Background(screen1)
    background.draw_background()

    while True:
        action = menu()
        if action == "Jogar":
            # Iniciar a tela de criação de jogador
            game = Game()
            game.run()
        elif action == "Settings":
            # Ir para as configurações
            tosetup = ScreenSettings()
            tosetup.run()
        elif action == "Antigo":
            display_message("Jogo antigo")


if __name__ == "__main__":
    main_game_loop()
