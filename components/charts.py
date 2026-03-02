import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config.settings import BASE_LAYOUT, GRADIENT_SCALE, PURPLE_SCALE, PIE_COLORS, GRID_STYLE
from config.styles import section_header, separator


def _title_font(text):
    return dict(text=text, font=dict(family='Outfit, sans-serif', size=16, color='#e0e0ff'))


def render_timeline_and_decades(df_filtered):
    separator()
    section_header("📊 Visualisations")

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
            **BASE_LAYOUT,
            title=_title_font("📈 Évolution chronologique des essais"),
            xaxis_title="Année",
            yaxis_title="Nombre d'essais",
            height=420,
            margin=dict(l=40, r=20, t=50, b=40),
            xaxis=GRID_STYLE,
            yaxis=GRID_STYLE,
        )
        fig1.layout.updatemenus = [dict(
            type="buttons",
            showactive=False,
            x=0.05, y=1.12,
            buttons=[dict(
                label="▶ Animer",
                method="animate",
                args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True)]
            )]
        )]
        frames = []
        for i in range(1, len(tests_per_year) + 1):
            frames.append(go.Frame(
                data=[go.Scatter(
                    x=tests_per_year['Date.Year'].iloc[:i],
                    y=tests_per_year['Essais'].iloc[:i],
                    fill='tozeroy',
                    fillcolor='rgba(139, 92, 246, 0.15)',
                    line=dict(width=2.5, color='#a78bfa'),
                )],
                name=str(i),
            ))
        fig1.frames = frames
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        decade_counts = df_filtered.groupby('Decade').size().reset_index(name='Essais')
        decade_counts = decade_counts.sort_values('Decade')
        fig2 = px.bar(
            decade_counts, x='Decade', y='Essais',
            color='Essais', color_continuous_scale=GRADIENT_SCALE,
        )
        fig2.update_traces(marker_line_width=0, opacity=0.9)
        fig2.update_layout(
            **BASE_LAYOUT,
            title=_title_font("📊 Distribution par décennie"),
            xaxis_title="Décennie",
            yaxis_title="Nombre d'essais",
            coloraxis_showscale=False,
            height=420,
            margin=dict(l=40, r=20, t=50, b=40),
            xaxis=GRID_STYLE,
            yaxis=GRID_STYLE,
        )
        st.plotly_chart(fig2, use_container_width=True)


def render_pie_and_ranking(df_filtered):
    separator()

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
            color_discrete_sequence=PIE_COLORS, hole=0.4,
        )
        fig3.update_traces(
            textposition='outside', textinfo='label+percent',
            textfont=dict(size=12, family='Outfit, sans-serif'),
            pull=[0.03] * len(main_data),
            marker=dict(line=dict(color='#0d0d1a', width=2)),
            rotation=90,
        )
        fig3.update_layout(
            **BASE_LAYOUT,
            height=480,
            margin=dict(l=20, r=20, t=50, b=20),
            title=_title_font("🥧 Répartition des essais"),
            showlegend=True,
            legend=dict(font=dict(size=11, family='Outfit, sans-serif')),
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col_bar:
        sorted_data = main_data.sort_values('Essais', ascending=True)
        fig4 = px.bar(
            sorted_data, x='Essais', y='Pays', orientation='h',
            color='Essais',
            color_continuous_scale=GRADIENT_SCALE,
            text='Essais',
        )
        fig4.update_traces(
            textposition='outside',
            textfont=dict(size=13, family='JetBrains Mono, monospace', color='#a78bfa'),
            marker_line_width=0,
        )
        fig4.update_layout(
            **BASE_LAYOUT,
            title=_title_font("🏆 Classement par nombre d'essais"),
            xaxis_title="Nombre d'essais",
            yaxis_title="",
            coloraxis_showscale=False,
            height=480,
            margin=dict(l=40, r=40, t=50, b=40),
            xaxis=GRID_STYLE,
            yaxis=GRID_STYLE,
        )
        st.plotly_chart(fig4, use_container_width=True)


def render_top_sites(df_filtered):
    if 'Location.Name' not in df_filtered.columns:
        return

    separator()
    section_header("📍 Top 10 des sites d'essais")
    top_sites = df_filtered['Location.Name'].value_counts().head(10).reset_index()
    top_sites.columns = ['Site', 'Essais']
    top_sites = top_sites.sort_values('Essais', ascending=True)

    fig5 = px.bar(
        top_sites, x='Essais', y='Site', orientation='h',
        color='Essais',
        color_continuous_scale=PURPLE_SCALE,
        text='Essais',
    )
    fig5.update_traces(
        textposition='outside',
        textfont=dict(size=13, family='JetBrains Mono, monospace', color='#a78bfa'),
        marker_line_width=0,
    )
    fig5.update_layout(
        **BASE_LAYOUT,
        title="",
        xaxis_title="Nombre d'essais",
        yaxis_title="",
        coloraxis_showscale=False,
        height=420,
        margin=dict(l=40, r=40, t=30, b=40),
        xaxis=GRID_STYLE,
        yaxis=GRID_STYLE,
    )
    st.plotly_chart(fig5, use_container_width=True)
