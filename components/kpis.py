import streamlit as st
import pandas as pd
from config.styles import section_header


def render_kpis(df_filtered):
    section_header("📊 Indicateurs clés")
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
