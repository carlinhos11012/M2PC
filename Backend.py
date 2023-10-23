import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patheffects as pe

joelho_db = pd.read_excel("DB/datasets/dataset_joelho_cir_trein.xlsx")
mao_db = pd.read_excel("DB/datasets/dataset_mao_cir_trein.xlsx")
quadril_db = pd.read_excel("DB/datasets/dataset_quadril_cir_trein.xlsx")
pe_torn_db = pd.read_excel("DB/datasets/dataset_pe_tor_cir_trein.xlsx")

def contar_realizacoes(dataframe, cirurgiao, procedimento):
    filtro = (dataframe['CIRURGIAO'] == cirurgiao) & (dataframe['PROCEDIMENTO'] == procedimento)
    quantidade = dataframe[filtro].shape[0]
    return f' O(a) cirurgião/cirurgiã {cirurgiao} realizou o procedimento {procedimento} {quantidade} vezes.'

def media_duracao_por_classificacao(dataframe, procedimento):
    filtro = dataframe['PROCEDIMENTO'] == procedimento
    procedimento_df = dataframe[filtro]

    media_por_classificacao = procedimento_df.groupby('CLASSIFICAÇÃO AGENDA')['DURACAO_CIRURGIA'].mean()

    fig, ax = plt.subplots(figsize=(10, 6))  # Crie uma figura e um subplot

    num_items = len(media_por_classificacao)
    color_map = plt.get_cmap('RdBu_r', num_items)

    bar_plot = sns.barplot(x=media_por_classificacao.index, y=media_por_classificacao.values, palette=color_map(np.linspace(0, 1, num_items)))

    # Adicione o valor da média dentro das barras
    for p in bar_plot.patches:
        ax.annotate(f'{p.get_height():.2f}',
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 9),
                    textcoords='offset points')

    ax.set_title(f'Média de tempo de duração do procedimento {procedimento} por classificação')
    ax.set_xlabel('Classificação Agenda')
    ax.set_ylabel('Duração Média (em minutos)')
    plt.xticks(rotation=45)  # rotaciona os rótulos do eixo x para melhor visualização
    fig.tight_layout()  # ajusta layout para evitar sobreposição de rótulos

    return fig  # Retorna a figura criada


def contagem_tratamento_por_sala(dataframe, procedimento):
    filtro = dataframe['PROCEDIMENTO'] == procedimento
    procedimento_df = dataframe[filtro]

    contagem_por_sala = procedimento_df['SALA'].value_counts()

    fig, ax = plt.subplots(figsize=(10, 6))

    labels = [f'{sala}' for sala, valor in contagem_por_sala.items()]

    colors = plt.cm.viridis(np.linspace(0, 1, len(contagem_por_sala)))

    patches, texts, autotexts = ax.pie(contagem_por_sala, labels=labels, colors=colors, autopct='%1.1f%%',
                                       startangle=90, shadow=True, explode=[0.1] * len(contagem_por_sala))

    for text, val in zip(texts, contagem_por_sala):
        text.set_color('black')
        text.set_size(10)
        text.set_text(f'{text.get_text()} ({val})')  # Adicionando os valores reais aos labels

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_size(10)
        autotext.set_path_effects([plt.matplotlib.patheffects.withStroke(linewidth=1, foreground='black'),
                                   plt.matplotlib.patheffects.Normal()])  # Adicionando contorno

    ax.set_title(f'Contagem de vezes que o tratamento {procedimento} foi realizado em cada sala')
    ax.set_ylabel('')
    fig.tight_layout()

    return fig

def estatisticas_procedimento_por_complexidade(procedimento, database):
    filtro = database['PROCEDIMENTO'] == procedimento
    procedimento_df = database[filtro]

    estatisticas = procedimento_df.groupby('COMPLEXIDADE').agg({'DURACAO_CIRURGIA': ['count', 'mean']})
    estatisticas.columns = ['CONTAGEM', 'MEDIA_DURACAO']

    return (
        f'Estatísticas para o procedimento {procedimento} por complexidade:',
        estatisticas
    )

def verificar_duracao_procedimento(dataframe, procedimento, duracao):
    filtro = dataframe['PROCEDIMENTO'] == procedimento
    procedimento_df = dataframe[filtro]

    media_duracao_procedimento = procedimento_df['DURACAO_CIRURGIA'].mean()

    if math.isnan(media_duracao_procedimento):
        return "MENOR", 0
    if duracao > media_duracao_procedimento:
        return "MAIOR", int(media_duracao_procedimento)
    elif duracao < media_duracao_procedimento:
        return "MENOR", int(media_duracao_procedimento)
    else:
        return "IGUAL", int(media_duracao_procedimento)

def contar_realizacoes_anestesia(dataframe, anestesista, procedimento):
    filtro = (dataframe['ANESTESISTA'] == anestesista) & (dataframe['PROCEDIMENTO'] == procedimento)
    quantidade = dataframe[filtro].shape[0]
    return f'O(a) anestesista {anestesista} realizou a anestesia para o procedimento {procedimento} {quantidade} vezes.'

def media_duracao_por_classificacao_anestesia(dataframe, procedimento):
    filtro = dataframe['PROCEDIMENTO'] == procedimento
    procedimento_df = dataframe[filtro]

    media_por_classificacao = procedimento_df.groupby('CLASSIFICAÇÃO AGENDA')['DURACAO_ANESTESIA'].mean()

    return f'Média de tempo de duração da anestesia para poder realizar {procedimento}:', media_por_classificacao

def contagem_tratamento_por_sala_anestesia(dataframe, procedimento):
    filtro = dataframe['PROCEDIMENTO'] == procedimento
    procedimento_df = dataframe[filtro]

    contagem_por_sala = procedimento_df['SALA'].value_counts()

    return (
        f'Contagem de vezes que a aplicação de anestesia para o {procedimento} foi realizado em cada sala:',
        contagem_por_sala
    )

def estatisticas_procedimento_por_complexidade_anestesia(procedimento, database):
    filtro = database['PROCEDIMENTO'] == procedimento
    procedimento_df = database[filtro]

    estatisticas = procedimento_df.groupby('COMPLEXIDADE').agg({'DURACAO_ANESTESIA': ['count', 'mean']})
    estatisticas.columns = ['CONTAGEM', 'MEDIA_DURACAO']

    return (
        f'Estatísticas para a anestesia {procedimento} por complexidade:',
        estatisticas
    )

def verificar_duracao_procedimento_anestesia(dataframe, procedimento, duracao):
    filtro = dataframe['PROCEDIMENTO'] == procedimento
    procedimento_df = dataframe[filtro]

    media_duracao_procedimento = procedimento_df['DURACAO_ANESTESIA'].mean()

    if duracao > media_duracao_procedimento:
        return f'A duração {duracao} minutos do tempo de anestesia para realizar {procedimento} é MAIOR que a média {int(media_duracao_procedimento)} minutos.'
    elif duracao < media_duracao_procedimento:
        return f'A duração {duracao} minutos do tempo de anestesia para realizar {procedimento} é MENOR que a média {int(media_duracao_procedimento)} minutos.'
    else:
        return f'A duração {duracao} minutos do tempo de anestesia para realizar {procedimento} é IGUAL à média {int(media_duracao_procedimento)} minutos.'

def retorna_cirurgioes():
    cirurgioes_joelho = list(joelho_db['CIRURGIAO'].unique())
    cirurgioes_mao = list(mao_db['CIRURGIAO'].unique())
    cirurgioes_quadril = list(quadril_db['CIRURGIAO'].unique())
    cirurgioes_pe_tornozelo = list(pe_torn_db['CIRURGIAO'].unique())

    todos_cirurgioes = cirurgioes_joelho + cirurgioes_mao + cirurgioes_quadril + cirurgioes_pe_tornozelo
    todos_cirurgioes = sorted(todos_cirurgioes)
    return ['-'] + todos_cirurgioes

def retorna_anestesistas():
    anestesistas_unicos = set()  # Conjunto para armazenar anestesistas únicos

    anestesistas_unicos.update(joelho_db['ANESTESISTA'].unique())
    anestesistas_unicos.update(mao_db['ANESTESISTA'].unique())
    anestesistas_unicos.update(quadril_db['ANESTESISTA'].unique())
    anestesistas_unicos.update(pe_torn_db['ANESTESISTA'].unique())

    todos_anestesistas = list(anestesistas_unicos)

    todos_anestesistas = [anestesista for anestesista in todos_anestesistas if isinstance(anestesista, str)]

    todos_anestesistas = sorted(todos_anestesistas)
    return ['-'] + todos_anestesistas

def retorna_procedimentos():
    procedimentos_unicos = set()  # Conjunto para armazenar procedimentos únicos

    procedimentos_unicos.update(joelho_db['PROCEDIMENTO'].unique())
    procedimentos_unicos.update(mao_db['PROCEDIMENTO'].unique())
    procedimentos_unicos.update(quadril_db['PROCEDIMENTO'].unique())
    procedimentos_unicos.update(pe_torn_db['PROCEDIMENTO'].unique())

    todos_procedimentos = list(procedimentos_unicos)

    todos_procedimentos = sorted(todos_procedimentos)

    return ['-'] + todos_procedimentos

def verifica(area_atuacao, procedimento, duracao, duracao_anestesia):
    if area_atuacao == 'Joelho':
        dataframe = joelho_db
    elif area_atuacao == 'Mão':
        dataframe = mao_db
    elif area_atuacao == 'Quadril':
        dataframe = quadril_db
    else:
        dataframe = pe_torn_db

    filtro = dataframe['PROCEDIMENTO'] == procedimento
    procedimento_df = dataframe[filtro]

    media_duracao_procedimento_anestesia = procedimento_df['DURACAO_ANESTESIA'].mean()
    media_duracao_procedimento = procedimento_df['DURACAO_CIRURGIA'].mean()


    if duracao < media_duracao_procedimento or duracao_anestesia < media_duracao_procedimento_anestesia:
        return "MENOR"
    return ""

def processo(cirurgiao, procedimento, area_atuacao, duracao_cirurgia, anestesista, duracao_anestesia):
    if area_atuacao == 'Joelho':
        area_atuacao = joelho_db
    elif area_atuacao == 'Mão':
        area_atuacao = mao_db
    elif area_atuacao == 'Quadril':
        area_atuacao = quadril_db
    elif area_atuacao == 'Pé/Tornozelo':
        area_atuacao = pe_torn_db

    (resultado_duracao_procedimento1,
     resultado_duracao_procedimento2) = verificar_duracao_procedimento(area_atuacao, procedimento, duracao_cirurgia)

    resultado_contar_realizacoes = contar_realizacoes(area_atuacao, cirurgiao, procedimento)

    resultado_media_duracao_por_classificacao = media_duracao_por_classificacao(area_atuacao, procedimento)

    resultado_contagem_tratamento_por_sala = contagem_tratamento_por_sala(area_atuacao, procedimento)

    (resultado_estatisticas_procedimento_por_complexidade1,
     resultado_estatisticas_procedimento_por_complexidade2) = estatisticas_procedimento_por_complexidade(procedimento,
                                                                                                      area_atuacao)
    # Funções para gerar informações sobre a anestesia
    resultado_duracao_anestesia = verificar_duracao_procedimento_anestesia(area_atuacao,
                                                                                               procedimento,
                                                                                               duracao_anestesia)
    resultado_contar_realizacoes_anestesia = contar_realizacoes_anestesia(area_atuacao, anestesista, procedimento)

    (resultado_media_duracao_por_classificacao_anestesia1,
     resultado_media_duracao_por_classificacao_anestesia2) = media_duracao_por_classificacao_anestesia(area_atuacao,
                                                                                                       procedimento)

    resultado_contagem_tratamento_por_sala_anestesia1, resultado_contagem_tratamento_por_sala_anestesia2 = contagem_tratamento_por_sala_anestesia(
        area_atuacao, procedimento)

    (resultado_estatisticas_procedimento_por_complexidade_anestesia1,
     resultado_estatisticas_procedimento_por_complexidade_anestesia2) = estatisticas_procedimento_por_complexidade_anestesia(
        procedimento, area_atuacao)

    return (
        resultado_duracao_procedimento1,
        resultado_duracao_procedimento2,
        resultado_contar_realizacoes,
        resultado_media_duracao_por_classificacao,
        resultado_contagem_tratamento_por_sala,
        resultado_estatisticas_procedimento_por_complexidade1,
        resultado_estatisticas_procedimento_por_complexidade2,
        resultado_duracao_anestesia,
        resultado_contar_realizacoes_anestesia,
        resultado_media_duracao_por_classificacao_anestesia1,
        resultado_media_duracao_por_classificacao_anestesia2,
        resultado_contagem_tratamento_por_sala_anestesia1,
        resultado_contagem_tratamento_por_sala_anestesia2,
        resultado_estatisticas_procedimento_por_complexidade_anestesia1,
        resultado_estatisticas_procedimento_por_complexidade_anestesia2
        )
