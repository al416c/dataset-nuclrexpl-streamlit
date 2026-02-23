import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="☢️ Explosions Nucléaires",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    *, html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    .hero-container {
        background: linear-gradient(135deg, #0d0d1a 0%, #1a0a2e 40%, #2d1b4e 70%, #1a0a2e 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 20px;
        padding: 40px 50px;
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 30% 50%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
                    radial-gradient(circle at 70% 50%, rgba(6, 182, 212, 0.06) 0%, transparent 50%);
        animation: pulse 8s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 0.5; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.05); }
    }
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #e0e0ff 0%, #a78bfa 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
        position: relative;
        z-index: 1;
    }
    .hero-subtitle {
        font-family: 'Outfit', sans-serif;
        font-size: 1.1rem;
        color: #8b8baf;
        font-weight: 300;
        letter-spacing: 0.5px;
        position: relative;
        z-index: 1;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #12121f 0%, #1e1e35 100%);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(139, 92, 246, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }
    [data-testid="stMetricLabel"] {
        color: #8b8baf;
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    [data-testid="stMetricValue"] {
        color: #e0e0ff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.9rem;
        font-weight: 600;
    }

    .section-header {
        font-family: 'Outfit', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #e0e0ff;
        padding: 12px 0;
        margin-top: 20px;
        margin-bottom: 10px;
        border-left: 4px solid #8b5cf6;
        padding-left: 16px;
    }

    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(139, 92, 246, 0.15);
    }

    .stSidebar [data-testid="stSidebarContent"] {
        background: linear-gradient(180deg, #0d0d1a 0%, #1a0a2e 50%, #12121f 100%);
    }
    .stSidebar .stMarkdown h2 {
        font-family: 'Outfit', sans-serif;
        color: #a78bfa;
        font-weight: 600;
    }

    .streamlit-expanderHeader {
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
        background: rgba(139, 92, 246, 0.08);
        border-radius: 10px;
    }

    .stPlotlyChart {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(139, 92, 246, 0.1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.5px;
    }
    .badge-purple { background: rgba(139,92,246,0.2); color: #a78bfa; border: 1px solid rgba(139,92,246,0.3); }
    .badge-cyan { background: rgba(6,182,212,0.2); color: #22d3ee; border: 1px solid rgba(6,182,212,0.3); }

    .custom-separator {
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(139,92,246,0.3) 50%, transparent 100%);
        margin: 30px 0;
        border: none;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-container">
    <div class="hero-title">☢️ Explosions nucléaires dans le monde</div>
    <div class="hero-subtitle">Analyse interactive de tous les essais nucléaires documentés · 1945 — 1998</div>
</div>
""", unsafe_allow_html=True)

with st.expander("ℹ️ Note : Essais nucléaires non confirmés (Israël)"):
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

st.sidebar.markdown("""
<div style="margin-top: 30px; padding: 15px; background: rgba(139,92,246,0.08); border-radius: 12px; border: 1px solid rgba(139,92,246,0.2);">
    <span class="badge badge-purple">SOURCE</span><br>
    <a href="https://www.kaggle.com/datasets/" style="color: #a78bfa; text-decoration: none; font-size: 0.9rem;">Kaggle Dataset ↗</a>
</div>
""", unsafe_allow_html=True)

df_filtered = df[
    (df['WEAPON SOURCE COUNTRY'].isin(selected_country)) &
    (df['Date.Year'] >= selected_years[0]) &
    (df['Date.Year'] <= selected_years[1]) &
    (df['Yield_Category'].isin(selected_yield))
]

st.markdown('<div class="section-header">📊 Indicateurs clés</div>', unsafe_allow_html=True)
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

st.markdown('<div class="custom-separator"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">📋 Aperçu du jeu de données</div>', unsafe_allow_html=True)
st.markdown(
    f'<span class="badge badge-cyan">{len(df_filtered)} essais affichés</span> '
    f'<span class="badge badge-purple">{len(df)} au total</span>',
    unsafe_allow_html=True,
)
st.dataframe(df_filtered.head(50), use_container_width=True, height=300)

st.markdown('<div class="custom-separator"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">📈 Statistiques par pays</div>', unsafe_allow_html=True)
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
    }).background_gradient(cmap='Purples', subset=["Nombre d'essais"]),
    use_container_width=True,
)

st.markdown('<div class="section-header">🔢 Répartition par pays</div>', unsafe_allow_html=True)
vc = df_filtered['WEAPON SOURCE COUNTRY'].value_counts().reset_index()
vc.columns = ['Pays', "Nombre d'essais"]
st.dataframe(vc, use_container_width=True)

st.markdown('<div class="custom-separator"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">📊 Visualisations</div>', unsafe_allow_html=True)

base_layout = dict(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(13,13,26,0.5)',
    font=dict(family='Outfit, sans-serif', size=12, color='#c0c0e0'),
)

col1, col2 = st.columns(2)

with col1:
    tests_per_year = df_filtered.groupby('Date.Year').size().reset_index(name='Essais')
    fig1 = px.area(
        tests_per_year, x='Date.Year', y='Essais',
        color_discrete_sequence=['#8b5cf6'],
    )
    fig1.update_traces(
        line=dict(width=2.5, color='#a78bfa'),
        fillcolor='rgba(139, 92, 246, 0.15)',
    )
    fig1.update_layout(
        **base_layout,
        title=dict(text="📈 Évolution chronologique des essais", font=dict(family='Outfit, sans-serif', size=16, color='#e0e0ff')),
        xaxis_title="Année",
        yaxis_title="Nombre d'essais",
        height=420,
        margin=dict(l=40, r=20, t=50, b=40),
        xaxis=dict(gridcolor='rgba(139,92,246,0.1)'),
        yaxis=dict(gridcolor='rgba(139,92,246,0.1)'),
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    decade_counts = df_filtered.groupby('Decade').size().reset_index(name='Essais')
    decade_counts = decade_counts.sort_values('Decade')
    fig2 = px.bar(
        decade_counts, x='Decade', y='Essais',
        color='Essais', color_continuous_scale=[[0, '#2d1b4e'], [0.5, '#7c3aed'], [1, '#06b6d4']],
    )
    fig2.update_traces(marker_line_width=0, opacity=0.9)
    fig2.update_layout(
        **base_layout,
        title=dict(text="📊 Distribution par décennie", font=dict(family='Outfit, sans-serif', size=16, color='#e0e0ff')),
        xaxis_title="Décennie",
        yaxis_title="Nombre d'essais",
        coloraxis_showscale=False,
        height=420,
        margin=dict(l=40, r=20, t=50, b=40),
        xaxis=dict(gridcolor='rgba(139,92,246,0.1)'),
        yaxis=dict(gridcolor='rgba(139,92,246,0.1)'),
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('<div class="custom-separator"></div>', unsafe_allow_html=True)

country_counts = df_filtered['WEAPON SOURCE COUNTRY'].value_counts().reset_index()
country_counts.columns = ['Pays', 'Essais']

total = country_counts['Essais'].sum()
country_counts['Pct'] = country_counts['Essais'] / total
main_data = country_counts[country_counts['Pct'] >= 0.02].copy()
others_sum = country_counts[country_counts['Pct'] < 0.02]['Essais'].sum()
if others_sum > 0:
    others_row = pd.DataFrame([{'Pays': 'Autres', 'Essais': others_sum, 'Pct': others_sum / total}])
    main_data = pd.concat([main_data, others_row], ignore_index=True)

pie_colors = ['#8b5cf6', '#06b6d4', '#f59e0b', '#10b981', '#ef4444', '#ec4899', '#6366f1', '#14b8a6']

col_pie, col_bar = st.columns(2)

with col_pie:
    fig3 = px.pie(
        main_data, values='Essais', names='Pays',
        color_discrete_sequence=pie_colors, hole=0.4,
    )
    fig3.update_traces(
        textposition='outside', textinfo='label+percent',
        textfont=dict(size=12, family='Outfit, sans-serif'),
        pull=[0.03] * len(main_data),
        marker=dict(line=dict(color='#0d0d1a', width=2)),
    )
    fig3.update_layout(
        **base_layout,
        height=480,
        margin=dict(l=20, r=20, t=50, b=20),
        title=dict(text="🥧 Répartition des essais", font=dict(family='Outfit, sans-serif', size=16, color='#e0e0ff')),
        showlegend=True,
        legend=dict(font=dict(size=11, family='Outfit, sans-serif')),
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_bar:
    sorted_data = main_data.sort_values('Essais', ascending=True)
    fig4 = px.bar(
        sorted_data, x='Essais', y='Pays', orientation='h',
        color='Essais',
        color_continuous_scale=[[0, '#2d1b4e'], [0.5, '#7c3aed'], [1, '#06b6d4']],
        text='Essais',
    )
    fig4.update_traces(
        textposition='outside',
        textfont=dict(size=13, family='JetBrains Mono, monospace', color='#a78bfa'),
        marker_line_width=0,
    )
    fig4.update_layout(
        **base_layout,
        title=dict(text="🏆 Classement par nombre d'essais", font=dict(family='Outfit, sans-serif', size=16, color='#e0e0ff')),
        xaxis_title="Nombre d'essais",
        yaxis_title="",
        coloraxis_showscale=False,
        height=480,
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(gridcolor='rgba(139,92,246,0.1)'),
        yaxis=dict(gridcolor='rgba(139,92,246,0.1)'),
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown('<div class="custom-separator"></div>', unsafe_allow_html=True)

lat_col = None
lon_col = None
for c in df_filtered.columns:
    cl = c.lower()
    if 'lat' in cl:
        lat_col = c
    if 'lon' in cl or 'long' in cl:
        lon_col = c

if lat_col and lon_col:
    st.markdown('<div class="section-header">🗺️ Carte des sites d\'essais nucléaires</div>', unsafe_allow_html=True)
    map_data = df_filtered[[lat_col, lon_col, 'WEAPON SOURCE COUNTRY', 'Date.Year', 'Yield_Average']].dropna()
    map_data = map_data.rename(columns={lat_col: 'lat', lon_col: 'lon'})

    color_map = {
        'États-Unis': '#8b5cf6',
        'URSS': '#ef4444',
        'France': '#3b82f6',
        'Chine': '#f59e0b',
        'UK': '#10b981',
        'Inde': '#ec4899',
        'Pakistan': '#06b6d4',
        'Corée du Nord': '#f97316',
    }

    fig_map = px.scatter_mapbox(
        map_data, lat='lat', lon='lon',
        color='WEAPON SOURCE COUNTRY',
        hover_data={'Date.Year': True, 'Yield_Average': ':.1f', 'lat': False, 'lon': False},
        color_discrete_map=color_map,
        zoom=1, height=650, opacity=0.75,
    )
    fig_map.update_traces(marker=dict(size=7))
    fig_map.update_layout(
        mapbox_style='carto-darkmatter',
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(family='Outfit, sans-serif'),
        legend=dict(
            title="Pays",
            font=dict(size=12, family='Outfit, sans-serif'),
            bgcolor='rgba(13,13,26,0.8)',
            bordercolor='rgba(139,92,246,0.3)',
            borderwidth=1,
            yanchor="top", y=0.99,
            xanchor="left", x=0.01,
        ),
    )
    st.plotly_chart(fig_map, use_container_width=True)

st.markdown('<div class="custom-separator"></div>', unsafe_allow_html=True)

if 'Location.Name' in df_filtered.columns:
    st.markdown('<div class="section-header">📍 Top 10 des sites d\'essais</div>', unsafe_allow_html=True)
    top_sites = df_filtered['Location.Name'].value_counts().head(10).reset_index()
    top_sites.columns = ['Site', 'Essais']
    top_sites = top_sites.sort_values('Essais', ascending=True)
    fig5 = px.bar(
        top_sites, x='Essais', y='Site', orientation='h',
        color='Essais',
        color_continuous_scale=[[0, '#1a0a2e'], [0.5, '#6d28d9'], [1, '#a78bfa']],
        text='Essais',
    )
    fig5.update_traces(
        textposition='outside',
        textfont=dict(size=13, family='JetBrains Mono, monospace', color='#a78bfa'),
        marker_line_width=0,
    )
    fig5.update_layout(
        **base_layout,
        title="",
        xaxis_title="Nombre d'essais",
        yaxis_title="",
        coloraxis_showscale=False,
        height=420,
        margin=dict(l=40, r=40, t=30, b=40),
        xaxis=dict(gridcolor='rgba(139,92,246,0.1)'),
        yaxis=dict(gridcolor='rgba(139,92,246,0.1)'),
    )
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("""
<div style="
    text-align: center;
    padding: 30px 20px;
    margin-top: 40px;
    background: linear-gradient(135deg, rgba(13,13,26,0.8) 0%, rgba(26,10,46,0.8) 100%);
    border-top: 1px solid rgba(139,92,246,0.2);
    border-radius: 16px 16px 0 0;
">
    <span style="font-family: 'Outfit', sans-serif; color: #8b8baf; font-size: 0.9rem;">
        📦 Source :
        <a href="https://www.kaggle.com/datasets/" style="color: #a78bfa; text-decoration: none;">
            Kaggle — Explosions Nucléaires ↗
        </a>
        &nbsp;·&nbsp; Réalisé avec
        <span style="color: #06b6d4;">Streamlit</span>,
        <span style="color: #a78bfa;">Pandas</span>,
        <span style="color: #22d3ee;">Plotly</span>
    </span>
</div>
""", unsafe_allow_html=True)