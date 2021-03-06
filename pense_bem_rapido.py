import pygame
import sys
import random

SCREEN_WIDTH = 800 # Largura da tela
SCREEN_HEIGHT = 600 # Altura da tela


class Led:
    def __init__(self, dir_desligado, dir_ligado, pos_x, pos_y):
        self.X = pos_x
        self.Y = pos_y
        self.rect = pygame.Rect(pos_x, pos_y, 64, 64)
        self.img_desligado = pygame.image.load(dir_desligado)
        self.img_ligado = pygame.image.load(dir_ligado)
        self.img_atual = self.img_desligado  # Armazena a imagem ativada ou desativada
        self.estado_atual = False  # False = desativado e True = ativado

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
        """
        :param dir_button: diretório da imagem do botão
        :param pos_x: posição no eixo X
        :param pos_y: posição no eixo Y
        """
        self.X = pos_x
        self.Y = pos_y
        self.rect = pygame.Rect(pos_x, pos_y, 128, 64)
        self.img = pygame.image.load(dir_button)
        self.botao_correto = False  # Variável que vai dizer se o botão é o correto a se apertar
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
        """
        Verifica se o botão foi pressionado e também se foi pressionado correto
        :return:
        """
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.botao_correto:
                self.pontuar = 1  # O botão correto soma 1 para ser verificado depois se acertou ou errou
            else:
                self.pontuar = 0
            return True
        return False

    def update_rect(self):
        """
        atualiza os valores do pygame.Rect do botão
        :return: Nada
        """
        self.rect.update(self.X, self.Y, 128, 64)


class Not:
    """
    Classe para criação das NOTs
    """
    def __init__(self, dir_not, pos_x, pos_y):
        """
        inicializar Not
        :param dir_not: diretorio da imagem do not
        :param pos_x: posição no eixo x
        :param pos_y: posilção no eixo y
        """
        self.X = pos_x
        self.Y = pos_y
        self.rect = pygame.Rect(pos_x, pos_y, 64, 64)
        self.img = pygame.image.load(dir_not)
        self.img.set_alpha(0)  # esconder not
        self.estado_atual = False  # Desligado

    def desligar(self):
        """
        desliga a LED
        :return: Nada
        """
        self.estado_atual = False
        self.img.set_alpha(0)

    def ligar(self):
        """
        liga a LED
        :return: Nada
        """
        self.estado_atual = True
        self.img.set_alpha(255)

    def set_pos(self, x, y):
        """
        modifica a posição do not
        :param x: posição do objeto em x
        :param y: posição do objeto em y
        :return: Nada
        """
        self.X = x
        self.Y = y

    def get_pos(self):
        """
        retorna o valor da posição X e Y do not
        :return: tupla com as posições
        """
        return self.X, self.Y

    def get_rect(self):
        """
        obtém o objeto rect do not
        :return: pygame.Rect
        """
        return self.rect

    def update_rect(self):
        """
        atualiza os valores do pygame.Rect do not
        :return: Nada
        """
        self.rect.update(self.X, self.Y, 128, 64)


class Cronometro:
    def __init__(self, i):
        """
        Inicializa Cronometro
        :param i: intervalo do timer em loop
        """
        self.inicio = None
        self.intervalo = i
        self.is_pause = True

    def iniciar_cronometro(self):
        """
        Inicializa o cronômetro para que o inicio fique fixo
        :return: Nada
        """
        self.inicio = pygame.time.get_ticks()
        self.is_pause = False

    def contagem(self):
        """
        Função presente nos ifs para saber se contou até o intervalo especificado
        :return: True se chegou no intervalo e False quando não chega
        """
        if self.get_contagem() >= self.intervalo and not self.is_pause:
            self.inicio = pygame.time.get_ticks()
            return True
        return False

    def get_contagem(self):
        """
        Método para realizar o cálculo do tempo que se passou desde do inicio do cronometro em segundos
        :return: boolean (segundos)
        """
        return (pygame.time.get_ticks() - self.inicio) / 1000

    def reset(self):
        """
        Reseta o cronômetro
        :return:
        """
        self.inicio = pygame.time.get_ticks()


class Game:
    def __init__(self, tela):
        # Variáveis
        self.screen = tela
        self.resposta_certa = -1  # armazena o botão certo para se pressionar
        self.resposta = 0  # armazena o botão pressionado
        self.score_value = 0  # armazena o tanto de acertos
        self.tempo_de_pensar = 3.2  # velocidade para dá uma resposta
        self.cronometro = Cronometro(self.tempo_de_pensar)
        self.cronometro.iniciar_cronometro()
        self.gameover = False  # se true então errou ou passou o tempo

        # Texto do score
        self.font_score = pygame.font.Font("fonts/RobotoMono-Regular.ttf", 32)
        self.text_score = self.font_score.render(f"Score = {self.score_value}",
                                                 True,
                                                 (255, 255, 255))

        # Título central do jogo
        self.font_titulo = pygame.font.Font("fonts/RobotoMono-Regular.ttf", 80)
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

        # Texto brenoAV

        self.text_brenoav = self.font_score.render("brenoAV",
                                                   True,
                                                   (255, 255, 255))

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
        self.buttons.append(Button("imagens/button_verde.png", 2.1 * 128, 400))
        self.buttons.append(Button("imagens/button_vermelho.png", 2.1 * 128, 480))
        self.buttons.append(Button("imagens/button_amarelo.png", 3.3 * 128, 400))
        self.buttons.append(Button("imagens/button_azul.png", 3.3 * 128, 480))

        # Not

        self.not1 = Not("imagens/not.png", 310, 300)
        self.not2 = Not("imagens/not.png", 460, 300)

    def desenhar_leds(self):
        """
        desenha as quatro LEDS na tela
        :return: Nada
        """
        for led in self.leds:
            self.screen.blit(led.img_atual, led.get_pos())

    def desenhar_nots(self):
        """
        desenha os dois NOTs na tela
        :return:
        """
        self.screen.blit(self.not1.img, self.not1.get_pos())
        self.screen.blit(self.not2.img, self.not2.get_pos())

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
        self.screen.blit(self.text_brenoav, (650, 550))

    def sortear_led(self):
        """
        Função responsável pelo sorteio das leds e continuação do jogo
        :return: Nada
        """
        self.cronometro.reset()  # reseta o cronômetro para zero e começa a contagem
        sorteio_led_cor = random.randint(0, 3)  # 0 - verde , 1 - vermelho, 2 - amarelo, 3 - azul
        sorteio_nots = random.randint(0, 3)  # 0,3 - sem nenhuma not, 1 - uma not, 2 - duas not
        if self.score_value <= 5:  # Começa com nots a partir do 5
            sorteio_nots = 0
        for i in range(len(self.leds)):  # Liga a porta para aparecer na tela
            if i == sorteio_led_cor:
                self.leds[i].ligar()
            else:
                self.leds[i].desligar()
        if sorteio_nots == 0 or sorteio_nots >= 2:
            if sorteio_nots == 2:
                self.not1.ligar()
                self.not2.ligar()
            else:
                self.not1.desligar()
                self.not2.desligar()

            for i in range(len(self.buttons)):  # define um botão verdadeiro e o restante falso
                if i == sorteio_led_cor:
                    self.buttons[i].botao_correto = True
                else:
                    self.buttons[i].botao_correto = False
        elif sorteio_nots == 1:
            self.not1.ligar()
            self.not2.desligar()
            for i in range(len(self.buttons)):  # define um botão falso e o restante verdadeiro
                if i == sorteio_led_cor:
                    self.buttons[i].botao_correto = False
                else:
                    self.buttons[i].botao_correto = True

    def resultado(self):
        """
        Método que faz a análise se o player acertou ou não
        :return:
        """
        soma = 0
        for button in self.buttons:
            soma += button.pontuar
            button.pontuar = 0
        if soma == 1:  # Se o player acertou um botão no método de is_clicked() vai atribuir 1
            self.acertou()
        else:
            self.tela_game_over()

    def show_score(self):
        """
        Método que atualiza o valor do score na tela
        :return: Nada
        """
        self.text_score = self.font_score.render(f"Score = {self.score_value}",
                                                 True,
                                                 (255, 255, 255))
        self.screen.blit(self.text_score, (10, 10))
        pygame.display.update()

    def game_update(self):
        """
        Atualiza as posições dos elementos durante tdo loop
        :return: Nada
        """
        for led in self.leds:
            led.update_rect()
        for button in self.buttons:
            button.update_rect()
        self.show_score()

    def tela_game_over(self):
        """
        Forma a tela de game over e freeza o jogo até o player apertar espaço
        :return: Nada
        """
        self.gameover = True
        # Texto game over
        screen.fill((10, 10, 10))  # Essa linha tem que ser a primeira
        screen.blit(self.text_game_over, self.text_rect_game_over)
        screen.blit(self.text_pressione, self.text_rect_pressione)
        self.show_score()
        pygame.display.update()

    def acertou(self):
        """
        Contabiliza os pontos de acerto e faz barulho
        :return:
        """
        self.score_value += 1
        self.score_up_sound.play()
        self.desligar_todas_leds()
        self.sortear_led()

    def desligar_todas_leds(self):
        """
        Desliga as leds e espera um delay para aparecer outra LEDs
        :return:
        """
        for led in self.leds:
            led.desligar()
        self.desenhar_leds()
        pygame.display.update()
        pygame.time.delay(200)  # Pausa o jogo por 200ms do tempo para sortear outra LED


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

    jogador_clicou = False
    pausa_inicial = True

    # Game Loop
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Clicou com o esquerdo
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in game.buttons:
                    if button.is_clicked():  # verifica se o player pressionou ou não um botão dos 4
                        game.resultado()
            elif event.type == pygame.KEYDOWN and game.gameover:
                if event.key == pygame.K_SPACE:
                    # Reseta todos as variáveís
                    game.gameover = False
                    jogador_clicou = False
                    game.score_value = 0
                    game.sortear_led()  # começa dnv a sortear

        if not game.gameover:

            screen.fill((10, 10, 10))  # Essa linha tem que ser a primeira

            # Desenhar os elementos na tela
            game.desenhar_leds()
            game.desenhar_buttons()
            game.desenhar_textos()
            game.desenhar_nots()
            pygame.display.update()

            # Pausa para começar
            if pausa_inicial:
                pygame.time.delay(1200)
                game.sortear_led()
                pausa_inicial = False

            # Verifica se o player não apertou em nenhum botão para dá game over
            if game.cronometro.contagem():
                # Lógica para dá game over quando o jogador não clica em nenhum botão
                if not jogador_clicou:
                    game.tela_game_over()

            game.game_update()
            pygame.display.update()
        else:  # Else que fica preso na tela de game over até que seja pressionado <espaço>
            game.tela_game_over()
