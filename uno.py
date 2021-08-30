from os import name, system
from random import choice, shuffle
from time import sleep


def limpa_tela():
    """realiza a limpeza da tela"""
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def mostra(jogador=None):
    """
    exibe a carta do topo ou todas as cartas de um jogador específico

    :param jogador: jogador cujas cartas serão exibidas (list)
    :return: carta do topo ou cartas do jogador escolhido (str)
    """
    if jogador is None:
        return d_cores[mesa[-1]['cor']] + mesa[-1]['valor'] + '\033[0m'
    else:
        leque = [d_cores[c['cor']] + c['valor'] + '\033[0m' for c in jogador]
        return '  '.join(leque)


def cenario():
    """exibe o cenário"""
    limpa_tela()
    for i in range(1, qtd):
        if i == vez:
            print('\033[4m', end='')
        # print(f'jogador {i}\033[0m' + f': {mostra(jogadores[i])}')
        print(f'jogador {i}' + f': {len(jogadores[i])} cartas\033[0m')
        print(sentido[0])
    if vez == 0:
        print('\033[4m', end='')
    print('você\033[0m: ' + mostra(jogadores[0]) + '\n')
    print('carta atual: ' + mostra() + '\n')


def analisa_jogada(carta):
    """
    verifica se é possível jogar uma determinada carta

    :param carta: carta que será analisada (dict)
    :return: verdadeiro/falso caso a carta seja jogável ou não (bool)
    """
    cond1 = carta['valor'] == mesa[-1]['valor']
    cond2 = carta['cor'] == mesa[-1]['cor'] and cartas_compra == 0
    cond3 = carta['valor'] in ('+4', 'C') and cartas_compra == 0
    if cond1 or cond2 or cond3:
        return True
    return False


def compra(jogador, n):
    """
    realiza a compra de cartas para um jogador

    :param jogador: jogador que irá comprar cartas (int)
    :param n: número de cartas a serem compradas (int)
    """
    for _ in range(n):
        jogadores[jogador].append(b.pop())


def executa(carta):
    """
    executa os efeitos das cartas não-numéricas

    :param carta: carta cujo efeito será executado (dict)
    :return: próximo a jogar e quantidade de cartas para compra (tuple)
    """
    if carta['valor'] in ('C', '+4'):
        if vez == 0:
            while True:
                entrada = input('digite uma cor: ').strip().lower()
                if entrada in cores:
                    break
                cenario()
                print('cor inválida!')
            carta['cor'] = entrada
        else:
            qtc = []  # quantidades de cartas por cor
            for cor in cores:
                qtc.append(len([c for c in jogadores[vez] if c['cor'] == cor]))
            carta['cor'] = cores[qtc.index(max(qtc))]
    for n in (2, 4):
        if carta['valor'] == f'+{n}':
            return ordem[ordem.index(vez) - (qtd - 1)], cartas_compra + n
    if carta['valor'] == 'X':
        return ordem[ordem.index(vez) - (qtd - 2)], 0
    if carta['valor'] == '>':
        ordem.reverse()
        sentido.reverse()
    return ordem[ordem.index(vez) - (qtd - 1)], 0


def jogada(jogador):
    """
    realiza a jogada de cada jogador

    :param jogador: jogador que irá jogar (int)
    :return: próximo a jogar e quantidade de cartas para compra (tuple)
    """
    prox = ordem[ordem.index(jogador) - (qtd - 1)]
    for n in ('+2', '+4'):
        cond1 = mesa[-1]['valor'] == n
        cond2 = cartas_compra > 0
        cond3 = not any([c['valor'] == n for c in jogadores[jogador]])
        if cond1 and cond2 and cond3:
            print(f'mais {cartas_compra} cartas!')
            compra(jogador, cartas_compra)
            sleep(2)
            return prox, 0
    if jogador == 0:
        n = len(jogadores[0])
        inst1 = 'digite a posição da carta que você quer jogar'
        intervalo = f' (1 a {n}) ' if n > 1 else ' '
        inst2 = 'ou "+" para comprar uma carta: '
        while True:
            comando = input(inst1 + intervalo + inst2).strip()
            if comando.isnumeric():
                comando = int(comando)
                if comando in range(1, n + 1):
                    c = jogadores[0][comando - 1]
                    if analisa_jogada(c):
                        mesa.append(c)
                        jogadores[0].remove(c)
                        return executa(c)
                    print('carta inválida')
                else:
                    print('posição inválida')
            elif comando == '+':
                if cartas_compra == 0:
                    compra(0, 1)
                    if analisa_jogada(jogadores[0][-1]):
                        mesa.append(jogadores[0].pop())
                        print(f'carta comprada e jogada ({mostra()})')
                        sleep(2)
                        return executa(mesa[-1])
                    print('carta comprada')
                    sleep(2)
                else:
                    compra(0, cartas_compra)
                    print(f'mais {cartas_compra} cartas!')
                    sleep(2)
                return prox, 0
            else:
                print('comando inválido')
    prioridades = []
    for c in jogadores[jogador]:
        if c['cor'] == 'preto':
            prioridades.append(c)
        else:
            prioridades.insert(0, c)
    for c in prioridades:
        if analisa_jogada(c):
            mesa.append(c)
            jogadores[jogador].remove(c)
            aux = executa(c)
            print(f'carta jogada ({mostra()})')
            sleep(2)
            return aux
    compra(jogador, 1)
    if analisa_jogada(jogadores[jogador][-1]):
        mesa.append(jogadores[jogador].pop())
        aux = executa(mesa[-1])
        print(f'carta comprada e jogada ({mostra()})')
        sleep(2)
        return aux
    print('carta comprada')
    sleep(2)
    return prox, 0


while True:
    limpa_tela()
    b = []
    cores = 'vermelho', 'verde', 'amarelo', 'azul'
    for cor in cores:
        for v in range(10):
            x = 1 if v == 0 else 2
            for _ in range(x):
                b.append({'cor': cor, 'valor': str(v), 'id': len(b) + 1})
        for v in ('X', '>', '+2'):
            for _ in range(2):
                b.append({'cor': cor, 'valor': v, 'id': len(b) + 1})
        for v in ('C', '+4'):
            b.append({'cor': 'preto', 'valor': v, 'id': len(b) + 1})
    d_cores = {cores[i]: f'\033[3{i + 1}m' for i in range(4)}
    d_cores['preto'] = '\033[0m'
    while True:
        qtd = input('informe o número de jogadores (2 a 10): ')
        if qtd.isnumeric() and int(qtd) in range(2, 11):
            qtd = int(qtd)
            break
        print('entrada inválida')
    jogadores = {x: [] for x in range(qtd)}
    ordem = list(jogadores.keys())
    mesa = []
    sentido = ['>', '<']
    shuffle(b)
    for jogador in jogadores.values():
        for _ in range(7):
            jogador.append(b.pop())
    while True:
        topo = choice(b)
        if topo['valor'].isnumeric():
            b.remove(topo)
            mesa.append(topo)
            break
    vez = choice(ordem)
    cartas_compra = 0
    while True:
        if len(b) <= 5 or cartas_compra >= len(b):
            b.extend(mesa[:-1])
            shuffle(b)
            mesa = [mesa[-1]]
        cenario()
        venceu = [len(jogadores[j]) == 0 for j in jogadores.keys()]
        if any(venceu):
            vencedor = venceu.index(True)
            break
        if vez:
            print(f'vez do jogador {vez}')
        else:
            print('sua vez')
        vez, cartas_compra = jogada(vez)
    print(f'{"você" if vencedor == 0 else f"jogador {vencedor}"} venceu')
    comando = input('digite "s" para sair ou outro comando para reiniciar: ')
    if comando.strip().lower() == 's':
        break
