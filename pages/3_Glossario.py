import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from utils.glossario import GLOSSARIO
from esconder_selo import esconder_selo_streamlit

st.set_page_config(page_title="Glossário", page_icon="📚", layout="wide")
esconder_selo_streamlit()  # oculta os controles do Streamlit Cloud
st.title("📚 Glossário de Consórcios")
st.write("Os termos que toda administradora usa — explicados sem economês.")

categorias = sorted(set(item["categoria"] for item in GLOSSARIO))
filtro = st.multiselect("Filtrar por categoria", categorias, default=categorias)

busca = st.text_input("🔍 Buscar termo", "")

itens_filtrados = [
    item for item in GLOSSARIO
    if item["categoria"] in filtro
    and (busca.lower() in item["termo"].lower() or busca == "")
]

if not itens_filtrados:
    st.warning("Nenhum termo encontrado com esse filtro/busca.")

for item in itens_filtrados:
    with st.expander(f"**{item['termo']}**  ·  _{item['categoria']}_"):
        st.write(item["explicacao"])
        st.success(f"💡 **Dica prática:** {item['dica']}")
