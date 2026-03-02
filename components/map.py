import streamlit as st
import plotly.express as px
from config.settings import COUNTRY_COLORS
from config.styles import section_header, separator


def _find_geo_columns(df):
    lat_col, lon_col = None, None
    for c in df.columns:
        cl = c.lower()
        if 'lat' in cl:
            lat_col = c
        if 'lon' in cl or 'long' in cl:
            lon_col = c
    return lat_col, lon_col


def render_map(df_filtered):
    lat_col, lon_col = _find_geo_columns(df_filtered)
    if not lat_col or not lon_col:
        return

    separator()
    section_header("🗺️ Carte des sites d'essais nucléaires")
    map_data = df_filtered[[lat_col, lon_col, 'WEAPON SOURCE COUNTRY', 'Date.Year', 'Yield_Average']].dropna()
    map_data = map_data.rename(columns={lat_col: 'lat', lon_col: 'lon'})

    fig_map = px.scatter_mapbox(
        map_data, lat='lat', lon='lon',
        color='WEAPON SOURCE COUNTRY',
        hover_data={'Date.Year': True, 'Yield_Average': ':.1f', 'lat': False, 'lon': False},
        color_discrete_map=COUNTRY_COLORS,
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
