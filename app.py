import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Exploration des explosions nucléaires", layout="wide")

st.title("Exploration des explosions nucléaires dans le monde")

@st.cache_data
def load_data():
    return pd.read_csv("nuclear_explosions.csv")

df = load_data()

df = df.assign(Yield_Average=(df['Data.Yeild.Lower'] + df['Data.Yeild.Upper']) / 2)
df['Decade'] = df['Date.Year'].apply(lambda x: (x // 10) * 10)
df['Yield_Category'] = df['Yield_Average'].map(
    lambda x: 'Faible' if x < 20 else ('Moyen' if x < 1000 else 'Élevé')
)

st.sidebar.header("🎛️ Filtres Interactifs")
countries = sorted(df['WEAPON SOURCE COUNTRY'].unique())
selected_country = st.sidebar.multiselect("Pays source", countries, default=countries)
min_year, max_year = int(df['Date.Year'].min()), int(df['Date.Year'].max())
selected_years = st.sidebar.slider("Période", min_year, max_year, (min_year, max_year))

yield_categories = df['Yield_Category'].unique().tolist()
selected_yield = st.sidebar.multiselect("Catégorie de puissance", yield_categories, default=yield_categories)

df_filtered = df[
    (df['WEAPON SOURCE COUNTRY'].isin(selected_country)) &
    (df['Date.Year'] >= selected_years[0]) &
    (df['Date.Year'] <= selected_years[1]) &
    (df['Yield_Category'].isin(selected_yield))
]

st.subheader("📋 Aperçu du Dataset")
st.markdown(f"**{len(df_filtered)}** essais affichés sur **{len(df)}** au total.")
st.dataframe(df_filtered.head(50), use_container_width=True)

st.subheader("📈 Statistiques par pays")
stats = (
    df_filtered
    .groupby('WEAPON SOURCE COUNTRY')['Yield_Average']
    .agg(['sum', 'mean', 'std', 'count'])
    .reset_index()
)
stats.columns = ['Pays', 'Total Yield', 'Moyenne', 'Écart-type', "Nombre d'essais"]
stats = stats.sort_values("Nombre d'essais", ascending=False)
st.dataframe(stats.style.format({
    'Total Yield': '{:,.1f}',
    'Moyenne': '{:,.2f}',
    'Écart-type': '{:,.2f}',
}), use_container_width=True)

st.subheader("🔢 Nombre d'essais par pays (value_counts)")
vc = df_filtered['WEAPON SOURCE COUNTRY'].value_counts().reset_index()
vc.columns = ['Pays', "Nombre d'essais"]
st.dataframe(vc, use_container_width=True)
st.subheader("📊 Visualisations")

col_viz1, col_viz2 = st.columns(2)

with col_viz1:
    st.markdown("**1. Évolution chronologique (Courbe)**")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    tests_per_year = df_filtered.groupby('Date.Year').size()
    ax1.plot(tests_per_year.index, tests_per_year.values, color='#1f77b4', marker='o', markersize=4, linewidth=2)
    ax1.set_xlabel("Année", fontsize=11)
    ax1.set_ylabel("Nombre d'essais", fontsize=11)
    ax1.set_title("Essais nucléaires par année", fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    fig1.tight_layout()
    st.pyplot(fig1)

with col_viz2:
    st.markdown("**2. Distribution par décennie (Histogramme)**")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    decade_counts = df_filtered.groupby('Decade').size().reset_index(name='count')
    ax2.bar(
        decade_counts['Decade'].astype(str),
        decade_counts['count'],
        color='#ff7f0e',
        edgecolor='white',
        linewidth=0.8,
    )
    ax2.set_xlabel("Décennie", fontsize=11)
    ax2.set_ylabel("Nombre d'essais", fontsize=11)
    ax2.set_title("Essais par décennie", fontsize=13, fontweight='bold')
    ax2.grid(True, axis='y', alpha=0.3)
    fig2.tight_layout()
    st.pyplot(fig2)

st.markdown("**3. Répartition globale par pays (Diagramme circulaire)**")
country_counts = df_filtered['WEAPON SOURCE COUNTRY'].value_counts()

threshold = 0.02
total = country_counts.sum()
main = country_counts[country_counts / total >= threshold].copy()
others = country_counts[country_counts / total < threshold]
if len(others) > 0:
    main['Autres'] = others.sum()

colors = plt.cm.Set2(range(len(main)))

fig3, ax3 = plt.subplots(figsize=(7, 5))
wedges, texts, autotexts = ax3.pie(
    main,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    pctdistance=0.80,
    wedgeprops=dict(edgecolor='white', linewidth=2),
)

for autotext in autotexts:
    autotext.set_fontsize(9)
    autotext.set_fontweight('bold')

for text in texts:
    text.set_text('')

ax3.legend(
    wedges,
    main.index,
    title="Pays",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
    fontsize=10,
    title_fontsize=11,
)
ax3.set_title("Répartition des essais par pays", fontsize=13, fontweight='bold', pad=20)
ax3.axis('equal')
fig3.tight_layout()
st.pyplot(fig3)

lat_col = None
lon_col = None
for c in df_filtered.columns:
    cl = c.lower()
    if 'lat' in cl:
        lat_col = c
    if 'lon' in cl or 'long' in cl:
        lon_col = c

if lat_col and lon_col:
    st.subheader("🗺️ Carte des sites d'essais nucléaires")
    map_data = df_filtered[[lat_col, lon_col, 'WEAPON SOURCE COUNTRY']].dropna()
    map_data = map_data.rename(columns={lat_col: 'latitude', lon_col: 'longitude'})
    st.map(map_data, size=20)

if 'Location.Name' in df_filtered.columns:
    st.subheader("📍 Top 10 des sites d'essais")
    top_sites = df_filtered['Location.Name'].value_counts().head(10)
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    bars = ax4.barh(top_sites.index[::-1], top_sites.values[::-1], color='#2ca02c', edgecolor='white')
    ax4.set_xlabel("Nombre d'essais", fontsize=11)
    ax4.set_title("Top 10 des sites d'essais nucléaires", fontsize=13, fontweight='bold')
    ax4.grid(True, axis='x', alpha=0.3)
    for bar in bars:
        width = bar.get_width()
        ax4.text(width + 1, bar.get_y() + bar.get_height() / 2, f'{int(width)}',
                 ha='left', va='center', fontsize=9, fontweight='bold')
    fig4.tight_layout()
    st.pyplot(fig4)

st.markdown("---")
st.markdown(
    "📦 Source : [Kaggle - Nuclear Explosions](https://www.kaggle.com/datasets/) "
    "| Réalisé avec **Streamlit**, **Pandas**, **Matplotlib** & **Seaborn**"
)