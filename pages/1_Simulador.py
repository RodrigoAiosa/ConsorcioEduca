import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd

from utils.calculos import (
    ParametrosConsorcio, parcela_consorcio_pre_contemplacao, fluxo_mensal_consorcio, valor_lance,
    ParametrosReajuste, fluxo_mensal_consorcio_com_reajuste,
)
from utils.pdf_export import gerar_pdf_simulacao
from esconder_selo import esconder_selo_streamlit

st.set_page_config(page_title="Simulador de Consórcio", page_icon="📊", layout="wide")
esconder_selo_streamlit()  # oculta os controles do Streamlit Cloud
st.title("📊 Simulador de Consórcio")
st.write("Preencha os dados do plano para estimar parcelas, custos totais e o impacto de um lance.")

with st.sidebar:
    st.header("Parâmetros do plano")
    valor_bem = st.number_input("Valor do bem (crédito contratado)", min_value=1000.0, value=100000.0, step=1000.0, format="%.2f")
    prazo_meses = st.slider("Prazo do plano (meses)", min_value=12, max_value=240, value=120, step=6)
    taxa_administracao = st.slider("Taxa de administração total (% sobre o bem)", 0.0, 30.0, 18.0, 0.5,
                                    help="Percentual TOTAL cobrado ao longo de todo o plano, não mensal.")
    fundo_reserva = st.slider("Fundo de reserva total (% sobre o bem)", 0.0, 10.0, 2.0, 0.5)
    seguro_mensal = st.slider("Seguro prestamista (% ao mês sobre saldo devedor)", 0.0, 0.5, 0.05, 0.01)

    st.markdown("---")
    st.subheader("Lance (opcional)")
    lance_proprio = st.slider("Lance próprio (% do valor do bem, dinheiro do bolso)", 0.0, 50.0, 0.0, 1.0)
    lance_embutido = st.slider("Lance embutido (% do valor do bem, usa o próprio crédito)", 0.0, 30.0, 0.0, 1.0)

    st.markdown("---")
    st.subheader("Reajuste anual (INCC/IPCA)")
    aplicar_reajuste = st.checkbox("Aplicar reajuste anual do bem", value=False,
                                    help="Consórcios de imóvel costumam usar o INCC; veículos e outros bens, o IPCA ou outro índice contratual.")
    indice_anual = st.slider("Índice de reajuste anual (%)", 0.0, 15.0, 5.0, 0.5, disabled=not aplicar_reajuste)

params = ParametrosConsorcio(
    valor_bem=valor_bem,
    prazo_meses=prazo_meses,
    taxa_administracao_total=taxa_administracao,
    fundo_reserva_total=fundo_reserva,
    seguro_mensal_perc=seguro_mensal,
    lance_proprio_perc=lance_proprio,
    lance_embutido_perc=lance_embutido,
)

resultado = parcela_consorcio_pre_contemplacao(params)

st.subheader("Resumo do plano")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Parcela base estimada", f"R$ {resultado['parcela_base']:.2f}")
c2.metric("Parcela + seguro (média)", f"R$ {resultado['parcela_media_total']:.2f}")
c3.metric("Custo total do plano", f"R$ {resultado['custo_total_plano']:.2f}")
c4.metric("Custo Efetivo Total (CET)", f"{resultado['custo_efetivo_total_perc']:.2f}%",
          help="Quanto você paga A MAIS do que o valor do bem, em percentual.")

st.caption(
    f"Composição dos custos: R$ {resultado['custo_administracao']:.2f} de taxa de administração "
    f"+ R$ {resultado['custo_fundo_reserva']:.2f} de fundo de reserva "
    f"+ seguro médio de R$ {resultado['seguro_medio_mensal']:.2f}/mês."
)

if lance_proprio > 0 or lance_embutido > 0:
    st.subheader("Impacto do lance")
    lance_info = valor_lance(params)
    l1, l2, l3 = st.columns(3)
    l1.metric("Lance próprio (desembolso)", f"R$ {lance_info['lance_proprio_valor']:.2f}")
    l2.metric("Lance embutido (do próprio crédito)", f"R$ {lance_info['lance_embutido_valor']:.2f}")
    l3.metric("Crédito líquido após embutido", f"R$ {lance_info['credito_liquido_apos_embutido']:.2f}")
    st.caption(
        "⚠️ O lance embutido reduz o valor de crédito que você efetivamente recebe na contemplação, "
        "mesmo pagando as parcelas com base no valor cheio do bem."
    )

st.divider()
st.subheader("Evolução mês a mês")

if aplicar_reajuste and indice_anual > 0:
    reajuste_params = ParametrosReajuste(indice_anual_perc=indice_anual, mes_aplicacao=12)
    fluxo = fluxo_mensal_consorcio_com_reajuste(params, reajuste_params)
    st.caption(
        f"📈 Reajuste de {indice_anual:.1f}% ao ano aplicado a cada 12 meses. "
        "Repare no 'salto' da parcela nos meses 13, 25, 37..."
    )
else:
    fluxo = fluxo_mensal_consorcio(params)

df = pd.DataFrame(fluxo)

tab1, tab2 = st.tabs(["📈 Gráfico", "📋 Tabela"])

with tab1:
    st.line_chart(df.set_index("mes")[["parcela_total", "saldo_devedor_estimado"]])

with tab2:
    colunas_renomeadas = {
        "mes": "Mês",
        "parcela_base": "Parcela base (R$)",
        "seguro": "Seguro (R$)",
        "parcela_total": "Parcela total (R$)",
        "saldo_devedor_estimado": "Saldo devedor estimado (R$)",
    }
    if "valor_bem_atualizado" in df.columns:
        colunas_renomeadas["valor_bem_atualizado"] = "Valor do bem atualizado (R$)"
    st.dataframe(
        df.rename(columns=colunas_renomeadas),
        use_container_width=True,
        hide_index=True,
    )

st.info(
    "💡 O saldo devedor aqui é uma **aproximação linear** para fins didáticos. Na prática, "
    "diluições por desistências e regras específicas de cada administradora também alteram esse valor."
)

st.divider()
st.subheader("📄 Exportar simulação")
st.write("Gere um PDF com o resumo desta simulação para guardar ou comparar depois.")

if st.button("Gerar PDF da simulação", type="primary"):
    pdf_bytes = gerar_pdf_simulacao(
        params=params,
        resultado=resultado,
        fluxo=fluxo,
        reajuste_aplicado=aplicar_reajuste and indice_anual > 0,
        indice_anual=indice_anual if (aplicar_reajuste and indice_anual > 0) else None,
        lance_proprio_perc=lance_proprio,
        lance_embutido_perc=lance_embutido,
    )
    st.download_button(
        label="⬇️ Baixar PDF",
        data=pdf_bytes,
        file_name="simulacao_consorcio.pdf",
        mime="application/pdf",
    )
