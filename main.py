import pygame
import sys
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Led:
    def __init__(self, dir_desligado, dir_ligado, pos_x, pos_y):
        self.X = pos_x
        self.Y = pos_y
        self.rect = pygame.Rect(pos_x, pos_y, 64, 64)
        self.img_desligado = pygame.image.load(dir_desligado)
        self.img_ligado = pygame.image.load(dir_ligado)
        self.img_atual = self.img_desligado
        self.estado_atual = False  # Desligado

    def desligar(self):
        """
        desliga a LED
        :return: Nada
        """
        self.estado_atual = False
        self.img_atual = self.img_desligado

    def ligar(self):
        """
        liga a LED
        :return: Nada
        """
        self.estado_atual = True
        self.img_atual = self.img_ligado

    def get_estado(self):
        """
        retorna se o led está ligada (True) ou não (False)
        :return: boolean
        """
        return self.estado_atual

    def set_pos(self, x, y):
        """
        modifica a posição da LED
        :param x: posição do objeto em x
        :param y: posição do objeto em y
        :return: Nada
        """
        self.X = x
        self.Y = y
        self.update_rect()

    def get_pos(self):
        """
        retorna o valor da posição X e Y da LED
        :return: tupla com as posições
        """
        return self.X, self.Y

    def get_rect(self):
        """
        obtém o objeto rect da LED
        :return: pygame.Rect
        """
        return self.rect

    def update_rect(self):
        """
        atualiza os valores do pygame.Rect da LED
        :return: Nada
        """
        self.rect.update(self.X, self.Y, 64, 64)


class Button:
    def __init__(self, dir_button, pos_x, pos_y):
        self.X = pos_x
        self.Y = pos_y
        self.rect = pygame.Rect(pos_x, pos_y, 128, 64)
        self.img = pygame.image.load(dir_button)
        self.botao_correto = False
        self.pontuar = 0

    def set_pos(self, x, y):
        """
        modifica a posição do botão
        :param x: posição do objeto em x
        :param y: posição do objeto em y
        :return: Nada
        """
        self.X = x
        self.Y = y

    def get_pos(self):
        """
        retorna o valor da posição X e Y do botão
        :return: tupla com as posições
        """
        return self.X, self.Y

    def get_rect(self):
        """
        obtém o objeto rect do botão
        :return: pygame.Rect
        """
        return self.rect

    def is_clicked(self):
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.botao_correto:
                self.pontuar = 1
            else:
                self.pontuar = 0
                # game over
                # sys.exit()
            return True
        return False

    def update_rect(self):
        """
        atualiza os valores do pygame.Rect do botão
        :return: Nada
        """
        self.rect.update(self.X, self.Y, 128, 64)


class Cronometro:
    def __init__(self, i):
        self.inicio = None
        self.intervalo = i
        self.is_pause = True

    def iniciar_cronometro(self):
        self.inicio = pygame.time.get_ticks() / 1000
        self.is_pause = False

    def contagem(self):
        if self.get_contagem() >= self.intervalo and not self.is_pause:
            self.inicio = pygame.time.get_ticks()
            return True
        return False

    def get_contagem(self):
        return (pygame.time.get_ticks() - self.inicio) / 1000

    def reset(self):
        self.inicio = pygame.time.get_ticks()


class Game:
    def __init__(self, tela):
        # Variáveis
        self.screen = tela
        self.resposta_certa = -1
        self.resposta = 0
        self.score_value = 0
        self.cronometro = Cronometro(3)
        self.cronometro.iniciar_cronometro()
        self.gameover = False

        # Texto do score
        self.font_score = pygame.font.Font("fonts/freesansbold.ttf", 32)
        self.text_score = self.font_score.render(f"Score = {self.score_value}",
                                                 True,
                                                 (255, 255, 255))

        # Título central do jogo
        self.font_titulo = pygame.font.Font("fonts/freesansbold.ttf", 32)
        self.text_titulo = self.font_titulo.render("pense BEM rápido",
                                                   True,
                                                   (255, 255, 255))
        # Centralizar em X
        self.text_rect_titulo = self.text_titulo.get_rect(center=(SCREEN_WIDTH / 2, 100))

        # Texto game over
        self.font_game_over = pygame.font.Font("fonts/freesansbold.ttf", 70)
        self.text_game_over = self.font_game_over.render("GAME OVER",
                                                         True,
                                                         (255, 255, 255))
        # Centralizar em X e Y
        self.text_rect_game_over = self.text_game_over.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        # Texto do pressione espaço
        self.text_pressione = self.font_score.render("Pressione <Espaço> para continuar",
                                                     True,
                                                     (255, 255, 255))
        self.text_rect_pressione = self.text_pressione.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60))

        # Sounds
        self.score_up_sound = pygame.mixer.Sound("sounds/score_up.wav")

        # Inicializar os LEDs
        self.leds = []
        self.leds.append(Led("imagens/desligado.png", "imagens/verde_ligado.png", 3 * 64, 200))
        self.leds.append(Led("imagens/desligado.png", "imagens/vermelho_ligado.png", 5 * 64, 200))
        self.leds.append(Led("imagens/desligado.png", "imagens/amarelo_ligado.png", 7 * 64, 200))
        self.leds.append(Led("imagens/desligado.png", "imagens/azul_ligado.png", 9 * 64, 200))

        # Inicializar os botões
        self.buttons = []
        self.buttons.append(Button("imagens/button_verde.png", 1 * 128, 400))
        self.buttons.append(Button("imagens/button_vermelho.png", 2.2 * 128, 400))
        self.buttons.append(Button("imagens/button_amarelo.png", 3.4 * 128, 400))
        self.buttons.append(Button("imagens/button_azul.png", 4.6 * 128, 400))

    def desenhar_leds(self):
        """
        desenha as quatro LEDS na tela
        :return: Nada
        """
        for led in self.leds:
            self.screen.blit(led.img_atual, led.get_pos())

    def desenhar_buttons(self):
        """
        desenha os quatro botões na tela
        :return: Nada
        """
        for button in self.buttons:
            self.screen.blit(button.img, button.get_pos())

    def desenhar_textos(self):
        """
        desenha os textos na tela
        :return: Nada
        """
        self.screen.blit(self.text_titulo, self.text_rect_titulo)
        self.screen.blit(self.text_score, (10, 10))

    def sortear_led(self):
        self.cronometro.reset()
        sorteio = random.randint(0, 3)
        for i in range(len(self.leds)):
            if i == sorteio:
                self.leds[i].ligar()
            else:
                self.leds[i].desligar()
        for i in range(len(self.buttons)):
            if i == sorteio:
                self.buttons[i].botao_correto = True
            else:
                self.buttons[i].botao_correto = False

    def resultado(self):
        soma = 0
        for button in self.buttons:
            soma += button.pontuar
            button.pontuar = 0
        if soma == 1:
            self.acertou()
        else:
            self.tela_game_over()

    def show_score(self):
        self.text_score = self.font_score.render(f"Score = {self.score_value}",
                                                 True,
                                                 (255, 255, 255))
        self.screen.blit(self.text_score, (10, 10))

    def game_update(self):
        """
        Atualiza as posições dos elementos
        :return: Nada
        """
        for led in self.leds:
            led.update_rect()
        for button in self.buttons:
            button.update_rect()

        self.show_score()

    def tela_game_over(self):
        self.gameover = True
        # Texto game over
        screen.fill((10, 10, 10))  # Essa linha tem que ser a primeira
        screen.blit(self.text_game_over, self.text_rect_game_over)
        self.show_score()
        screen.blit(self.text_pressione, self.text_rect_pressione)
        pygame.display.update()

    def acertou(self):
        self.score_value += 1
        self.score_up_sound.play()
        self.desligar_todas_leds()
        self.sortear_led()

    def desligar_todas_leds(self):
        for led in self.leds:
            led.desligar()
        self.desenhar_leds()
        pygame.display.update()
        pygame.time.delay(200)


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

    cronometro_inicio = Cronometro(2)
    game.sortear_led()
    jogador_clicou = False
    # Game Loop
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Pressionou o botão
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in game.buttons:
                    if button.is_clicked():
                        game.resultado()
            elif event.type == pygame.KEYDOWN and game.gameover:
                if event.key == pygame.K_SPACE:
                    # Reseta todos as variáveís
                    game.gameover = False
                    jogador_clicou = False
                    game.score_value = 0

        if not game.gameover:
            screen.fill((10, 10, 10))  # Essa linha tem que ser a primeira

            # Desenhar os elementos na tela
            game.desenhar_leds()
            game.desenhar_buttons()
            game.desenhar_textos()

            # Acende a Luz
            if game.cronometro.contagem():
                # Lógica para dá game over quando o jogador não clica em nenhum botão
                if not jogador_clicou:
                    game.tela_game_over()
                else:
                    game.sortear_led()

            game.game_update()
            pygame.display.update()
        else:
            game.tela_game_over()
