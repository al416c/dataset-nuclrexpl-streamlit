import streamlit as st
from config.settings import PAGE_CONFIG
from config.styles import inject_css
from data.loader import load_data, prepare_data, filter_data
from components.hero import render_hero
from components.sidebar import render_sidebar
from components.kpis import render_kpis
from components.tables import render_overview, render_stats, render_value_counts
from components.charts import render_timeline_and_decades, render_pie_and_ranking, render_top_sites
from components.map import render_map
from components.footer import render_footer

st.set_page_config(**PAGE_CONFIG)
inject_css()

render_hero()

df = prepare_data(load_data())

selected_country, selected_years, selected_yield = render_sidebar(df)

df_filtered = filter_data(df, selected_country, selected_years, selected_yield)

render_kpis(df_filtered)
render_overview(df_filtered, len(df))
render_stats(df_filtered)
render_value_counts(df_filtered)
render_timeline_and_decades(df_filtered)
render_pie_and_ranking(df_filtered)
render_map(df_filtered)
render_top_sites(df_filtered)
render_footer()