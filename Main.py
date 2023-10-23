import streamlit as st
import Backend as bd
import subprocess
import json

# Inicialize a lista cirurgioes na sessão (se ainda não estiver definida)
if 'cirurgioes' not in st.session_state:
    st.session_state.cirurgioes = []

# Função para adicionar cirurgiões à lista
def adicionar_cirurgiao(cirurgiao, procedimento, area_atuacao, duracao, anestesista, duracao_anestesia):
    cirurgioes = st.session_state.cirurgioes
    cirurgioes.append({
        "Cirurgiao": cirurgiao,
        "Procedimento": procedimento,
        "Area de atuação": area_atuacao,
        "Duração": duracao,
        "Anestesista": anestesista,
        "Duração da anestesia": duracao_anestesia
    })

def imprimir_resultado(duracao_procedimento, duracao_anestesia):
    st.subheader(f"Tempo estimado da duração desse procedimento")
    st.write(duracao_procedimento)
    st.subheader(f"Tempo estimado da duração da anestesia")
    st.write(duracao_anestesia)

# Página principal do Streamlit
st.markdown("<h1 style='text-align: center; color: white;'>Sistema de Monitoramento Preditivo de Processos</h1>", unsafe_allow_html=True)

st.header("Cadastro do Agendamento")

cirurgiao = st.selectbox(
    "Nome do Cirurgião:",
    bd.retorna_cirurgioes()
)
procedimento = st.selectbox(
    "Procedimento:",
    bd.retorna_procedimentos()
)
area_atuacao = st.selectbox(
    "Área de Atuação:",
    ('-','Joelho', 'Mão', 'Pé/Tornozelo', 'Quadril')
)
anestesista = st.selectbox(
    "Nome do Anestesista:",
    [] + bd.retorna_anestesistas()
)
duracao_anestesia = st.number_input("Duração estimada da aplicação da anestesia (Em minutos)", min_value=0)
duracao = st.number_input("Duração estimada da cirurgia (Em minutos)", min_value=0)

# Botões para adicionar um cirurgião ou ver resultados
if st.button("Adicionar Processo"):
    if cirurgiao != '-' and procedimento != '-' and area_atuacao != '-' and anestesista != '-':
        adicionar_cirurgiao(cirurgiao, procedimento, area_atuacao, duracao, anestesista, duracao_anestesia)
        st.success("Cirurgião adicionado com sucesso!")
        st.header("Último Processo Cadastrado:")
        st.table(st.session_state.cirurgioes[-1])
    else:
        st.warning("Você deve preencher todos os dados.")

# Renderize a tabela apenas se houver cirurgiões cadastrados
if st.session_state.cirurgioes:
    st.subheader("Todos os Processos")
    st.table(st.session_state.cirurgioes)




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



if st.button("Realizar Análise do Agendamento"):
    st.markdown("<h1 style='text-align: center; color: white;'>Resultados da Avaliação do Agendamento</h1>", unsafe_allow_html=True)
    x = 0
    for i in st.session_state.cirurgioes:
        resultado = bd.verifica(i.get("Area de atuação"), i.get("Procedimento"), i.get("Duração"),
                                i.get("Duração da anestesia"))
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

st.write("Desenvolvido por Carlos Santos e Manoel Bina")
