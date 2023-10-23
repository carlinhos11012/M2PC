import sys
import streamlit as st
import Backend as bd
import json

# Obter a lista a partir do argumento passado
lista_json = sys.argv[1]

# Converter a string JSON de volta para uma lista de dicionários
cirurgioes = json.loads(lista_json)

st.markdown("<h1 style='text-align: center; color: white;'>Resultados da Avaliação do Agendamento</h1>", unsafe_allow_html=True)


def imprimir_resultado(cirurgiao, procedimento, area_atuacao, duracao, anestesista, duracao_anestesia):
    (
        duracao_procedimento1,
        duracao_procedimento2,
        contar_realizacoes,
        media_duracao_por_classificacao,
        contagem_tratamento_por_sala,
        estatisticas_procedimento_por_complexidade1,
        estatisticas_procedimento_por_complexidade2,
        duracao_anestesia,
        contar_realizacoes_anestesia,
        resultado_media_duracao_por_classificacao_anestesia1,
        resultado_media_duracao_por_classificacao_anestesia2,
        contagem_tratamento_por_sala_anestesia1,
        contagem_tratamento_por_sala_anestesia2,
        estatisticas_procedimento_por_complexidade_anestesia1,
        estatisticas_procedimento_por_complexidade_anestesia2
    ) \
        = (
        bd.processo(cirurgiao, procedimento, area_atuacao, duracao, anestesista, duracao_anestesia))

    st.markdown("<h1 style='text-align: center; color: #add8e6;'>Informações Sobre o tipo do Procedimento</h1>", unsafe_allow_html=True)
    st.write(f'A duração {duracao} minutos do procedimento {procedimento} é {duracao_procedimento1} que a média {duracao_procedimento2} minutos.')
    st.write(contar_realizacoes)
    st.pyplot(media_duracao_por_classificacao)
    st.pyplot(contagem_tratamento_por_sala)
    st.write(estatisticas_procedimento_por_complexidade1)
    st.write(estatisticas_procedimento_por_complexidade2)

    st.markdown("<h1 style='text-align: center; color: #add8e6;'>Informações Sobre a Anestesia</h1>", unsafe_allow_html=True)

    st.write(duracao_anestesia)
    st.write(contar_realizacoes_anestesia)
    st.write(resultado_media_duracao_por_classificacao_anestesia1)
    st.write(resultado_media_duracao_por_classificacao_anestesia2)
    st.write(contagem_tratamento_por_sala_anestesia1)
    st.write(contagem_tratamento_por_sala_anestesia2)
    st.write(estatisticas_procedimento_por_complexidade_anestesia1)
    st.write(estatisticas_procedimento_por_complexidade_anestesia2)


x = 0
for i in cirurgioes:
    resultado = bd.verifica(i.get("Area de atuação"), i.get("Procedimento"), i.get("Duração"), i.get("Duração da anestesia"))
    if resultado == "MENOR":
        with st.expander(f"Processo n°{x + 1} | {i.get('Procedimento')} | {'⚠️'} Tempo Insuficiente"):
            imprimir_resultado(
                i.get("Cirurgiao"),
                i.get("Procedimento"),
                i.get("Area de atuação"),
                i.get("Duração"),
                i.get("Anestesista"),
                i.get("Duração da anestesia")
            )
    else:
        with st.expander(f"Processo n°{x + 1} | {i.get('Procedimento')}"):
            imprimir_resultado(
                i.get("Cirurgiao"),
                i.get("Procedimento"),
                i.get("Area de atuação"),
                i.get("Duração"),
                i.get("Anestesista"),
                i.get("Duração da anestesia")
            )
    x += 1
