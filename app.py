import streamlit as st
import model
from materiais import PAPEIS, TINTAS, TECIDOS
import json
import pandas as pd

ESTOQUE_FILE = "db.json"


def carregar_estoque():
    try:
        with open(ESTOQUE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def salvar_estoque(estoque):
    with open(ESTOQUE_FILE, "w") as f:
        json.dump(estoque, f, indent=4)


estoque = carregar_estoque()
st.title("📦 Controle de Estoque")

# Criar abas para cada tipo de material
abas = st.tabs(["📜 Papéis", "🎨 Tintas", "🧵 Tecidos"])

# Criar dataframes separados para cada categoria
df_papel = pd.DataFrame(estoque.get("papeis", []))
df_tinta = pd.DataFrame(estoque.get("tintas", []))
df_tecido = pd.DataFrame(estoque.get("tecidos", []))

# Aba de Papéis
with abas[0]:
    st.subheader("📜 Estoque de Papéis")
    if not df_papel.empty:
        st.table(df_papel)
    else:
        st.warning("Ainda não há papéis no estoque.")

# Aba de Tintas
with abas[1]:
    st.subheader("🎨 Estoque de Tintas")
    if not df_papel.empty:
        st.table(df_tinta)
    else:
        st.warning("Ainda não há tintas no estoque.")

# Aba de Tecidos
with abas[2]:
    st.subheader("🧵 Estoque de Tecidos")
    if not df_papel.empty:
        st.table(df_tecido)
    else:
        st.warning("Ainda não há tecidos no estoque.")

# Barra lateral para adicionar produto
with st.sidebar:
    st.subheader("Adicionar Produto")
    categoria = st.selectbox("Categoria do Produto", [
                             "Papel", "Tinta", "Tecido"])

    if categoria == "Papel":
        nome = st.selectbox("Tipo do Papel", PAPEIS)
        qtd_unit = st.number_input("Quantidade de rolos:", step=1, min_value=1)
        qtd_rolo = st.number_input("Metros Por Rolo", min_value=50, step=50)
        d = {"name": nome, "quantity": qtd_unit, "metros": qtd_rolo*qtd_unit}

    elif categoria == "Tinta":
        cor = st.selectbox("Cor da Tinta:", TINTAS)
        tipo = st.selectbox("Tipo da Tinta:", ("Sublimação", "Solvente"))
        qtd_litro = st.number_input(
            "Quantidade por litro:", step=1, min_value=1)
        qtd_unit = st.number_input(
            "Quantidade de litros:", min_value=1, step=1)
        d = {"color": cor, "quantity": qtd_unit,
            "type": tipo, "litros_total": qtd_litro*qtd_unit}

    elif categoria == "Tecido":
        nome = st.selectbox("Nome do Tecido", TECIDOS)
        qtd_metro = st.number_input("Quantiade de metros", step=1, min_value=1)
        qtd_unit = st.number_input("Quantidade de rolos:", min_value=1, step=1)
        d = {"name": nome, "quantity": qtd_unit, "metros": qtd_metro*qtd_unit}

    if st.button("Adicionar Produto"):
        if categoria == "Papel":
            if model.insert_papel(d) is not None:
                st.success(f"Produto {d['name']} cadastro com sucesso!")     
            else:
                st.warning("Erro ao salvo o produto!")
                
                
        if categoria == "Tinta":
            if model.insert_tinta(d) is not None:
                st.success(f"Produto {d['color']} cadastro com sucesso!")     
            else:
                st.warning("Erro ao salvo o produto!")
        if categoria == "Tecido":
            if model.insert_tecido(d) is not None:
                st.success(f"Produto {d['name']} cadastro com sucesso!")     
            else:
                st.warning("Erro ao salvo o produto!")

            

# Home com gráficos
