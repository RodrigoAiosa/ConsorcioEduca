import streamlit as st
from esconder_selo import esconder_selo_streamlit

st.set_page_config(
    page_title="Consórcio Educa | Simulador e Educação Financeira",
    page_icon="🧭",
    layout="wide",
)
esconder_selo_streamlit()  # oculta os controles do Streamlit Cloud

st.title("🧭 Consórcio Educa")
st.subheader("Simulação e educação financeira para quem tem (ou pensa em ter) um consórcio")

st.markdown("""
A maioria das pessoas entra em um consórcio sem entender de verdade **quanto vai pagar no total**,
**como funciona a contemplação** ou **o que aconteceria se tivesse escolhido outro caminho**
(financiamento, poupança programada). Esse projeto existe para preencher essa lacuna.

### O que você pode fazer aqui:
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 📊 Simulador de Consórcio")
    st.write(
        "Informe valor do bem, prazo, taxa de administração, fundo de reserva e seguro, "
        "e veja a parcela estimada, o custo efetivo total (CET) e a evolução mês a mês."
    )
    st.page_link("pages/1_Simulador.py", label="Ir para o Simulador →", icon="📊")

with col2:
    st.markdown("#### ⚖️ Comparador")
    st.write(
        "Compare o consórcio lado a lado com um financiamento tradicional e com uma "
        "poupança programada (aporte mensal rendendo juros) para o mesmo bem."
    )
    st.page_link("pages/2_Comparador.py", label="Ir para o Comparador →", icon="⚖️")

with col3:
    st.markdown("#### 📚 Glossário")
    st.write(
        "Entenda os termos que as administradoras usam — taxa de administração, lance "
        "embutido, fundo de reserva, CET — sem economês."
    )
    st.page_link("pages/3_Glossario.py", label="Ir para o Glossário →", icon="📚")

st.divider()

col4, col5 = st.columns(2)

with col4:
    st.markdown("#### 🎯 Simulador de Contemplação")
    st.write(
        "Explore de forma didática como a probabilidade de ser sorteado muda ao longo do "
        "prazo do grupo, e o impacto de dar um lance."
    )
    st.page_link("pages/4_Contemplacao.py", label="Ir para o Simulador de Contemplação →", icon="🎯")

with col5:
    st.markdown("#### 🏢 Comparar Administradoras")
    st.write(
        "Importe um CSV com condições de diferentes administradoras (ou propostas que você "
        "já recebeu) e compare parcela, custo total e CET lado a lado."
    )
    st.page_link("pages/5_Comparar_Administradoras.py", label="Ir para o Comparador de Administradoras →", icon="🏢")

st.divider()

st.info(
    "⚠️ **Aviso importante**: este projeto tem finalidade **educativa**. As fórmulas usadas são "
    "simplificações didáticas baseadas em práticas comuns do mercado, mas **cada administradora "
    "tem seu próprio regulamento**. Sempre confira o contrato e o CET oficial antes de decidir. "
    "Este app não é consultoria financeira."
)

st.caption("Projeto open-source · Feito com Python + Streamlit")
