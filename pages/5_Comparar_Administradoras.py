import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import io
import streamlit as st
import pandas as pd

from utils.calculos import ParametrosConsorcio, parcela_consorcio_pre_contemplacao
from esconder_selo import esconder_selo_streamlit

st.set_page_config(page_title="Comparar Administradoras", page_icon="🏢", layout="wide")
esconder_selo_streamlit()  # oculta os controles do Streamlit Cloud
st.title("🏢 Comparar Administradoras (via CSV)")
st.write(
    "Importe uma planilha com as condições de diferentes administradoras (ou simulações que "
    "você já recebeu de vendedores) e compare parcela, custo total e CET lado a lado."
)

COLUNAS_OBRIGATORIAS = [
    "administradora", "taxa_administracao_total", "fundo_reserva_total",
    "seguro_mensal_perc", "prazo_meses",
]

# --- Template para download ---
template_df = pd.DataFrame([
    {"administradora": "Administradora A", "taxa_administracao_total": 18.0, "fundo_reserva_total": 2.0,
     "seguro_mensal_perc": 0.05, "prazo_meses": 120},
    {"administradora": "Administradora B", "taxa_administracao_total": 15.5, "fundo_reserva_total": 3.0,
     "seguro_mensal_perc": 0.04, "prazo_meses": 100},
    {"administradora": "Administradora C", "taxa_administracao_total": 21.0, "fundo_reserva_total": 1.5,
     "seguro_mensal_perc": 0.06, "prazo_meses": 140},
])

csv_buffer = io.StringIO()
template_df.to_csv(csv_buffer, index=False)

col_a, col_b = st.columns([2, 1])
with col_a:
    st.markdown("""
    **Formato esperado do CSV** (colunas obrigatórias):

    - `administradora` — nome/identificação
    - `taxa_administracao_total` — % total sobre o valor do bem
    - `fundo_reserva_total` — % total sobre o valor do bem
    - `seguro_mensal_perc` — % ao mês sobre o saldo devedor
    - `prazo_meses` — prazo do plano em meses
    """)
with col_b:
    st.download_button(
        "⬇️ Baixar modelo de CSV",
        data=csv_buffer.getvalue(),
        file_name="modelo_administradoras.csv",
        mime="text/csv",
    )

st.divider()

valor_bem = st.number_input("Valor do bem para a comparação (R$)", min_value=1000.0, value=100000.0, step=1000.0)

arquivo = st.file_uploader("📤 Envie o CSV das administradoras", type=["csv"])

if arquivo is not None:
    try:
        df_input = pd.read_csv(arquivo)
    except Exception as e:
        st.error(f"Não foi possível ler o CSV: {e}")
        st.stop()

    faltando = [c for c in COLUNAS_OBRIGATORIAS if c not in df_input.columns]
    if faltando:
        st.error(
            f"O CSV está com colunas faltando: **{', '.join(faltando)}**. "
            "Baixe o modelo acima para conferir o formato esperado."
        )
        st.stop()

    resultados = []
    for _, linha in df_input.iterrows():
        try:
            params = ParametrosConsorcio(
                valor_bem=valor_bem,
                prazo_meses=int(linha["prazo_meses"]),
                taxa_administracao_total=float(linha["taxa_administracao_total"]),
                fundo_reserva_total=float(linha["fundo_reserva_total"]),
                seguro_mensal_perc=float(linha["seguro_mensal_perc"]),
            )
            r = parcela_consorcio_pre_contemplacao(params)
            resultados.append({
                "Administradora": linha["administradora"],
                "Prazo (meses)": params.prazo_meses,
                "Taxa Adm. (%)": params.taxa_administracao_total,
                "Fundo Reserva (%)": params.fundo_reserva_total,
                "Parcela estimada (R$)": round(r["parcela_media_total"], 2),
                "Custo total (R$)": round(r["custo_total_plano"], 2),
                "CET (%)": round(r["custo_efetivo_total_perc"], 2),
            })
        except Exception as e:
            st.warning(f"Linha com problema ('{linha.get('administradora', '?')}'): {e}")

    if resultados:
        df_resultado = pd.DataFrame(resultados).sort_values("CET (%)")

        st.subheader("Resultado comparativo")
        st.dataframe(df_resultado, use_container_width=True, hide_index=True)

        melhor = df_resultado.iloc[0]
        st.success(
            f"🏆 Melhor CET encontrado: **{melhor['Administradora']}** com "
            f"{melhor['CET (%)']:.2f}% (parcela estimada de R$ {melhor['Parcela estimada (R$)']:,.2f})."
        )

        st.subheader("Parcela estimada por administradora")
        st.bar_chart(df_resultado.set_index("Administradora")["Parcela estimada (R$)"])

        st.subheader("CET por administradora")
        st.bar_chart(df_resultado.set_index("Administradora")["CET (%)"])

        st.info(
            "💡 Um CET mais baixo não significa necessariamente a melhor escolha: considere também "
            "o histórico de contemplações do grupo, reputação da administradora e flexibilidade de lance."
        )
else:
    st.caption("Nenhum arquivo enviado ainda. Baixe o modelo acima, preencha com os dados reais e envie aqui.")
