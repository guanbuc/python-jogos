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
        df = read_csv(local, delimiter=',', header=None)
        self.linhas = {}

        for index, row in df.iterrows():
            row = row.sort_values()
            self.linhas[f'{index}'] = []
            for i in range(0, 6):
                self.linhas[f'{index}'].append(int(row.iloc[i]) if not isna(row.iloc[i]) else None)

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
    with open('./outputPontosPorConcursoPorJogador.txt', 'w') as f:
        f.write(f'Concurso;Aposta;Pontos;Jogador;Números\n')
        for i in linhaSorteada:
            for j in linhaApostada:
                for lS in linhaSorteada[i]:
                    for lA in linhaApostada[j]:
                        if lS is not None:
                            if int(lS) == int(lA):
                                dezenas.append(int(lS))
                                pontos += 1

                Jogador = ''

                match int(j):
                    case x if x in [0,1,2,3,4,5,6,7,8,9]:
                        Jogador = ('Ricardo')
                    case x if x in [10,11,12,13,14,15,16,17,18,19]:
                        Jogador = ('Hugo')
                    case x if x in [20,21,22,23,24,25,26,27,28,29]:
                        Jogador = ('Sergio')
                    case x if x in [30,31,32,33,34,35,36,37,38,39]:
                        Jogador = ('Cleide')
                    case x if x in [40,41,42,43,44,45,46,47,48,49]:
                        Jogador = ('Helio')
                    case x if x in [50,51,52,53,54,55,56,57,58,59]:
                        Jogador = ('Luiz')
                    case x if x in [60,61,62,63,64,65,66,67,68,69]:
                        Jogador = ('Carolinda')
                    case x if x in [70,71,72,73,74,75,76,77,78,79]:
                        Jogador = ('Leticia')
                    case x if x in [80,81,82,83,84,85,86,87,88,89]:
                        Jogador = ('Vinicius')
                    case x if x in [90,91,92,93,94,95,96,97,98,99]:
                        Jogador = ('Michael')
                    case x if x >= 100:
                        Jogador = ('Sidnei')

                if pontos >= 2: # Só registrar apostas com 2 ou mais acertos, e vc pode parametrizar isso aqui
                    f.write(f'{(int(i))};{int(j) + 1};{pontos};{Jogador};{str(dezenas)}\n')

                pontos = 0
                dezenas = []


if __name__ == '__main__':
    EstatisticaPorBolaMega()
    EstatisticaPorVezesDeDezena()
    EstatisticaPorApostaJogador()