import random
from time import sleep
# DADOS DAS CARTAS NECESSÁRIOS PARA O JOGO
naipes = ('Copas', 'Ouros', 'Espadas', 'Paus')
numeros = ('Dois', 'Tres', 'Quatro', 'Cinco', 'Seis', 'Sete', 'Oito', 'Nove', 'Dez', 'Valete', 'Dama', 'Rei', 'As')
valores = {'Dois': 2, 'Tres': 3, 'Quatro': 4, 'Cinco': 5, 'Seis': 6, 'Sete': 7, 'Oito': 8,
           'Nove': 9, 'Dez': 10, 'Valete': 10, 'Dama': 10, 'Rei': 10, 'As': 11}

jogando = True


class Card:
    def __init__(self, naipe, num):
        self.naipe = naipe
        self.num = num
        self.valor = valores[num]

    def __str__(self):
        return self.num + ' de ' + self.naipe


class Deck:
    def __init__(self):
        self.baralho = []

        for naipe in naipes:
            for num in numeros:
                carta = Card(naipe, num)
                self.baralho.append(carta)

    def embaralhar(self):
        random.shuffle(self.baralho)

    def puxar_uma(self):
        return self.baralho.pop()


class Hand:
    def __init__(self):
        self.mao = []
        self.pontos = 0
        self.ases = 0

    def add_cartas(self, novas_cartas):
        self.mao.append(novas_cartas)
        self.pontos += novas_cartas.valor
        if novas_cartas.num == 'As':
            self.ases += 1

    def ajuste_ases(self):
        while self.pontos > 21 and self.ases:
            self.pontos -= 10
            self.ases -= 1


class Chips:
    def __init__(self, total=100):
        self.total = total
        self.aposta = 0

    def ganhou_aposta(self):
        self.total += self.aposta

    def perdeu_aposta(self):
        self.total -= self.aposta


def checar_aposta(fichas):
    while True:
        try:
            fichas.aposta = int(input('\nInforme quantas fichas deseja apostar: '))
        except ValueError:
            print('Desculpe, o número de fichas deve ser um número inteiro!')
        else:
            if fichas.aposta > fichas.total:
                print(f'Desculpa, mas sua aposta não pode ultrapassar seu total de fichas que é de {fichas.total}')
            else:
                break


def mostrar_parte_mao(jogador, negociante):
    sleep(1.5)
    print('\nMÃO DO NEGOCIANTE: ')
    print('< CARTA VIRADA >')
    print(negociante.mao[1])
    sleep(1.5)
    print('\nMÃO DO JOGADOR:', *jogador.mao, sep='\n')
    print(f'>>VALOR DA MÃO JOGADOR: {jogador.pontos}')


def mostrar_toda_mao(jogador, negociante):
    sleep(1.5)
    print('\nMÃO DO NEGOCIANTE:', *negociante.mao, sep='\n')
    print(f'>>VALOR DA MÃO NEGOCIANTE: {negociante.pontos}')
    sleep(1.5)
    print('\nMÃO DO JOGADOR:', *jogador.mao, sep='\n')
    print(f'>>VALOR DA MÃO JOGADOR: {jogador.pontos}')


def hit(deck, mao):
    mao.add_cartas(deck.puxar_uma())
    mao.ajuste_ases()


def hit_or_stand(deck, mao):
    global jogando

    while True:
        sleep(1.5)
        res = input("Quer comprar ou parar? Digite 'c' ou 'p' ")
        if res[0] == 'c':
            hit(deck, mao)
        elif res[0] == 'p':
            print('Jogador escolheu parar. Negociante joga agora')
            jogando = False
        else:
            print('Por favor, tente novamente')
            continue
        break


def jogador_estoura(fichas):
    print('Jogador ESTOUROU 21!')
    fichas.perdeu_aposta()


def jogador_vence(fichas):
    print('Jogador VENCEU!')
    fichas.ganhou_aposta()


def negociante_estoura(fichas):
    print('Negociante ESTOUROU 21!')
    fichas.ganhou_aposta()


def negociante_vence(fichas):
    print('Negociante VENCEU!')
    fichas.perdeu_aposta()


def empate():
    print('Jogador e Negociante empataram. É um push')


cont = 0
while True:
    print('-' * 90)
    print(f'{"BEM-VINDO AO BLACKJACK":^90}')
    print('-' * 90)
    print('Bem-vindo ao BlackJack, chegue o mais próximo de 21 sem estourar!\n'
          'O Negociante irá comprar até chegar a 17. Ases podem ter valor 1 ou 11 dependendo da mão')
    # CRIAÇÃO DO BARALHO:
    baralho = Deck()
    baralho.embaralhar()

    # CRIAÇÃO DOS JOGADORES E SUAS FICHAS E DANDO PRIMEIRAS DUAS CARTAS:
    mao_jogador = Hand()

    # VERIFICANDO SE ESTÁ NO COMEÇO DA PARTIDA E ASSIM SOLICITANDO O Nº DE FICHAS INICIAIS
    if cont == 0:
        while True:
            try:
                n_fichas = int(input('\nInforme quantas fichas você possui: '))
                break
            except ValueError:
                print('Desculpe, o número de fichas deve ser um número inteiro!')
        fichas_jogador = Chips(n_fichas)

    mao_jogador.add_cartas(baralho.puxar_uma())
    mao_jogador.add_cartas(baralho.puxar_uma())

    mao_negociante = Hand()
    mao_negociante.add_cartas(baralho.puxar_uma())
    mao_negociante.add_cartas(baralho.puxar_uma())

    # DEFININDO APOSTAS E SE O JOGADOR POSSUI FICHAS AINDA:
    if fichas_jogador.total == 0:
        print('\nVocê não possui fichas, não é possível jogar!\n'
              'Obrigado por jogar! Até mais...')
        break
    checar_aposta(fichas_jogador)

    # MOSTRANDO MÃOS DOS JOGADORES E DO NEGOCIANTE:
    mostrar_parte_mao(mao_jogador, mao_negociante)

    # LOOP PARA OCORRER OS HITS OU STANDS
    while jogando:

        # PERGUNTANDO SE O JOGADOR QUER OU NÃO CONTINUAR:
        hit_or_stand(baralho, mao_jogador)

        # MOSTRANDO NOVAMENTE A MÃO DOS JOGADORES:
        mostrar_parte_mao(mao_jogador, mao_negociante)

        # CHECANDO SE O JOGADOR JÁ ESTOUROU:
        if mao_jogador.pontos > 21:
            jogador_estoura(fichas_jogador)
            break

    # SE O JOGADOR AINDA NÃO ESTOUROU É A VEZ DO NEGOCIANTE:
    if mao_jogador.pontos <= 21:

        # NEGOCIANTE PRECISA COMPRAR ATÉ CHEGAR EM 17 AO MENOS:
        while mao_negociante.pontos < 17:
            hit(baralho, mao_negociante)

        # MOSTRANDO AS MÃOS DO JOGADOR E DO NEGOCIANTE, SEM OCULTAR NADA:
        mostrar_toda_mao(mao_jogador, mao_negociante)

        # VERIFICANDO AS POSSIBILIDADES DE VITÓRIAS E DERROTAS
        if mao_negociante.pontos > 21:
            negociante_estoura(fichas_jogador)
        elif mao_negociante.pontos > mao_jogador.pontos:
            negociante_vence(fichas_jogador)
        elif mao_negociante.pontos < mao_jogador.pontos:
            jogador_vence(fichas_jogador)
        else:
            empate()

    # MOSTRAR AO JOGADOR SEU SALDO DE FICHAS:
    print(f'\nFICHAS DO JOGADOR: {fichas_jogador.total}')

    # VERIFICAR SE QUER CONTINUAR A JOGAR:
    while True:
        opcao = input('Deseja jogar mais uma mão? [S/N]: ').upper()[0]
        if opcao in 'SN':
            break
    if opcao == 'S':
        jogando = True
        cont += 1
        continue
    else:
        print('Obrigado por jogar! Até mais...')
        break
