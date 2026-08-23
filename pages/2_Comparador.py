import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd

from utils.calculos import (
    ParametrosConsorcio, parcela_consorcio_pre_contemplacao,
    ParametrosFinanciamento, simular_financiamento,
    simular_poupanca_programada,
)

st.set_page_config(page_title="Comparador", page_icon="⚖️", layout="wide")
st.title("⚖️ Consórcio vs. Financiamento vs. Poupança Programada")
st.write("Compare os três caminhos mais comuns para adquirir um bem de alto valor.")

with st.sidebar:
    st.header("Dados do bem")
    valor_bem = st.number_input("Valor do bem", min_value=1000.0, value=100000.0, step=1000.0)
    prazo_meses = st.slider("Prazo (meses)", 12, 240, 120, 6)

    st.markdown("---")
    st.subheader("Consórcio")
    taxa_administracao = st.slider("Taxa de administração total (%)", 0.0, 30.0, 18.0, 0.5)
    fundo_reserva = st.slider("Fundo de reserva total (%)", 0.0, 10.0, 2.0, 0.5)
    seguro_mensal = st.slider("Seguro mensal (% sobre saldo)", 0.0, 0.5, 0.05, 0.01)

    st.markdown("---")
    st.subheader("Financiamento")
    entrada_perc = st.slider("Entrada (%)", 0.0, 50.0, 20.0, 1.0)
    juros_mensal = st.slider("Juros do financiamento (% a.m.)", 0.0, 3.0, 1.3, 0.05)

    st.markdown("---")
    st.subheader("Poupança programada")
    rendimento_mensal = st.slider("Rendimento do investimento (% a.m.)", 0.0, 2.0, 0.7, 0.05,
                                   help="Ex: 0,7% a.m. ~ próximo de CDI/poupança conservadora")

# --- Cálculos ---
params_consorcio = ParametrosConsorcio(
    valor_bem=valor_bem, prazo_meses=prazo_meses,
    taxa_administracao_total=taxa_administracao,
    fundo_reserva_total=fundo_reserva,
    seguro_mensal_perc=seguro_mensal,
)
r_consorcio = parcela_consorcio_pre_contemplacao(params_consorcio)

params_financ = ParametrosFinanciamento(
    valor_bem=valor_bem, entrada_perc=entrada_perc,
    prazo_meses=prazo_meses, taxa_juros_mensal=juros_mensal,
)
r_financ = simular_financiamento(params_financ)

r_poupanca = simular_poupanca_programada(valor_bem, prazo_meses, rendimento_mensal)

# --- Tabela comparativa ---
st.subheader("Comparativo geral")

comparativo = pd.DataFrame([
    {
        "Modalidade": "🎯 Consórcio",
        "Parcela mensal (R$)": round(r_consorcio["parcela_media_total"], 2),
        "Total pago (R$)": round(r_consorcio["custo_total_plano"], 2),
        "Custo extra sobre o bem (%)": round(r_consorcio["custo_efetivo_total_perc"], 2),
        "Recebe o bem": "Só após contemplação (sorteio ou lance)",
    },
    {
        "Modalidade": "🏦 Financiamento",
        "Parcela mensal (R$)": round(r_financ["parcela_mensal"], 2),
        "Total pago (R$)": round(r_financ["total_pago_periodo"], 2),
        "Custo extra sobre o bem (%)": round(r_financ["custo_efetivo_total_perc"], 2),
        "Recebe o bem": "Imediatamente (na contratação)",
    },
    {
        "Modalidade": "💰 Poupança programada",
        "Parcela mensal (R$)": round(r_poupanca["aporte_mensal"], 2),
        "Total pago (R$)": round(r_poupanca["total_aportado"], 2),
        "Custo extra sobre o bem (%)": round(-(r_poupanca["rendimento_total_obtido"] / valor_bem) * 100, 2),
        "Recebe o bem": "Somente ao final do prazo",
    },
])

st.dataframe(comparativo, use_container_width=True, hide_index=True)

st.caption(
    "No caso da poupança programada, o 'custo extra' é **negativo** porque o rendimento reduz "
    "o quanto você precisa desembolsar no total — é a única modalidade em que o dinheiro trabalha a seu favor."
)

st.divider()

# --- Gráfico comparativo de parcelas ---
st.subheader("Parcela mensal lado a lado")
grafico_df = pd.DataFrame({
    "Modalidade": ["Consórcio", "Financiamento", "Poupança programada"],
    "Parcela mensal (R$)": [
        r_consorcio["parcela_media_total"],
        r_financ["parcela_mensal"],
        r_poupanca["aporte_mensal"],
    ],
})
st.bar_chart(grafico_df.set_index("Modalidade"))

st.divider()

st.markdown("""
### 🧠 Como interpretar isso

- **Consórcio**: geralmente tem a **menor parcela mensal**, mas você só recebe o bem quando é
  contemplado (sorteio ou lance) — pode ser no mês 1 ou só perto do fim do plano.
- **Financiamento**: você recebe o bem **na hora**, mas paga juros sobre o saldo devedor todo mês,
  o que costuma gerar o **maior custo total**.
- **Poupança programada**: exige disciplina e não garante o bem em uma data certa (depende do seu
  próprio ritmo de aporte), mas é o único caminho em que você **não paga por crédito de terceiros**.
""")

st.info(
    "⚠️ Esta comparação usa fórmulas simplificadas para fins didáticos. Taxas reais de mercado, "
    "reajustes anuais, impostos e condições específicas de cada instituição podem alterar "
    "significativamente esses números."
)
