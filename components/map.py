import numpy as np
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

    extra_cols = [c for c in ['Data.Name', 'Data.Type', 'Data.Purpose', 'WEAPON DEPLOYMENT LOCATION'] if c in df_filtered.columns]
    map_data = df_filtered[[lat_col, lon_col, 'WEAPON SOURCE COUNTRY', 'Date.Year', 'Yield_Average'] + extra_cols].dropna(subset=[lat_col, lon_col])
    map_data = map_data.rename(columns={lat_col: 'lat', lon_col: 'lon'})
    map_data['Date.Year'] = map_data['Date.Year'].astype(int)
    map_data['Yield_Display'] = map_data['Yield_Average'].fillna(0)
    map_data['Marker_Size'] = np.clip(np.log1p(map_data['Yield_Display']) * 2.5, 5, 30)

    view = st.radio(
        "Mode d'affichage",
        ["☢️ Points (par pays)", "🌡️ Carte de densité"],
        horizontal=True,
        label_visibility='collapsed',
    )

    _legend_style = dict(
        title="Pays",
        font=dict(size=12, family='Outfit, sans-serif'),
        bgcolor='rgba(13,13,26,0.8)',
        bordercolor='rgba(139,92,246,0.3)',
        borderwidth=1,
        yanchor="top", y=0.99,
        xanchor="left", x=0.01,
    )

    if view == "☢️ Points (par pays)":
        hover_tpl = "<b>%{customdata[0]}</b><br>"
        hover_tpl += "Pays : %{customdata[1]}<br>"
        hover_tpl += "Année : %{customdata[2]}<br>"
        hover_tpl += "Puissance : %{customdata[3]:.1f} kt<br>"
        if 'Data.Name' in map_data.columns:
            hover_tpl += "Nom : %{customdata[4]}<br>"
        hover_tpl += "<extra></extra>"

        custom_cols = [
            map_data.get('WEAPON DEPLOYMENT LOCATION', map_data['WEAPON SOURCE COUNTRY']),
            map_data['WEAPON SOURCE COUNTRY'],
            map_data['Date.Year'],
            map_data['Yield_Display'],
        ]
        if 'Data.Name' in map_data.columns:
            custom_cols.append(map_data['Data.Name'])

        fig_map = px.scatter_mapbox(
            map_data, lat='lat', lon='lon',
            color='WEAPON SOURCE COUNTRY',
            color_discrete_map=COUNTRY_COLORS,
            zoom=1, height=650, opacity=0.8,
        )
        fig_map.update_traces(
            marker=dict(size=map_data['Marker_Size']),
            customdata=np.stack(custom_cols, axis=-1),
            hovertemplate=hover_tpl,
        )
        fig_map.update_layout(
            mapbox_style='carto-darkmatter',
            margin=dict(l=0, r=0, t=0, b=0),
            font=dict(family='Outfit, sans-serif'),
            legend=_legend_style,
        )
        st.plotly_chart(fig_map, use_container_width=True)

    else:
        fig_density = px.density_mapbox(
            map_data, lat='lat', lon='lon',
            z='Yield_Display',
            radius=18,
            zoom=1, height=650,
            color_continuous_scale=[
                [0, 'rgba(13,13,26,0)'],
                [0.2, 'rgba(139,92,246,0.3)'],
                [0.5, 'rgba(167,139,250,0.6)'],
                [0.8, 'rgba(6,182,212,0.8)'],
                [1, 'rgba(34,211,238,1)'],
            ],
        )
        fig_density.update_layout(
            mapbox_style='carto-darkmatter',
            margin=dict(l=0, r=0, t=0, b=0),
            font=dict(family='Outfit, sans-serif'),
            coloraxis_colorbar=dict(
                title=dict(text='Puissance (kt)', font=dict(family='Outfit, sans-serif', size=12, color='#a78bfa')),
                tickfont=dict(family='JetBrains Mono, monospace', size=10, color='#8b8baf'),
                bgcolor='rgba(13,13,26,0.6)',
                bordercolor='rgba(139,92,246,0.3)',
                borderwidth=1,
            ),
        )
        st.plotly_chart(fig_density, use_container_width=True)
