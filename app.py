import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="☢️ Explosions nucléaires",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .block-container { padding-top: 1rem; }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%);
        border: 1px solid #3d3d5c;
        border-radius: 12px;
        padding: 15px 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    [data-testid="stMetricLabel"] { color: #a0a0c0; }
    [data-testid="stMetricValue"] { color: #ffffff; font-size: 1.8rem; }
    .stDataFrame { border-radius: 10px; overflow: hidden; }
    h1, h2, h3 { color: #e0e0ff; }
    .stSidebar [data-testid="stSidebarContent"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
</style>
""", unsafe_allow_html=True)

st.title("☢️ Exploration des explosions nucléaires dans le monde")

with st.expander("ℹ️ Note : Essais nucléaires non confirmés"):
    st.markdown("""
    **Israël** n'apparaît pas dans ce dataset car aucun essai nucléaire israélien
    n'est officiellement confirmé. Cependant, plusieurs événements sont suspectés :

    - **1963** — Test souterrain possible dans le désert du Néguev
      (rapporté par *Wehrtechnik*, magazine militaire ouest-allemand)
    - **1966** — Test d'implosion possible à rendement nul dans le Néguev
    - **1979** — **Incident Vela** : double flash détecté par un satellite américain
      dans l'océan Indien sud. Un consensus scientifique et historique considère
      qu'il s'agissait d'un test nucléaire israélien
      (Avner Cohen, Middlebury Institute).

    Israël maintient une politique officielle d'**ambiguïté nucléaire**
    et n'a jamais confirmé ni infirmé posséder l'arme nucléaire.
    (Malgré les différentes sources et preuves attestant le contraire)

    *Sources : Lt. Col. Warner D. Farr (USAF), The New York Times,
    Theodore Taylor, Avner Cohen.*
    """)

@st.cache_data
def load_data():
    return pd.read_csv("nuclear_explosions.csv")

df = load_data()

# Traduction des noms de pays
country_translation = {
    'USSR': 'URSS',
    'USA': 'États-Unis',
    'FRANCE': 'France',
    'CHINA': 'Chine',
    'INDIA': 'Inde',
    'PAKISTAN': 'Pakistan',
    'UK': 'UK',
    'NORTH KOREA': 'Corée du Nord',
}
df['WEAPON SOURCE COUNTRY'] = df['WEAPON SOURCE COUNTRY'].replace(country_translation)

df = df.assign(Yield_Average=(df['Data.Yeild.Lower'] + df['Data.Yeild.Upper']) / 2)
df['Decade'] = df['Date.Year'].apply(lambda x: f"{(x // 10) * 10}s")
df['Yield_Category'] = df['Yield_Average'].map(
    lambda x: '🟢 Faible (<20 kt)' if x < 20 else ('🟡 Moyen (20-1000 kt)' if x < 1000 else '🔴 Élevé (>1000 kt)')
)

st.sidebar.markdown("## 🎛️ Filtres")

countries = sorted(df['WEAPON SOURCE COUNTRY'].unique())
selected_country = st.sidebar.multiselect("🌍 Pays source", countries, default=countries)

min_year, max_year = int(df['Date.Year'].min()), int(df['Date.Year'].max())
selected_years = st.sidebar.slider("📅 Période", min_year, max_year, (min_year, max_year))

yield_categories = df['Yield_Category'].unique().tolist()
selected_yield = st.sidebar.multiselect("💥 Catégorie de puissance", yield_categories, default=yield_categories)

st.sidebar.markdown("📦 Source : [Kaggle](https://www.kaggle.com/datasets/)")

df_filtered = df[
    (df['WEAPON SOURCE COUNTRY'].isin(selected_country)) &
    (df['Date.Year'] >= selected_years[0]) &
    (df['Date.Year'] <= selected_years[1]) &
    (df['Yield_Category'].isin(selected_yield))
]

st.markdown("### 📊 Indicateurs clés")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("Total essais", f"{len(df_filtered):,}")
with kpi2:
    st.metric("Pays impliqués", f"{df_filtered['WEAPON SOURCE COUNTRY'].nunique()}")
with kpi3:
    avg_yield = df_filtered['Yield_Average'].mean()
    st.metric("Puissance moyenne", f"{avg_yield:,.1f} kt" if not pd.isna(avg_yield) else "N/A")
with kpi4:
    max_yield = df_filtered['Yield_Average'].max()
    st.metric("Essai le plus puissant", f"{max_yield:,.0f} kt" if not pd.isna(max_yield) else "N/A")

st.subheader("📋 Aperçu du jeu de données")
st.markdown(f"**{len(df_filtered)}** essais affichés sur **{len(df)}** au total.")
st.dataframe(df_filtered.head(50), use_container_width=True, height=300)

st.subheader("📈 Statistiques par pays")
stats = (
    df_filtered
    .groupby('WEAPON SOURCE COUNTRY')['Yield_Average']
    .agg(['sum', 'mean', 'std', 'count'])
    .reset_index()
)
stats.columns = ['Pays', 'Puissance totale (kt)', 'Moyenne (kt)', 'Écart-type (kt)', "Nombre d'essais"]
stats = stats.sort_values("Nombre d'essais", ascending=False)
st.dataframe(
    stats.style.format({
        'Puissance totale (kt)': '{:,.1f}',
        'Moyenne (kt)': '{:,.2f}',
        'Écart-type (kt)': '{:,.2f}',
    }).background_gradient(cmap='YlOrRd', subset=["Nombre d'essais"]),
    use_container_width=True,
)

st.subheader("🔢 Répartition par pays (value_counts)")
vc = df_filtered['WEAPON SOURCE COUNTRY'].value_counts().reset_index()
vc.columns = ['Pays', "Nombre d'essais"]
st.dataframe(vc, use_container_width=True)

st.subheader("📊 Visualisations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📈 Évolution chronologique")
    tests_per_year = df_filtered.groupby('Date.Year').size().reset_index(name='Essais')
    fig1 = px.line(
        tests_per_year, x='Date.Year', y='Essais',
        markers=True, color_discrete_sequence=['#00d4ff'],
    )
    fig1.update_layout(
        template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Année",
        yaxis_title="Nombre d'essais", font=dict(size=12),
        height=400, margin=dict(l=40, r=20, t=30, b=40),
    )
    fig1.update_traces(line=dict(width=2.5), marker=dict(size=5))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("#### 📊 Distribution par décennie")
    decade_counts = df_filtered.groupby('Decade').size().reset_index(name='Essais')
    decade_counts = decade_counts.sort_values('Decade')
    fig2 = px.bar(
        decade_counts, x='Decade', y='Essais',
        color='Essais', color_continuous_scale='Oranges',
    )
    fig2.update_layout(
        template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Décennie",
        yaxis_title="Nombre d'essais", font=dict(size=12),
        height=400, margin=dict(l=40, r=20, t=30, b=40),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("#### 🥧 Répartition des essais par pays")
country_counts = df_filtered['WEAPON SOURCE COUNTRY'].value_counts().reset_index()
country_counts.columns = ['Pays', 'Essais']

total = country_counts['Essais'].sum()
country_counts['Pct'] = country_counts['Essais'] / total
main_data = country_counts[country_counts['Pct'] >= 0.02].copy()
others_sum = country_counts[country_counts['Pct'] < 0.02]['Essais'].sum()
if others_sum > 0:
    others_row = pd.DataFrame([{'Pays': 'Autres', 'Essais': others_sum, 'Pct': others_sum / total}])
    main_data = pd.concat([main_data, others_row], ignore_index=True)

col_pie, col_bar = st.columns(2)

with col_pie:
    fig3 = px.pie(
        main_data, values='Essais', names='Pays',
        color_discrete_sequence=px.colors.qualitative.Set2, hole=0.35,
    )
    fig3.update_traces(
        textposition='outside', textinfo='label+percent',
        textfont_size=12, pull=[0.03] * len(main_data),
        marker=dict(line=dict(color='#1a1a2e', width=2)),
    )
    fig3.update_layout(
        template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12), height=450,
        margin=dict(l=20, r=20, t=30, b=20),
        showlegend=True, legend=dict(font=dict(size=11)),
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_bar:
    st.markdown("#### 🏆 Classement par nombre d'essais")
    sorted_data = main_data.sort_values('Essais', ascending=True)
    fig4 = px.bar(
        sorted_data, x='Essais', y='Pays', orientation='h',
        color='Essais', color_continuous_scale='Tealgrn', text='Essais',
    )
    fig4.update_traces(textposition='outside', textfont_size=12)
    fig4.update_layout(
        template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Nombre d'essais",
        yaxis_title="", font=dict(size=12), height=450,
        margin=dict(l=20, r=40, t=30, b=40), coloraxis_showscale=False,
    )
    st.plotly_chart(fig4, use_container_width=True)

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
    map_data = df_filtered[[lat_col, lon_col, 'WEAPON SOURCE COUNTRY', 'Date.Year', 'Yield_Average']].dropna()
    map_data = map_data.rename(columns={lat_col: 'lat', lon_col: 'lon'})
    fig_map = px.scatter_mapbox(
        map_data, lat='lat', lon='lon',
        color='WEAPON SOURCE COUNTRY',
        hover_data={'Date.Year': True, 'Yield_Average': ':.1f', 'lat': False, 'lon': False},
        color_discrete_sequence=px.colors.qualitative.Set2,
        zoom=1, height=600, opacity=0.7,
    )
    fig_map.update_traces(marker=dict(size=6))
    fig_map.update_layout(
        mapbox_style='carto-darkmatter',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(
            title="Pays",
            font=dict(size=12),
            bgcolor='rgba(0,0,0,0.5)',
            yanchor="top", y=0.99,
            xanchor="left", x=0.01,
        ),
    )
    st.plotly_chart(fig_map, use_container_width=True)

if 'Location.Name' in df_filtered.columns:
    st.subheader("📍 Top 10 des sites d'essais")
    top_sites = df_filtered['Location.Name'].value_counts().head(10).reset_index()
    top_sites.columns = ['Site', 'Essais']
    top_sites = top_sites.sort_values('Essais', ascending=True)
    fig5 = px.bar(
        top_sites, x='Essais', y='Site', orientation='h',
        color='Essais', color_continuous_scale='Purples', text='Essais',
    )
    fig5.update_traces(textposition='outside', textfont_size=12)
    fig5.update_layout(
        template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Nombre d'essais",
        yaxis_title="", font=dict(size=12), height=400,
        margin=dict(l=20, r=40, t=30, b=40), coloraxis_showscale=False,
    )
    st.plotly_chart(fig5, use_container_width=True)

st.markdown(
    "<div style='text-align: center; color: #666; padding: 20px;'>"
    "📦 Source : <a href='https://www.kaggle.com/datasets/' style='color: #00d4ff;'>Kaggle - Explosions Nucléaires</a> "
    "| Réalisé avec <b>Streamlit</b>, <b>Pandas</b>, <b>Plotly</b>"
    "</div>",
    unsafe_allow_html=True,
)