import pygame, sys
from pygame.locals import *
from random import randint

class Cobra:
    #cores
    COR_FUNDO = (255, 255, 255)
    COR_DESTAQUE = (245, 27, 230)
    COR_TEXTO = (63, 8, 59)
    COR_COMIDA = (255, 0, 0)
    COR_CABECA = (175, 11, 193)
    COR_CORPO = (255, 0, 255)

    #bloco
    BLOCO = [18, 18]

    #direçoes
    DIREITA = 6
    ESQUERDA = 4
    CIMA = 8
    BAIXO = 2

    #janela
    COMPRIMENTO_JANELA = 440
    ALTURA_JANELA = 510
    TELA = None
    VELOCIDADE = 5

    #controlar o jogo
    morto = False
    pontos = 0
    direcao = None
    relogio = None

    #cobra
    COBRA = [[30, 120], [10, 120]]
    CABECA = [30, 120]

    TEM_COMIDA = False
    COMIDA_POS = None

    def start(self):
        #inicializa o jogo com a cobra ir pra direita
        #sem pontos
        self.direcao = self.DIREITA
        self.morto = False
        self.pontos = 0

        pygame.init()
        self.relogio = pygame.time.Clock()

        self.jogar()

    #cria a tela do jogo
    def construirJogo(self):
        self.TELA = pygame.display.set_mode((self.COMPRIMENTO_JANELA, self.ALTURA_JANELA), 0, 32)
        pygame.display.set_caption('Cobra Xtreme Snake 2.0')

    def jogar(self):
        self.construirJogo()

        self.adicionarComida()

        while not self.morto:
            
            for evento in pygame.event.get():
                print(evento)

                if evento.type == QUIT:
                    pygame.quit() #fecha a janela do jogo
                    sys.exit() #fecha o terminal

                if evento.type == KEYDOWN:
                    if evento.key == K_LEFT or evento.key == ord('o'):
                        self.direcao = self.ESQUERDA
                    elif evento.key == K_RIGHT or evento.key == ord('p'):
                        self.direcao = self.DIREITA
                    elif evento.key == K_UP or evento.key == ord('k'):
                        self.direcao = self.CIMA
                    elif evento.key == K_DOWN or evento.key == ord('m'):
                        self.direcao = self.BAIXO

            self.calculaDirecaoCabeca()

            if not self.TEM_COMIDA:
                self.adicionarComida()

            #adiciona a cabeca da cobra na lista do corpo da serpente
            self.COBRA.insert(0, list(self.CABECA))

            #verificar se a cobra comer a comida
            if self.CABECA[0] == self.COMIDA_POS[0] and self.CABECA[1] == self.COMIDA_POS[1]:
                self.TEM_COMIDA = False
                self.pontos += 500
                self.VELOCIDADE += 1
            else:
                self.COBRA.pop()

            self.desenharJogo()

    def adicionarComida(self):
        while True:
            x1 = randint(0, 20)
            y1 = randint(0, 17)

            #cria uma comida em uma posicao aleatoria
            self.COMIDA_POS = [int(x1 * 20) + 10, int(y1 * 20) + 120]

            #verifica se a comida nao esta na cobra
            if self.COBRA.count(self.COMIDA_POS) == 0:
                self.TEM_COMIDA = True
                break

    def calculaDirecaoCabeca(self):
        match self.direcao:
            case self.DIREITA:
                self.CABECA[0] += 20

                if(self.CABECA[0] >= self.COMPRIMENTO_JANELA - 20):
                    self.morto = True
            case self.ESQUERDA:
                self.CABECA[0] -= 20

                if(self.CABECA[0] < 10):
                    self.morto = True
            case self.CIMA:
                self.CABECA[1] -= 20

                if(self.CABECA[1] < 110):
                    self.morto = True
                
            case self.BAIXO:
                self.CABECA[1] += 20

                if(self.CABECA[1] >= self.ALTURA_JANELA - 30):
                    self.morto = True
                
        #verifica se a cobra bateu nela mesma
        if self.COBRA.count(self.CABECA) > 0:
            self.morto = True

    def desenharJogo(self):
        self.TELA.fill(self.COR_FUNDO)

        #desenha o placar do pontuação
        pygame.draw.rect(self.TELA, self.COR_DESTAQUE, Rect([10, 10], [420,100]), 1)

        #escreve o texto do placar
        font = pygame.font.Font(None, 40)
        placar = font.render("Pontos:" + str(self.pontos), 1, self.COR_TEXTO)

        posicaoPlacar = placar.get_rect()
        posicaoPlacar.left = 75
        posicaoPlacar.top = 45

        #desenha o placar na tela
        self.TELA.blit(placar, posicaoPlacar)

        #desenha a area do jogo
        pygame.draw.rect(self.TELA, self.COR_DESTAQUE, Rect([10,120], [420,380]), 1)

        #desenha comida
        pygame.draw.rect(self.TELA, self.COR_COMIDA, Rect(self.COMIDA_POS, self.BLOCO))

        #desenha a cobra
        for quadradinho in self.COBRA:
            if quadradinho == self.COBRA[0]:
                pygame.draw.rect(self.TELA, self.COR_CABECA, Rect(quadradinho, self.BLOCO))
            else:
                pygame.draw.rect(self.TELA, self.COR_CORPO, Rect(quadradinho, self.BLOCO))

        pygame.display.update()
        self.relogio.tick(9)