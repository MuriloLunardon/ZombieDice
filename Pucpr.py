from random import shuffle, choice
from time import sleep
from collections import namedtuple
from colorama import init, Fore, Style
init()
Dado = namedtuple("Dado", ['cor', 'lados'])

# Cria a classe dos dados
def criar_dados():
    dado_verde = Dado('verde', ['tiro', 'cerebro', 'cerebro', 'cerebro', 'passo', 'passo'])
    dado_vermelho = Dado('vermelho', ['tiro', 'tiro', 'tiro', 'cerebro', 'passo', 'passo'])
    dado_amarelo = Dado('amarelo', ['tiro', 'tiro', 'cerebro', 'cerebro', 'passo', 'passo'])

    lista_dados = [dado_verde, dado_verde, dado_verde, dado_verde, dado_verde, dado_verde,
                   dado_vermelho, dado_vermelho, dado_vermelho,
                   dado_amarelo, dado_amarelo, dado_amarelo, dado_amarelo]
    shuffle(lista_dados)
    return lista_dados


def verificar_dados(dado, lado_sorteado, tempscore, lista_dados, dados_na_mao):

    if lado_sorteado == 'cerebro':
        tempscore['cerebros'] += 1
        lista_dados.append(dados_na_mao.pop(dados_na_mao.index(dado)))
    elif lado_sorteado == 'tiro':
        tempscore['tiros'] += 1
        lista_dados.append(dados_na_mao.pop(dados_na_mao.index(dado)))

    shuffle(lista_dados)


def criar_players():
    players = []

    while True:
        try:
             num_players = int(input(f"{Fore.BLUE}{Style.BRIGHT}Digite quantos jogadores irão jogar: "))
             if num_players > 1:
                 break
             else:
                 print("Voce não pode jogar sozinho !!")
        except ValueError:
            print("O Numero precisa ser inteiro.")

    for i in range(num_players):
        nome = input(f"Digite o nome do jogador {i+1}: ").capitalize()
        player = {'nome': nome, 'score': 0}
        players.append(player)

    shuffle(players)
    sleep(0.3)
    print(f"*** ORDEM PARA JOGAR ***")
    n = 1
    for player in players:
        print(f"{n}. {player['nome']}")
        n += 1

    return players


def text_color(cor_dado):
    if cor_dado == 'verde':
        return Fore.LIGHTGREEN_EX
    elif cor_dado == 'amarelo':
        return Fore.YELLOW
    else:
        return Fore.RED


def turno(player):
    sleep(0.3)
    print(f"\nVez do jogador {player['nome']}")
    x = input("Pressione enter para continuar")
    lista_dados = criar_dados()
    tempscore = {'cerebros': 0, 'tiros': 0}
    dados_na_mao = []
    while True:
        while len(dados_na_mao) < 3:
            dados_na_mao.append(lista_dados.pop())

        n = 1
        for dado in reversed(dados_na_mao):
            sleep(0.3)
            print(f"\n{Fore.BLUE}Jogando dado {n}")
            n += 1

            cor = dado.cor
            cor_txt = text_color(cor)
            shuffle(dado.lados)
            lado_sorteado = choice(dado.lados)

            print(f"{cor_txt}   Cor: {cor}\n   Lado: {lado_sorteado}")
            verificar_dados(dado, lado_sorteado, tempscore, lista_dados, dados_na_mao)

        print(f"{Fore.BLUE}\nCérebros atuais: {tempscore['cerebros']}\nTiros atuais: {tempscore['tiros']}")
        if tempscore['tiros'] < 3:
            if input("Deseja continuar jogando? (s/n): ").upper() != 'S':
                print(f"Você conseguiu {tempscore['cerebros']} cérebros.")
                player['score'] += tempscore['cerebros']
                break
        else:
            print(f"Você tomou muitos tiros e acabou perdendo {tempscore['cerebros']} cérebros.")
            break


def placar(players):
    print(f"\n*** PLACAR ATUAL ***")
    for player in players:
        print(f"{player['nome']}: {player['score']} pontos.")


if __name__ == '__main__':
    players = criar_players()

    game_over = False
    while not game_over:
        for player in players:
            turno(player)
            if player['score'] >= 13:
                winner = player['nome']
                game_over = True
        if not game_over:
            placar(players)
        else:
            print(f"\nO jogo acabou. O grande vencedor foi: {winner}")
            placar(players)