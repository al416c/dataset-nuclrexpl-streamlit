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
    map_data = map_data.sort_values('Date.Year').reset_index(drop=True)
    map_data['Date.Year'] = map_data['Date.Year'].astype(int)

    fig_map = px.scatter_mapbox(
        map_data, lat='lat', lon='lon',
        color='WEAPON SOURCE COUNTRY',
        animation_frame='Date.Year',
        hover_data={'Date.Year': True, 'Yield_Average': ':.1f', 'lat': False, 'lon': False},
        color_discrete_map=COUNTRY_COLORS,
        zoom=1, height=700, opacity=0.8,
    )
    fig_map.update_traces(marker=dict(size=8))
    fig_map.update_layout(
        mapbox_style='carto-darkmatter',
        margin=dict(l=0, r=0, t=0, b=60),
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
        updatemenus=[dict(
            type="buttons", showactive=False,
            x=0.05, y=-0.02, xanchor="left", yanchor="top",
            buttons=[
                dict(label="▶ Lecture", method="animate",
                     args=[None, {"frame": {"duration": 150, "redraw": True},
                                  "fromcurrent": True,
                                  "transition": {"duration": 80}}]),
                dict(label="⏸ Pause", method="animate",
                     args=[[None], {"frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}]),
            ],
            font=dict(color='#e2e8f0', family='Outfit, sans-serif'),
            bgcolor='rgba(139,92,246,0.3)',
            bordercolor='rgba(139,92,246,0.5)',
        )],
        sliders=[dict(
            active=0,
            currentvalue=dict(prefix="Année : ", font=dict(size=14, family='JetBrains Mono, monospace', color='#a78bfa')),
            pad=dict(t=40),
            font=dict(color='#8b8baf', family='Outfit, sans-serif'),
            bgcolor='rgba(13,13,26,0.6)',
            activebgcolor='#8b5cf6',
            bordercolor='rgba(139,92,246,0.3)',
            borderwidth=1,
        )],
    )
    st.plotly_chart(fig_map, use_container_width=True)
