import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd

from utils.calculos import probabilidade_contemplacao_simples

st.set_page_config(page_title="Simulador de Contemplação", page_icon="🎯", layout="wide")
st.title("🎯 Simulador de Contemplação por Sorteio")
st.write(
    "Entenda, de forma didática, como a chance de ser sorteado muda ao longo do grupo. "
    "**Importante:** esta é uma estimativa simplificada para fins educativos, não a fórmula "
    "oficial de nenhuma administradora."
)

col1, col2 = st.columns(2)
with col1:
    num_participantes = st.number_input("Número de participantes no grupo", min_value=10, value=200, step=10)
with col2:
    num_contemplados_mes = st.number_input("Contemplados por sorteio a cada mês", min_value=1, value=2, step=1)

prazo_meses = st.slider("Prazo do grupo (meses)", 12, 240, 120, 6)

linhas = []
for mes in range(1, prazo_meses + 1):
    r = probabilidade_contemplacao_simples(num_participantes, num_contemplados_mes, mes, prazo_meses)
    linhas.append({
        "Mês": mes,
        "Participantes restantes (estimado)": r["participantes_restantes_estimado"],
        "Prob. de sorteio NESTE mês (%)": round(r["probabilidade_sorteio_no_mes"] * 100, 3),
        "Prob. acumulada de já ter sido sorteado (%)": round(r["probabilidade_acumulada_estimada"] * 100, 2),
    })

df = pd.DataFrame(linhas)

st.subheader("Como a probabilidade evolui")
st.line_chart(df.set_index("Mês")[["Prob. de sorteio NESTE mês (%)", "Prob. acumulada de já ter sido sorteado (%)"]])

with st.expander("📋 Ver tabela completa"):
    st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

st.markdown("""
### 🧠 O que isso significa na prática

- Quanto **mais participantes** no grupo, **menor** a chance individual de sorteio a cada mês.
- Quanto **mais contemplações por mês** o grupo oferece, **maior** a chance — mas isso geralmente
  está ligado ao tamanho das parcelas arrecadadas, não é "de graça".
- A **probabilidade acumulada** mostra a chance estimada de você já ter sido contemplado
  em algum momento até aquele mês, assumindo sorteio puro (sem lances disputando).
- **Lances** mudam completamente essa dinâmica: quem dá lance compete em uma "fila" separada
  do sorteio, e isso pode acelerar (ou não) a contemplação dependendo de quanto os outros
  participantes também estão ofertando.
""")

st.info(
    "⚠️ Grupos reais têm dinâmicas mais complexas: desistências, atrasos, entrada de novos "
    "participantes e regras específicas de cada administradora alteram esses números na prática."
)
