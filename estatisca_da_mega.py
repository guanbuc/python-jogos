# -*- encoding: utf-8 -*-

from pandas import *
import numpy as np


class EstatisticaMega:
    def __init__(self):
        self.numeros = []
        self.colunas = {}
        self.linhas = {}
        self.contagem = object

    def contCsv(self, local):
        df = read_csv(local, delimiter=',')

        for index, row in df.iterrows():
            print(row['jogador'])
            self.linhas[f'{row['jogador']}'] = []
            for i in range(1, 6):
                self.linhas[f'{row['jogador']}'].append(row[f'bola{i}'])

    def contXlsx(self, local):
        self.linhas = {}
        df = read_excel(local, engine='openpyxl')
        df = df.replace({np.nan: None})

        self.colunas = {}

        for i in range(1, 7):
            self.colunas[f'Bola{i}'] = dict(df[f'Bola{i}'].value_counts().sort_index())

        for index, row in df.iterrows():
            self.linhas[f'{row['Concurso']}'] = []
            for i in range(1, 7):
                self.linhas[f'{row['Concurso']}'].append(row[f'Bola{i}'])
                self.numeros.append(row[f'Bola{i}'])

        series = Series(self.numeros)

        self.contagem = series.value_counts().sort_index()



clsEstatisticaMega = EstatisticaMega()

def lerArquivoCsv(arquivo):
    clsEstatisticaMega.contCsv(arquivo)
    return clsEstatisticaMega.linhas

def lerArquivoXlsx(arquivo):
    clsEstatisticaMega.contXlsx(arquivo)
    return clsEstatisticaMega.linhas


def EstatisticaPorBolaMega():
    lerArquivoXlsx('./Mega-Sena.xlsx')

    with open('./outputEstatisticaPorBolaMega.txt', 'w') as f:
        f.write(f'bola;dezena;quantidade de vezes\n')

    with open('./outputEstatisticaPorBolaMega.txt', 'a') as f:
        for i in clsEstatisticaMega.colunas:
            for j in clsEstatisticaMega.colunas[i]:
                f.write(f'{i};{int(j)};{clsEstatisticaMega.colunas[i][j]}\n')

def EstatisticaPorVezesDeDezena():
    with open(f'./outputEstatisticaMega.txt', 'w') as f:
        f.write('Número;Quantidade de vezes sorteado\n')
        for numero, quantidade in clsEstatisticaMega.contagem.items():
            f.write(f'{numero:.0f};{quantidade:.0f}\n')

def EstatisticaPorApostaJogador():
    lerArquivoCsv('./jogos.csv')
    linhaApostada = clsEstatisticaMega.linhas

    lerArquivoXlsx('./Mega-Sena.xlsx')
    linhaSorteada = clsEstatisticaMega.linhas

    pontos = 0
    dezenas = []
    with open('./outputPontosPorConcurso.txt', 'w') as f:
        f.write(f'Concurso;Aposta;Pontos;Apostador;Números\n')
        for i in linhaSorteada:
            for j in linhaApostada:
                for lS in linhaSorteada[i]:
                    for lA in linhaApostada[j]:
                        if lS is not None:
                            if int(lS) == int(lA):
                                dezenas.append(int(lS))
                                pontos += 1

                apostador = ''
                match int(j):
                    case x if x in [0,1,2,3,4,5,6,7,8,9]:
                        apostador = ('Ricardo')
                    case x if x in [10,11,12,13,14,15,16,17,18,19]:
                        apostador = ('Hugo')
                    case x if x in [20,21,22,23,24,25,26,27,28,29]:
                        apostador = ('Sergio')
                    case x if x in [30,31,32,33,34,35,36,37,38,39]:
                        apostador = ('Cleide')
                    case x if x in [40,41,42,43,44,45,46,47,48,49]:
                        apostador = ('Helio')
                    case x if x in [50,51,52,53,54,55,56,57,58,59]:
                        apostador = ('Luiz')
                    case x if x in [60,61,62,63,64,65,66,67,68,69]:
                        apostador = ('Carolinda')
                    case x if x in [70,71,72,73,74,75,76,77,78,79]:
                        apostador = ('Leticia')
                    case x if x in [80,81,82,83,84,85,86,87,88,89]:
                        apostador = ('Vinicius')
                    case x if x in [90,91,92,93,94,95,96,97,98,99]:
                        apostador = ('Michael')
                    case x if x >= 100:
                        apostador = ('Sidnei')

                if pontos >= 2: # Só registrar apostas com 2 ou mais acertos, e vc pode parametrizar isso aqui
                    f.write(f'{(int(i) + 1)};{int(j) + 1};{pontos};{apostador};{str(dezenas)}\n')

                pontos = 0
                dezenas = []


if __name__ == '__main__':
    EstatisticaPorBolaMega()
    EstatisticaPorVezesDeDezena()
    lerArquivoCsv('./jogos.csv')
    #EstatisticaPorApostaJogador()