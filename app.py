import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Exploration des Explosions Nucléaires", layout="wide")

st.title("Exploration des Explosions Nucléaires dans le Monde")

@st.cache_data
def load_data():
    return pd.read_csv("nuclear_explosions.csv")

df = load_data()

df = df.assign(Yield_Average=(df['Data.Yeild.Lower'] + df['Data.Yeild.Upper']) / 2)
df['Decade'] = df['Date.Year'].apply(lambda x: (x // 10) * 10)

st.sidebar.header("Filtres Interactifs")
countries = df['WEAPON SOURCE COUNTRY'].unique()
selected_country = st.sidebar.multiselect("Pays source", countries, default=countries)
min_year, max_year = int(df['Date.Year'].min()), int(df['Date.Year'].max())
selected_years = st.sidebar.slider("Période", min_year, max_year, (min_year, max_year))

df_filtered = df[
    (df['WEAPON SOURCE COUNTRY'].isin(selected_country)) & 
    (df['Date.Year'] >= selected_years[0]) & 
    (df['Date.Year'] <= selected_years[1])
]

st.subheader("Aperçu du Dataset")
st.dataframe(df_filtered.head())

col1, col2 = st.columns(2)

with col1:
    st.subheader("Nombre d'essais par type")
    st.dataframe(df_filtered['Data.Type'].value_counts().reset_index())

with col2:
    st.subheader("Statistiques de Puissance (Yield) par Pays")
    stats = df_filtered.groupby('WEAPON SOURCE COUNTRY')['Yield_Average'].agg(['sum', 'mean', 'std']).reset_index()
    st.dataframe(stats)

st.subheader("Visualisations")

col_viz1, col_viz2 = st.columns(2)

with col_viz1:
    st.markdown("**1. Évolution chronologique (Courbe)**")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    tests_per_year = df_filtered.groupby('Date.Year').size()
    ax1.plot(tests_per_year.index, tests_per_year.values, color='b', marker='o', markersize=4)
    ax1.grid(True)
    st.pyplot(fig1)

with col_viz2:
    st.markdown("**2. Distribution par décennie (Histogramme)**")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.histplot(df_filtered['Decade'], bins=len(df['Decade'].unique()), kde=False, ax=ax2, color='orange')
    st.pyplot(fig2)

st.markdown("**3. Répartition globale par pays (Diagramme circulaire)**")
fig3, ax3 = plt.subplots(figsize=(6, 6))
country_counts = df_filtered['WEAPON SOURCE COUNTRY'].value_counts()
ax3.pie(country_counts, labels=country_counts.index, autopct='%1.1f%%', startangle=90)
ax3.axis('equal')
st.pyplot(fig3)