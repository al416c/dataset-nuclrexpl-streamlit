import streamlit as st


def render_sidebar(df):
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

    return selected_country, selected_years, selected_yield
