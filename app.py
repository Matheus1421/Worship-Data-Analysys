import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Ministério", layout="wide")

@st.cache_data
def carregar_dados():
    df_exec = pd.read_csv("DADOS_DASHBOARD_FINAL.csv")
    df_exec = df_exec.dropna(subset=['ID_MUSICA'])
    df_acervo = pd.read_csv("ADOLESCENTES - MUSICAS.csv")
    df_acervo = df_acervo.rename(columns={'ID_MÚSICA': 'ID_MUSICA'})
    
    def limpar_texto(df):
        cols_texto = ['MÚSICA', 'AUTOR_MUSICA', 'CLASSIFICACAO_MUSICA']
        for col in cols_texto:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.upper()
        return df

    df_exec = limpar_texto(df_exec)
    df_acervo = limpar_texto(df_acervo)
    
    return df_exec, df_acervo

df, df_acervo = carregar_dados()

st.sidebar.header("Filtros")

if "CLASSIFICACAO_MUSICA" in df_acervo.columns:
    lista_classificacao = df_acervo["CLASSIFICACAO_MUSICA"].dropna().unique()
    classificacao_selecionada = st.sidebar.multiselect(
        "Estilo musical:", 
        options=lista_classificacao, 
        default=lista_classificacao
    )
else:
    classificacao_selecionada = []

df_filtrado = df.copy()          
df_acervo_filtrado = df_acervo.copy() 

if classificacao_selecionada:
    df_filtrado = df_filtrado[df_filtrado["CLASSIFICACAO_MUSICA"].isin(classificacao_selecionada)]
    df_acervo_filtrado = df_acervo_filtrado[df_acervo_filtrado["CLASSIFICACAO_MUSICA"].isin(classificacao_selecionada)]

ids_tocados = set(df_filtrado["ID_MUSICA"].unique())       # Quem já tocou
ids_totais = set(df_acervo_filtrado["ID_MUSICA"].unique()) # Todos que existem
ids_nao_tocados = ids_totais - ids_tocados                 # A Diferença

df_fila = df_acervo_filtrado[df_acervo_filtrado["ID_MUSICA"].isin(ids_nao_tocados)]

st.title("📊 Dashboard de Execução Musical")
st.markdown("---")

# KPIs
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Execuções Totais", len(df_filtrado))
col2.metric("Músicas Diferentes Tocadas", len(ids_tocados))
col3.metric("Total no Acervo", len(df_acervo_filtrado))
col4.metric("Na Fila (Nunca Tocadas)", len(df_fila))

if len(ids_totais) > 0:
    giro = (len(ids_tocados) / len(ids_totais)) * 100
else:
    giro = 0
col5.metric("Giro do Repertório", f"{giro:.1f}%")

st.markdown("---")

aba1, aba2, aba3 = st.tabs(["🎵 Execução", "🎤 Artistas", "💡 Oportunidades (Fila)"])

with aba1:
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("Top 10 Músicas")
        if not df_filtrado.empty:
            df_top = df_filtrado["MÚSICA"].value_counts().reset_index().head(10)
            df_top.columns = ["Música", "Qtd"]
            fig_barras = px.bar(df_top, x="Qtd", y="Música", orientation='h', text="Qtd")
            fig_barras.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_barras, use_container_width=True)
    
    with col_g2:
        st.subheader("Estilos Executados")
        if "CLASSIFICACAO_MUSICA" in df_filtrado.columns and not df_filtrado.empty:
            fig_pizza = px.pie(df_filtrado, names="CLASSIFICACAO_MUSICA", hole=0.5)
            st.plotly_chart(fig_pizza, use_container_width=True)


with aba2:
    col_art1, col_art2 = st.columns(2)
    
    with col_art1:
        st.subheader("Mais Executados (Demanda)")
        if not df_filtrado.empty:
            df_art_exec = df_filtrado["AUTOR_MUSICA"].value_counts().reset_index().head(10)
            df_art_exec.columns = ["Artista", "Execuções"]
            # Cor Vermelha
            fig_exec = px.bar(df_art_exec, x="Execuções", y="Artista", orientation='h', text="Execuções", color_discrete_sequence=['#FF4B4B'])
            fig_exec.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_exec, use_container_width=True)
            
    with col_art2:
        st.subheader("Maiores no Acervo (Oferta)")
        df_art_acervo = df_acervo_filtrado["AUTOR_MUSICA"].value_counts().reset_index().head(10)
        df_art_acervo.columns = ["Artista", "Músicas"]
        # Cor Azul
        fig_acervo = px.bar(df_art_acervo, x="Músicas", y="Artista", orientation='h', text="Músicas", color_discrete_sequence=['#1E90FF'])
        fig_acervo.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_acervo, use_container_width=True)

with aba3:
    st.subheader(f"Raio-X da Fila: {len(df_fila)} músicas disponíveis")
    
    if not df_fila.empty:
        col_f1, col_f2 = st.columns(2)
        
        # Gráfico Artistas na Fila (Verde)
        with col_f1:
            st.markdown("##### 🎹 Artistas com mais músicas paradas")
            df_art_fila = df_fila["AUTOR_MUSICA"].value_counts().reset_index().head(10)
            df_art_fila.columns = ["Artista", "Qtd na Fila"]
            
            fig_art_fila = px.bar(
                df_art_fila, 
                x="Qtd na Fila", 
                y="Artista", 
                orientation='h', 
                text="Qtd na Fila", 
                color_discrete_sequence=['#00CC96'] # Verde
            )
            fig_art_fila.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_art_fila, use_container_width=True)

        with col_f2:
            st.markdown("##### 🎸 Estilos parados")
            if "CLASSIFICACAO_MUSICA" in df_fila.columns:
                fig_pizza_fila = px.pie(
                    df_fila, 
                    names="CLASSIFICACAO_MUSICA", 
                    hole=0.5,
                    color_discrete_sequence=px.colors.sequential.Teal
                )
                st.plotly_chart(fig_pizza_fila, use_container_width=True)

        st.markdown("---")
        st.markdown("##### 📋 Lista Detalhada")
        st.dataframe(
            df_fila[["MÚSICA", "AUTOR_MUSICA", "CLASSIFICACAO_MUSICA"]], 
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("Zeraram a fila! Todo o repertório desse filtro já foi tocado. 🎉")