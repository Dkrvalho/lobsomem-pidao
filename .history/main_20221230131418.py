import pygame 
from sys import exit
from random import randint

def mostra_pontos():
    tempo_atual = pygame.time.get_ticks() - inicio #subtraindo a váriável pelo início vai fazer com que sempre que o jogo reinicia ele começa a pontuação do zero
    pontos_txt = fonte.render(f'Pontos: {int(tempo_atual/100)}', False, "Black")
    pontos_txt_ret = pontos_txt.get_rect(midtop = (400,25))
    janela.blit(pontos_txt,pontos_txt_ret)
    return tempo_atual

def inimigo_movimento(obstaculo_lista):
    if obstaculo_lista:
        for obstaculo_ret in obstaculo_lista:
            obstaculo_ret.x -= 8
            
            if obstaculo_ret.bottom == 370:
                janela.blit(rato, obstaculo_ret) #pode ser feito em outra função
            else:
                janela.blit(morcego, obstaculo_ret)
        
        obstaculo_lista = [obstaculo for obstaculo in obstaculo_lista if obstaculo.x > -100] #isso é uma "list comprehension" uqe cira uma nova lista baseado nos valores quem continha na lista anterior. Ela evita que você precise fazer um for statement para dar um append da lista anterior na próxima.
            
        return obstaculo_lista
    
    else: return []

def colisao(jogador, obstaculos):
    if obstaculos:
        for obstaculo_ret in obstaculos:
            if jogador.colliderect(obstaculo_ret):
                return False
    return True

def jogador_animacao():
    global jogador, jogador_posicao
    
    if jogador_ret.bottom < 350:
        jogador = jogador_pulo
    else:
        jogador_posicao += 0.12
        if jogador_posicao >= len(jogador_andar):
            jogador_posicao = 0
        jogador = jogador_andar[int(jogador_posicao)]
        
def rato_animacao():
    global rato, rato_posicao
    
    rato_posicao += 0.12
    if rato_posicao >= len(rato_mov):
        rato_posicao = 0
    rato = rato_mov[int(rato_posicao)]
    
def morcego_animacao():
    global morcego, morcego_posicao
    
    morcego_posicao += 0.12
    if morcego_posicao >= len(morcego_mov):
        morcego_posicao = 0
    morcego = morcego_mov[int(morcego_posicao)]

pygame.init() #necessário para iniciar qualquer código com pygame
janela = pygame.display.set_mode((800,400)) #cria a anela do programa com tamanho de largura e altura
pygame.display.set_caption('Lobisomem Pidao by Dkr_') #adiciona o nome do jogo
relogio = pygame.time.Clock() #o objeto 'relógio' nos ajudará com o tempo, o que nos ajudará a controlar o 'framerate'
fonte = pygame.font.Font("Tutorial Pygamelobsomem-pidao/fontes/Bradley.ttf", 50) #especificar fonte e tamanho
jogo_ativo = True
inicio = 0 #serve para reiniciar o tempo de jogo quando o jogo reinicia
pontuacao = 0

ceu2 = pygame.image.load("lobsomem-pidao/graficos/bg1.png").convert() #criamos uma superfície pra ser exibida no display e demos um tamanho a ela, nesse caso, ela terá o tamanho da imagem
ceu1 = pygame.image.load("lobsomem-pidao/graficos/bg2.png").convert_alpha() #convert é para converter a imagem em um formato que o pygame consegue lê melhor (conver_alpha é para imagens sem fundo)
chao = pygame.image.load("lobsomem-pidao/graficos/bg3.png").convert_alpha()

'''
-----Comentando pois esses dados foram adicionados em uma função-----
pontos_txt = fonte.render("Pontos: 000", False, "White") #informação do texto (dos pontos, nesse caso), cantos arredondados e cor
pontos_txt_ret = pontos_txt.get_rect(midtop = (400,25))
'''

#teste = pygame.Surface((100,200)) #caso queiramos criar uma superfício com tamanho específico
#o posicionamento desta superfície se dá através do comando 'janela.blit(teste,(x,y))' no nosso loop de eventos
#teste.fill("Red") #caso queiramos adicionar uma cor para a fuperfície 'teste'

#Inimigos

#Rato
rato_mov_1 = pygame.image.load("lobsomem-pidao/graficos/inimigos/rato/rato1.png").convert_alpha()
rato_mov_2 = pygame.image.load("lobsomem-pidao/graficos/inimigos/rato/rato2.png").convert_alpha()
rato_mov_3 = pygame.image.load("lobsomem-pidao/graficos/inimigos/rato/rato3.png").convert_alpha()
#rato_ret = rato.get_rect(midbottom = (820,370)) #onde o inimgo inicia (não é mas necessário)
rato_mov = [rato_mov_1, rato_mov_2, rato_mov_3]
rato_posicao = 0
rato = rato_mov[rato_posicao]

#Morcego
morcego_mov_1 = pygame.image.load("lobsomem-pidao/graficos/inimigos/morcego/morcego1.png").convert_alpha()
morcego_mov_2 = pygame.image.load("lobsomem-pidao/graficos/inimigos/morcego/morcego2.png").convert_alpha()
morcego_mov_3 = pygame.image.load("lobsomem-pidao/graficos/inimigos/morcego/morcego3.png").convert_alpha()
morcego_mov = [morcego_mov_1, morcego_mov_2, morcego_mov_3]
morcego_posicao = 0
morcego = morcego_mov[morcego_posicao]

inimigo_ret_lista = []

#Jogador
jogador_andar_1 = pygame.image.load("lobsomem-pidao/graficos/jogador/jogador_a1.png").convert_alpha()
jogador_andar_2 = pygame.image.load("lobsomem-pidao/graficos/jogador/jogador_a2.png").convert_alpha()
jogador_andar_3 = pygame.image.load("lobsomem-pidao/graficos/jogador/jogador_a3.png").convert_alpha()
jogador_andar_4 = pygame.image.load("lobsomem-pidao/graficos/jogador/jogador_a4.png").convert_alpha()
jogador_andar = [jogador_andar_1, jogador_andar_2, jogador_andar_3, jogador_andar_4]
jogador_posicao = 0
jogador_pulo = pygame.image.load("lobsomem-pidao/graficos/jogador/jogador_a3.png").convert_alpha()

jogador = jogador_andar[jogador_posicao]
jogador_ret = jogador.get_rect(midbottom = (80,370)) #desenha um retângulo ao redor do jogador (53)
gravidade_jogador = 0 #número inicial da gravidade

#Tela de Indrução
jogador_tela = pygame.image.load("lobsomem-pidao/graficos/jogador/jogador_tela.png").convert_alpha()
jogador_tela = pygame.transform.rotozoom(jogador_tela, 10, 1.1)
jogador_tela_ret = jogador_tela.get_rect(midright = (400,300))

titulo_tela = fonte.render('Lobisomem', False, (158,41,55))
titulo_tela = pygame.transform.rotozoom(titulo_tela, 0, 1.8)
titulo_tela_ret = titulo_tela.get_rect(midright = (720,60))

titulo_tela_sombra = fonte.render('Lobisomem', False, "Black")
titulo_tela_sombra = pygame.transform.rotozoom(titulo_tela_sombra, 0, 1.8)
titulo_tela_sombra_ret = titulo_tela_sombra.get_rect(midright = (722,62))

titulo2_tela = fonte.render('Pidao', False, (158,41,55))
titulo2_tela = pygame.transform.rotozoom(titulo2_tela, 0, 1.6)
titulo2_tela_ret = titulo2_tela.get_rect(midright = (720,130))

titulo2_tela_sombra = fonte.render('Pidao', False, "Black")
titulo2_tela_sombra = pygame.transform.rotozoom(titulo2_tela_sombra, 0, 1.6)
titulo2_tela_sombra_ret = titulo2_tela_sombra.get_rect(midright = (722,132))

restart_tela = fonte.render("'Press SPACE to restart!'", False, (158,41,55))
restart_tela = pygame.transform.rotozoom(restart_tela, 0, 0.6)
restart_tela_ret = restart_tela.get_rect(midtop = (570,290))

restart2_tela = fonte.render("'Press SPACE to restart!'", False, "Black")
restart2_tela = pygame.transform.rotozoom(restart2_tela, 0, 0.6)
restart2_tela_ret = restart2_tela.get_rect(midtop = (572,292))

fundo_tela = pygame.image.load("lobsomem-pidao/graficos/fundo_tela.jpg").convert_alpha()

#Respaw Inimigo
inimigo_respaw = pygame.USEREVENT +1
pygame.time.set_timer(inimigo_respaw,1100)

while True: #serve para manter nossa janela aberta e atualizando enquanto o que estiver dentro for verdade.
    #desenhar todos os elementos
    #atualizar tudo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            #toda esta parte (if statement) serve para fechar o nosso programa completamente, a parte do quit no pygame serve como oposto do comando que abre a janela, enquanto o 'exit', importado do 'sys', mata completamente o processo e evita qualquer erro ao fechar nossa janela  
        if jogo_ativo:
            
            #if event.type == pygame.MOUSEMOTION:
                #print(event.pos)
                #este 'if statement' me da a posição do mouse (caso ele se mova) na janela do pygame
            if event.type == pygame.MOUSEBUTTONDOWN and jogador_ret.bottom >= 370:
                gravidade_jogador = -18
                #este 'if statement' registra quando o botão do mouse é pressionado (qualquer botão) e aplicad uma ação a ele (neste caso, ele "pula")
                #também temos o MOUSEBUTTONUP, que registra quando o botão do mouse é solto depois de pressionado
            #if event.type == pygame.MOUSEMOTION:
                #if jogador_ret.collidepoint(event.pos): print("colisão")
                #este 'if statement' registra quando o movimento do mouse (ver linhas 30) coincide com o retângulo do jogador.
            if event.type == inimigo_respaw:
                if randint(0,2):
                    inimigo_ret_lista.append(rato.get_rect(midbottom = (randint(900,1100),370)))   
                else:
                    inimigo_ret_lista.append(morcego.get_rect(midbottom = (randint(900,1100),230)))    
                
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    jogo_ativo = True
                    inicio = pygame.time.get_ticks()    
                                   
    if jogo_ativo:
    #Toda essa parte se refere ao loop do jogo em si, o jogo rodará enquanto esse 'if statemente' for 'True'                 
        janela.blit(ceu2,(0,0)) #aqui vamos exibir a nossa superfície na nossa janela na posição cima-esquerda
        janela.blit(ceu1,(0,0))
        janela.blit(chao,(0,0))
        pontuacao = mostra_pontos()
        
        '''
        -----Tudo isso vai ser executado através da função mostra_pontos-----
        
        pygame.draw.rect(janela,"Black",pontos_txt_ret)
        #aqui desenhamos um retângulo onde os parâmetros são: onde ele será desenha, cor e tamanho (no caso ele vai obedecer ao retângulo dos pontos)
        pygame.draw.rect(janela,"Black",pontos_txt_ret,20)
        #neste 4º parâmetro, definimos uma linha para o retêngulo, isso faz com que ele "perca" a cor de preenchimento, por isso ela está em uma linha duplicada
        
        janela.blit(pontos_txt,pontos_txt_ret) #as coordenadas serão a posição da janela
        '''
        
        '''
        -----Isso tudo não será mais necessário pois será emplementado em uma classe de respaw-----
        
        inimigo_ret.x -= 6 # movimento do inimigo no eixo x
        if inimigo_ret.right < 0: inimigo_ret.left = 805 #loop do inimigo. Quando a direita do retângulo for menor que o ponto 0 (sair da tela pra direita), a esquerda do inimigo volta pro ponto 805 (à direita da tela).
        janela.blit(inimigo,inimigo_ret) #superfície a ser exibida e sua posição
        '''
        
        #Jogador
        gravidade_jogador += 0.9 #ganho de gravidade por ciclo
        jogador_ret.y += gravidade_jogador #atrela o movimento do jogador no eixo y ao valor da gravidade
        if jogador_ret.bottom >= 370: jogador_ret.bottom = 370 #esse "if statemente" checa se a parte de baixo do retângulo do jogador está abaixo do ponto 380 (chão), se este for o caso, volta a 380. Isso simula a colisão do jogador com o chão.
        jogador_animacao()
        janela.blit(jogador,jogador_ret) #a janela da imagem do jogador está na posição do jogador_ret
        
        #Movemento Inimigo
        rato_animacao()
        morcego_animacao()
        inimigo_ret_lista = inimigo_movimento(inimigo_ret_lista)
        
        #Colisão
        jogo_ativo = colisao(jogador_ret, inimigo_ret_lista)
        
    else:
    #essa parte determina o que acontecerá quando o 'if statemente' do jogo se tornar 'False', ou seja, quando o personagem se colidir com o inimigo.
        janela.blit(fundo_tela,(0,0))
        janela.blit(jogador_tela,jogador_tela_ret)
        inimigo_ret_lista.clear()
        jogador_ret.midbottom = (80,370)
        gravidade_jogador = 0
        
        pontos_tela = fonte.render(f'Pontos: {int(pontuacao/100)}', False, "White")
        pontos_tela = pygame.transform.rotozoom(pontos_tela, 0, 0.7)
        pontos_tela_ret = pontos_tela.get_rect(midtop = (570,210))
        janela.blit(pontos_tela,pontos_tela_ret)
        
        janela.blit(titulo_tela_sombra,titulo_tela_sombra_ret)
        janela.blit(titulo_tela,titulo_tela_ret) 
        janela.blit(titulo2_tela_sombra,titulo2_tela_sombra_ret)
        janela.blit(titulo2_tela,titulo2_tela_ret)              
        janela.blit(restart2_tela,restart2_tela_ret)              
        janela.blit(restart_tela,restart_tela_ret)              
    
    '''
    pulo = pygame.key.get_pressed()
    if pulo[pygame.K_SPACE]:
        print("pulo")
    '''
    #esta é uma forma de implementar um evento através do pressionamento de uma tecla do jogo e é bastante útil quando estamos trabalhando com POO
    
    #if jogador_ret.colliderect(inimigo_ret): #checa a colisão de forma 'booleana', o contrário também funciona
        #print("colisão")
    
    #pos_mouse = pygame.mouse.get_pos() #cria um parâmetro para dar a posição do ponteiro do mouse
    #if jogador_ret.collidepoint(pos_mouse): #checa se o ponteiro do mouse colide com o retângulo do jogador
        #print(pygame.mouse.get_pressed()) #checa, de forma 'booleana' se cada um dos botões do mouse estão pressionados caso o mouse esteja no retângulo do jogador (fuciona para os 3 principais)
        #print("colisão com o jogador")
    
    pygame.display.update() #necessário para manter a janela aberta ***NÃO EXECUTAR SEM ANTES CRIAR O BOTÃO DE EXIT***
    relogio.tick(60) #aqui preenchemos nosso objeto com um inteiro, neste caso, falamos pro nosso programa que nosso loop não deve rodar a mais de 60fps
    
    