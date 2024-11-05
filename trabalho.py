import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Título e introdução
st.title("Dados globais sobre terremotos")
st.write("Este conjunto de dados fornece informações detalhadas sobre 1.137 terremotos ao redor do mundo, incluindo atributos como magnitude, localização, tempo e medições sismológicas. Os dados foram coletados usando a API EveryEarthquake da RapidAPI.")
st.write("Fonte: https://www.kaggle.com/datasets/shreyasur965/recent-earthquakes?resource=download")

# Carrega a base de dados earthquakes.csv
df = pd.read_csv('earthquakes.csv')

# Menu 
menu = st.sidebar.selectbox("Navegação", ["Home", "Incidência de Terremotos", "Sensação e Magnitude"])

# Condicional para exibir conteúdo com base na seleção do menu

#Menu Home
if menu == "Home":
    st.header("Mapa de Localização dos Terremotos")
    st.write("O st.map é uma função da biblioteca Streamlit que permite criar um mapa interativo de forma rápida e simples. Aqui estão os detalhes de como ele funciona:")

    # Adicionando um botão "Veja Mais"
    if st.button("Veja Mais"):
        st.write("""**Entrada de Dados**: O st.map aceita um DataFrame do Pandas com colunas chamadas latitude e longitude. Ele utiliza essas coordenadas para plotar pontos no mapa.""")

    # Verifique se as colunas de latitude e longitude estão presentes e plote o mapa
    if 'latitude' in df.columns and 'longitude' in df.columns:
        st.map(df[['latitude', 'longitude']])  
    else:
        st.error("As colunas 'latitude' e 'longitude' não estão presentes no arquivo CSV.")
        
    st.write("O mapa apresenta a marcação dos terremos documentados na base de dados.")

    if st.button("Curiosidades"):
            st.write("""
                    **Whites City (New Mexico)**: é o local com mais incidências de terremotos. Isso porque, a região do Novo México contém várias falhas geológicas que podem causar terremotos. E há uma grande aividade de Exploração de Recursos Naturais: Algumas áreas podem ter sua atividade sísmica aumentada por atividades humanas, como a exploração de petróleo e gás ou o fraturamento hidráulico (fracking), que pode causar tremores induzidos.
                    
                    **Izu Islands (Japan) e Hualien City (Taiwan)**:Embora não sejam extremamente próximas, ambas as áreas estão situadas no Círculo de Fogo do Pacífico, uma região conhecida por sua intensa atividade sísmica e vulcânica, o que significa que ambas podem estar sujeitas a terremotos.""")


# Menu Incidência de Terremotos
elif menu == "Incidência de Terremotos":
    st.header("Top 10 Locais com Maior Número de Terremotos")
    st.write("Dados obtidos com base na quantidade de **type = earthquake** por **location** mais apresentadas na base de dados.")

    if 'location' in df.columns:
        # Filtrar as 10 localizações com mais terremotos
        top_10_locations = df['location'].value_counts().nlargest(10)

        # Botão para informações adicionais sobre as bibliotecas
        if st.button("Bibliotecas utilizadas"):
            st.write("""Explicação das libs usadas para gerar o gráfico:

**matplotlib.pyplot**: É a biblioteca principal usada para criar gráficos em Python, incluindo gráficos de pizza.

**seaborn**: É uma biblioteca construída em cima do Matplotlib que fornece uma interface de alto nível para criar gráficos estatísticos mais atraentes e informativos. Neste caso, usamos Seaborn para definir a paleta de cores "pastel" para o gráfico de pizza.

**pandas**: Foi usado para a manipulação e análise dos dados, incluindo a contagem das localizações com mais terremotos.""")

        # Criar e exibir o gráfico de pizza
        plt.figure(figsize=(10, 8))
        plt.pie(top_10_locations, labels=top_10_locations.index, autopct='%1.1f%%', startangle=90, 
                colors=sns.color_palette("pastel"), wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
        plt.title('Top 10 Locais com Maior Número de Terremotos', fontsize=16)
        plt.axis('equal')
        plt.legend(title="Localizações", loc="best", bbox_to_anchor=(1, 0, 0.5, 1))

        # Mostrar o gráfico no Streamlit
        st.pyplot(plt)
    else:
        st.error("A coluna 'location' não está presente no arquivo CSV.")

# Menu Sensação e Magnitude
elif menu == "Sensação e Magnitude":
    st.header("Análise de Regressão Linear: Magnitude vs. Número de Pessoas que Sentiram")

    # Remover linhas com valores ausentes nas colunas 'magnitude' e 'felt'
    df_clean = df.dropna(subset=['magnitude', 'felt'])

    # Gráfico de regressão linear
    plt.figure(figsize=(10, 6))
    sns.regplot(x='magnitude', y='felt', data=df_clean, line_kws={'color': 'red'}, scatter_kws={'alpha': 0.5})
    plt.xlabel('Magnitude')
    plt.ylabel('Número de Pessoas que Sentiram')
    plt.title('Regressão Linear: Magnitude vs. Número de Pessoas que Sentiram')
    plt.grid(True)
    st.pyplot(plt)

    # Calcular a correlação entre 'magnitude' e 'felt'
    correlation = df_clean['magnitude'].corr(df_clean['felt'])

    # Calcular a média de magnitude por felt
    media_magnitude_por_felt = df.groupby('felt')['magnitude'].mean()

    # Gráfico de dispersão da magnitude vs. felt
    plt.figure(figsize=(10, 6))
    plt.scatter(df['felt'], df['magnitude'], alpha=0.5)
    plt.xlabel('Felt')
    plt.ylabel('Magnitude')
    plt.title('Magnitude vs. Felt')
    plt.grid(True)
    st.pyplot(plt)

    st.write("Os gráficos acima mostram a relação entre a magnitude dos terremotos e o número de pessoas que sentiram os tremores. Você pode analisar se há uma tendência clara entre os dois.")
    st.write("Apesar de de existir terremotos de escala 7 (mais alta), não significam que eles são os mais 'sentidos'. Isso porque, outros fatores, como a distância do epicentro e a densidade populacional, podem influenciar o número de pessoas que sentem um terremoto. ")