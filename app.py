import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

# Arquivo para armazenar o estoque
ESTOQUE_FILE = "estoque.json"

# Função para carregar o estoque
def carregar_estoque():
    try:
        with open(ESTOQUE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Função para salvar o estoque
def salvar_estoque(estoque):
    with open(ESTOQUE_FILE, "w") as f:
        json.dump(estoque, f, indent=4)

# Carregar estoque ao iniciar
estoque = carregar_estoque()

st.title("📦 Controle de Estoque")

# Barra lateral para adicionar produto
with st.sidebar:
    st.subheader("Adicionar Produto")
    categoria = st.selectbox("Categoria do Produto", ["Papel", "Tinta", "Outros"])
    
    if categoria == "Papel":
        nome = st.text_input("Nome do Papel")
        gramatura = st.text_input("Gramatura (g/m²)")
        unidade = "metros"
        quantidade = st.number_input("Quantidade (metros)", min_value=0.0, step=0.1, format="%.2f")
    elif categoria == "Tinta":
        nome = st.text_input("Nome da Tinta")
        cor = st.text_input("Cor da Tinta")
        unidade = "litros"
        quantidade = st.number_input("Quantidade (litros)", min_value=0.0, step=0.1, format="%.2f")
    else:
        nome = st.text_input("Nome do Produto")
        unidade = st.text_input("Unidade de Medida (ex: unidades, metros, litros)")
        quantidade = st.number_input("Quantidade Inicial", min_value=0.0, step=0.1, format="%.2f")
    
    alerta = st.number_input("Nível de alerta", min_value=0.0, step=0.1, format="%.2f")
    
    if st.button("Adicionar Produto"):
        if nome:
            estoque[nome] = {"quantidade": quantidade, "unidade": unidade, "alerta": alerta, "categoria": categoria}
            salvar_estoque(estoque)
            st.success(f"{nome} adicionado com sucesso!")
            st.experimental_rerun()
        else:
            st.warning("Preencha todos os campos!")

# Home com gráficos
st.subheader("📊 Visão Geral do Estoque")
if estoque:
    df = pd.DataFrame.from_dict(estoque, orient="index")
    
    # Gráfico de barras do estoque
    fig, ax = plt.subplots()
    ax.bar(df.index, df["quantidade"], color='blue')
    ax.set_ylabel("Quantidade")
    ax.set_xlabel("Produtos")
    ax.set_title("Estoque Atual")
    plt.xticks(rotation=45, ha='right')
    
    st.pyplot(fig)
    st.dataframe(df)
else:
    st.info("Nenhum produto no estoque.")

# Registrar saída de produto
st.subheader("📉 Registrar Saída")
produto_selecionado = st.selectbox("Escolha o produto", list(estoque.keys()))
quantidade_saida = st.number_input("Quantidade a remover", min_value=0.0, step=0.1, format="%.2f")

if st.button("Registrar Saída"):
    if produto_selecionado in estoque:
        estoque[produto_selecionado]["quantidade"] -= quantidade_saida
        salvar_estoque(estoque)
        st.success(f"{quantidade_saida} {estoque[produto_selecionado]['unidade']} removidos de {produto_selecionado}.")
        st.experimental_rerun()

# Alertas de estoque baixo
st.subheader("⚠️ Alertas de Estoque Baixo")
alertas = {p: d for p, d in estoque.items() if d["quantidade"] <= d["alerta"]}
if alertas:
    for produto, dados in alertas.items():
        st.warning(f"{produto} está abaixo do nível de alerta! Restam {dados['quantidade']} {dados['unidade']}")
else:
    st.success("Todos os produtos estão acima do nível de alerta.")
