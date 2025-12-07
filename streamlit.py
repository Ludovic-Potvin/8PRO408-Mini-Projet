import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from plotly.subplots import make_subplots

import streamlit as st


def _setup_boxplot(df):
    df_exploded = (
        df.assign(listed_in=df["listed_in"].str.split(", "))
        .explode("listed_in")
        .rename(columns={"listed_in": "genre"})
    )

    # Find the tops
    top = df_exploded["genre"].value_counts().nlargest(40).index
    df_top = df_exploded[df_exploded["genre"].isin(top)]

    # 3. Create box plot
    fig = px.box(
        df_top,
        x="release_year",
        y="genre",
        color="genre",
        title="Distribution des années de sortie par genre",
        orientation="h",
        hover_data={"title"},
    )

    fig.update_traces(hovertemplate="<b>%{customdata[0]}</b><extra></extra>")

    # Clean axis labels
    fig.update_layout(
        height=1200,
        xaxis_title="Années de sortie",
        yaxis_title="Genre",
        showlegend=False,
    )

    return fig


def _representation_populartie_genre(df):
    # Exploser la colonne listed_in en une ligne par genre
    genres_series = df["listed_in"].str.split(", ").explode()

    genres_counts = genres_series.value_counts().reset_index()
    genres_counts.columns = ["genre", "count"]
    genres_counts.head()

    # Représentation par barre
    fig = px.bar(
        genres_counts.head(20),
        x="genre",
        y="count",
        title="Genres les plus populaires",
        labels={"genre": "Genre", "count": "Nombre de titres"},
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig


# == Streamlit app setup == #

df = pd.read_csv("netflix_titles.csv")

st.title("Analyse du catalogue netflix")
st.subheader("Par Ludovic Potvin & Louis Seranne")
st.set_page_config(layout="wide")

# 1. Popularite par genre
st.header("Popularité par genre")
st.write("Le diagramme suivant nous permet de voir la popularité des genres")
barplot_genre = _representation_populartie_genre(df)
st.plotly_chart(barplot_genre)

# 2. Nombre de titre ajouter au fil du temps
st.header("Distribution des années de sortie par genre")
st.write(
    "Le diagramme suivant nous permet de facilement voir la popularité des genres au cour du temps"
)
boxplot_year_genre = _setup_boxplot(df)
st.plotly_chart(boxplot_year_genre)
