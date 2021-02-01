import pygame
import sys


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Led:
    def __init__(self, dir_desligado, dir_ligado):
        self.img_desligado = pygame.image.load(dir_desligado)
        self.img_ligado = pygame.image.load(dir_ligado)
        self.img_atual = self.img_desligado
        self.estado_atual = False

    def desligar(self):
        self.estado_atual = False
        self.img_atual = self.img_desligado

    def ligar(self):
        self.estado_atual = True
        self.img_atual = self.img_ligado

    def get_estado(self):
        return self.estado_atual


class Game:
    def __init__(self, tela):
        self.screen = tela
        # Título central do jogo
        self.font_titulo = pygame.font.Font("fonts/freesansbold.ttf", 32)
        self.text_titulo = self.font_titulo.render("pense BEM rápido",
                                                   True,
                                                   (255, 255, 255))
        # Centralizar em X
        self.text_rect_titulo = self.text_titulo.get_rect(center=(SCREEN_WIDTH / 2, 100))

        # Inicializar os LEDs
        self.led_verde = Led("imagens/desligado.png", "imagens/verde_ligado.png")
        self.led_vermelho = Led("imagens/desligado.png", "imagens/vermelho_ligado.png")
        self.led_amarelo = Led("imagens/desligado.png", "imagens/amarelo_ligado.png")
        self.led_azul = Led("imagens/desligado.png", "imagens/azul_ligado.png")

    def desenhar_leds(self):
        self.screen.blit(self.led_verde.img_atual, (3*64, 200))
        self.screen.blit(self.led_vermelho.img_atual, (5*64, 200))
        self.screen.blit(self.led_amarelo.img_atual, (7*64, 200))
        self.screen.blit(self.led_azul.img_atual, (9*64, 200))

    def desenhar_textos(self):
        self.screen.blit(self.text_titulo, self.text_rect_titulo)


if __name__ == "__main__":
    # Inicialização do pygame
    pygame.init()
    # Cria a janela do jogo
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Inicializar novo jogo
    game = Game(screen)
    # Título da janela
    pygame.display.set_caption("pense BEM rápido")
    # Icone
    icon = pygame.image.load("imagens/icon.png")
    pygame.display.set_icon(icon)
    # Tempos
    tempo_atual = 0
    cronometro_ligar = 0  # timer para contar até acender
    tempo_ligar = 2  # em segundos

    # Game Loop
    while True:
        screen.fill((10, 10, 10))  # Essa linha tem que ser a primeira

        # Desenhar as LEDs
        game.desenhar_leds()
        game.desenhar_textos()

        # Acende a Luz
        tempo_atual = pygame.time.get_ticks()/1000  # transforma em segundos
        if tempo_atual - cronometro_ligar >= tempo_ligar:
            cronometro_ligar = tempo_atual
            if game.led_verde.get_estado():
                game.led_verde.desligar()
            else:
                game.led_verde.ligar()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Pressionou o botão
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.led_verde.ligar()
                    game.led_vermelho.ligar()
                    game.led_amarelo.ligar()
                    game.led_azul.ligar()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    game.led_verde.desligar()
                    game.led_vermelho.desligar()
                    game.led_amarelo.desligar()
                    game.led_azul.desligar()

        pygame.display.update()
