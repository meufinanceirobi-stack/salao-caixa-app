import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date

def get_conn():
    return sqlite3.connect('caixa.db', check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS movimentacoes
                 (data TEXT, tipo TEXT, descricao TEXT, valor REAL, profissional TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS config
                 (chave TEXT PRIMARY KEY, valor REAL)''')
    c.execute("INSERT OR IGNORE INTO config (chave, valor) VALUES ('taxa_comissao', 0.4)")
    conn.commit()
    conn.close()

init_db()  # Roda uma vez

def registrar(tipo, desc, valor, prof=""):
    conn = get_conn()
    data = datetime.now().isoformat()
    c = conn.cursor()
    c.execute("INSERT INTO movimentacoes VALUES (?, ?, ?, ?, ?)", (data, tipo, desc, valor, prof))
    conn.commit()
    conn.close()
    st.rerun()

def saldo_dia():
    conn = get_conn()
    hoje = date.today().isoformat()
    df = pd.read_sql_query(f"SELECT * FROM movimentacoes WHERE data LIKE '{hoje}%'", conn)
    conn.close()
    entradas = df[df['tipo']=='entrada']['valor'].sum() if not df.empty else 0
    saidas = df[df['tipo']=='saida']['valor'].sum() if not df.empty else 0
    return entradas - saidas, entradas, saidas

def comissoes():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT valor FROM config WHERE chave='taxa_comissao'")
    result = c.fetchone()
    conn.close()
    if result:
        taxa = result[0]
        conn2 = get_conn()
        hoje = date.today().isoformat()
        query = f"SELECT profissional, ROUND(SUM(valor * {taxa}), 2) as comissao FROM movimentacoes WHERE data LIKE '{hoje}%' AND profissional != '' AND tipo='entrada' GROUP BY profissional"
        df = pd.read_sql_query(query, conn2)
        conn2.close()
        return df
    return pd.DataFrame()

def update_taxa(nova_taxa):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE config SET valor=? WHERE chave='taxa_comissao'", (nova_taxa,))
    conn.commit()
    conn.close()

st.title("💰 Caixa Simples Salão")

if 'taxa' not in st.session_state:
    st.session_state.taxa = 0.4
taxa = st.slider("Taxa Comissão", 0.0, 1.0, st.session_state.taxa, key="taxa_slider")
if taxa != st.session_state.taxa:
    st.session_state.taxa = taxa
    update_taxa(taxa)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Entrada")
    desc = st.text_input("Serviço", key="entrada_desc")
    prof = st.text_input("Profissional", key="entrada_prof")
    val = st.number_input("Valor R$", 0.0, key="entrada_val")
    if st.button("➕ Registrar", key="entrada_btn"):
        if desc and val > 0:
            registrar("entrada", desc, val, prof)
            st.success("Registrado!")

with col2:
    st.subheader("📤 Saída")
    desc = st.text_input("Despesa", key="saida_desc")
    val = st.number_input("Valor R$", 0.0, key="saida_val")
    if st.button("➖ Registrar", key="saida_btn"):
        if desc and val > 0:
            registrar("saida", desc, val)
            st.success("Registrado!")

st.subheader("📊 Hoje")
saldo, ent, sai = saldo_dia()
col1m, col2m, col3m = st.columns(3)
col1m.metric("Saldo", f"R$ {saldo:.2f}")
col2m.metric("Entradas", f"R$ {ent:.2f}")
col3m.metric("Saídas", f"R$ {sai:.2f}")

com = comissoes()
if not com.empty:
    st.subheader("💼 Comissões")
    st.dataframe(com)

if st.button("📥 CSV Hoje", key="csv_btn"):
    conn = get_conn()
    hoje = date.today().isoformat()
    df = pd.read_sql_query(f"SELECT * FROM movimentacoes WHERE data LIKE '{hoje}%'", conn)
    conn.close()
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Baixar CSV", csv, f"caixa_{hoje}.csv", "text/csv")