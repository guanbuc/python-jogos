# -*- encoding: utf-8 -*-
import pandas
import pandas as pd
import numpy as np
import csv

from pandas.core.interchange.dataframe_protocol import DataFrame


class EstatisticaMega:
    def __init__(self):
        self.df = DataFrame
        self.contagem = None
        self.porPeriodoMM = []
        self.porPeriodoMMYY = []
        self.porCombinacoesMM = []
        self.porCombinacoesMMYY = []
        self.numeros = []
        self.colunas = {}
        self.linhas = {}
        self.dezenas = {}
        self.combinacoes = {}

    def contCsv(self, local):
        # tenta utf-8 e faz fallback para latin-1 em caso de erro de decodificação
        try:
            df = pd.read_csv(local, delimiter=',', header=None,
                             names=['bola1', 'bola2', 'bola3', 'bola4', 'bola5', 'bola6'],
                             usecols=[0,1,2,3,4,5],
                             encoding='utf-8')

        except UnicodeDecodeError:
            df = pd.read_csv(local, delimiter=',', header=None,
                             names=['bola1', 'bola2', 'bola3', 'bola4', 'bola5', 'bola6'],
                             usecols=[0,1,2,3,4,5],
                             encoding='latin-1')

        except Exception:
            # último recurso: usar engine python e substituir erros
            df = pd.read_csv(local, delimiter=',', header=None, engine='python',
                             names=['bola1', 'bola2', 'bola3', 'bola4', 'bola5', 'bola6'],
                             usecols=[0,1,2,3,4,5],
                             encoding='utf-8', on_bad_lines='skip')

        self.linhas = {}

        for index, row in df.iterrows():
            row = row.sort_values()
            self.linhas[f'{index}'] = []
            for i in range(0, 6):
                self.linhas[f'{index}'].append(int(row.iloc[i]) if not pd.isna(row.iloc[i]) else None)

    def contXlsx(self, local):
        self.linhas = {}
        self.colunas = {}
        self.porCombinacoesMM = []
        self.porCombinacoesMMYY = []
        self.numeros = []
        self.porPeriodoMM = []
        self.porPeriodoMMYY = []

        self.df = pd.read_excel(local, engine='openpyxl')
        self.df = self.df.replace({np.nan: None})

        self.df['Data do Sorteio'] = pd.to_datetime(self.df['Data do Sorteio'], format='%d/%m/%Y', errors='coerce', dayfirst=True)
        self.df['mes_ano'] = self.df['Data do Sorteio'].dt.strftime('%m/%Y')
        self.df['mes'] = self.df['Data do Sorteio'].dt.strftime('%m')

        for i in range(1, 7):

            # Cria uma coluna de faixa para cada bola separadamente
            self.df[f'faixa_Bola{i}'] = pd.cut(self.df[f'Bola{i}'],
                                          bins=[0, 10, 20, 30, 40, 50, 60],
                                          labels=['1-10', '11-20', '21-30', '31-40', '41-50', '51-60'])

            self.colunas[f'Bola{i}'] = dict(self.df[f'Bola{i}'].value_counts().sort_index())
            self.dezenas[f'faixa_Bola{i}'] = dict(self.df[f'faixa_Bola{i}'].value_counts().sort_index())

            contMMYY = self.df.groupby(['mes_ano', f'faixa_Bola{i}'])[f'faixa_Bola{i}'].count().reset_index(name=f'count_faixa_bola{i}')
            contMM = self.df.groupby(['mes', f'faixa_Bola{i}'])[f'faixa_Bola{i}'].count().reset_index(name=f'count_faixa_bola{i}')

            contMMYY[f'count_faixa_bola{i}'] = contMMYY[f'count_faixa_bola{i}'].astype('Int64')
            contMM[f'count_faixa_bola{i}'] = contMM[f'count_faixa_bola{i}'].astype('Int64')

            self.porPeriodoMM.append(contMM)
            self.porPeriodoMMYY.append(contMMYY)

        # Concatenar as faixas em uma única coluna
        self.df['dezenas_combinadas'] = self.df[list(self.dezenas)].apply(lambda row: '|'.join(row.astype(str)), axis=1)

        # Use count() em vez de value_counts()
        contCombMMYY = self.df.groupby(['mes_ano', 'dezenas_combinadas'])['dezenas_combinadas'].count().reset_index(
            name='count_combinacao_MMYY')
        contCombMM = self.df.groupby(['mes', 'dezenas_combinadas'])['dezenas_combinadas'].count().reset_index(
            name='count_combinacao_MM')

        contCombMMYY['count_combinacao_MMYY'] = contCombMMYY['count_combinacao_MMYY'].astype('Int64')
        contCombMM['count_combinacao_MM'] = contCombMM['count_combinacao_MM'].astype('Int64')

        # Contar quantas vezes cada combinação aparece
        self.combinacoes['dezenas_combinadas'] = dict(self.df['dezenas_combinadas'].value_counts())

        self.porCombinacoesMMYY.append(contCombMMYY)
        self.porCombinacoesMM.append(contCombMM)

        for index, row in self.df.iterrows():
            self.linhas[f'{row['Concurso']}'] = []
            for i in range(1, 7):
                self.linhas[f'{row['Concurso']}'].append(row[f'Bola{i}'])
                self.numeros.append(row[f'Bola{i}'])

        series = pd.Series(self.numeros)

        self.contagem = series.value_counts().sort_index() if not series.empty else pd.Series(dtype='int64')


clsEstatisticaMega = EstatisticaMega()

def lerArquivoCsv(arquivo):
    clsEstatisticaMega.contCsv(arquivo)
    return clsEstatisticaMega.linhas

def lerArquivoXlsx(arquivo):
    clsEstatisticaMega.contXlsx(arquivo)
    return clsEstatisticaMega.linhas

def EstatisticaPorBolaMega():
    lerArquivoXlsx('./Mega-Sena.xlsx')

    with open('./outputEstatisticaPorBolaMega.csv', 'w', encoding='utf-8', errors='replace', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['bola', 'dezena', 'quantidade de vezes'])
        for i in clsEstatisticaMega.colunas:
            for j in clsEstatisticaMega.colunas[i]:
                writer.writerow([i, int(j), clsEstatisticaMega.colunas[i][j]])

def EstatisticaPorFaixaBolaMega():
    with open('./outputEstatisticaPorFaixaBolaMega.csv', 'w', encoding='utf-8', errors='replace', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['faixa_bola', 'dezena', 'quantidade de vezes'])
        for i in clsEstatisticaMega.dezenas:
            for j in clsEstatisticaMega.dezenas[i]:
                writer.writerow([i, j, clsEstatisticaMega.dezenas[i][j]])

def EstatisticaPorConjFaixaBolaMega():
    with open('./outputEstatisticaPorConjFaixaBolaMega.csv', 'w', encoding='utf-8', errors='replace', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['dezenas_combinadas', 'quantidade de vezes'])
        for i in clsEstatisticaMega.combinacoes:
            for j in clsEstatisticaMega.combinacoes[i]:
                writer.writerow([j, clsEstatisticaMega.combinacoes[i][j]])

def EstatisticaPorFaixaPeriodoMesAno():
    nwDf = pd.concat(clsEstatisticaMega.porPeriodoMMYY, ignore_index=True)

    #nwDf = nwDf.fillna(0).astype({col: int for col in nwDf.select_dtypes('float').columns})

    nwDf.to_csv('./outputEstatisticaPorFaixaPeriodoMesAno.csv', index=False, encoding='utf-8')

def EstatisticaPorConjFaixaPeriodoMesAno():
    nwDf = pd.concat(clsEstatisticaMega.porCombinacoesMMYY, ignore_index=True)

    #nwDf = nwDf.fillna(0).astype({col: int for col in nwDf.select_dtypes('float').columns})

    nwDf.to_csv('./outputEstatisticaPorConjFaixaPeriodoMesAno.csv', index=False, encoding='utf-8')

def EstatisticaPorFaixaPeriodoMes():
    nwDf = pd.concat(clsEstatisticaMega.porPeriodoMM, ignore_index=True)

    #nwDf = nwDf.fillna(0).astype({col: int for col in nwDf.select_dtypes('float').columns})

    nwDf.to_csv('./outputEstatisticaPorFaixaPeriodoMes.csv', index=False, encoding='utf-8')

def EstatisticaPorConjFaixaPeriodoMes():
    nwDf = pd.concat(clsEstatisticaMega.porCombinacoesMM, ignore_index=True)

    #nwDf = nwDf.fillna(0).astype({col: int for col in nwDf.select_dtypes('float').columns})

    nwDf.to_csv('./outputEstatisticaPorConjFaixaPeriodoMes.csv', index=False, encoding='utf-8')

def EstatisticaPorVezesDeDezena():
    with open('./outputEstatisticaMega.csv', 'w', encoding='utf-8', errors='replace', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Número', 'quantidade de vezes'])
        for numero, quantidade in clsEstatisticaMega.contagem.items():
            writer.writerow([f'{numero:.0f}', f'{quantidade:.0f}'])

def EstatisticaPorApostaJogador():
    lerArquivoCsv('./jogos.csv')
    linhaApostada = clsEstatisticaMega.linhas

    lerArquivoXlsx('./Mega-Sena.xlsx')
    linhaSorteada = clsEstatisticaMega.linhas

    pontos = 0
    dezenas = []
    with open('./outputPontosPorConcursoPorJogador.csv', 'w', encoding='utf-8', errors='replace', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Concurso', 'Aposta', 'Pontos', 'Jogador', 'Números'])
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

                if pontos >= 2: # Só registrar apostas com 2 ou mais acertos
                    writer.writerow([int(i), int(j) + 1 , pontos , Jogador , str(dezenas)])

                pontos = 0
                dezenas = []


if __name__ == '__main__':
    EstatisticaPorBolaMega()
    EstatisticaPorVezesDeDezena()
    EstatisticaPorApostaJogador()
    EstatisticaPorFaixaBolaMega()
    EstatisticaPorConjFaixaBolaMega()
    EstatisticaPorFaixaPeriodoMesAno()
    EstatisticaPorConjFaixaPeriodoMesAno()
    EstatisticaPorFaixaPeriodoMes()
    EstatisticaPorConjFaixaPeriodoMes()