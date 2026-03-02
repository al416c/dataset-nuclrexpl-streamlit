import streamlit as st
from config.styles import section_header, separator


def render_overview(df_filtered, df_total_len):
    separator()
    section_header("📋 Aperçu du jeu de données")
    st.markdown(
        f'<span class="badge badge-cyan">{len(df_filtered)} essais affichés</span> '
        f'<span class="badge badge-purple">{df_total_len} au total</span>',
        unsafe_allow_html=True,
    )
    st.dataframe(df_filtered.head(50), use_container_width=True, height=300)


def render_stats(df_filtered):
    separator()
    section_header("📈 Statistiques par pays")
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


def render_value_counts(df_filtered):
    section_header("🔢 Répartition par pays")
    vc = df_filtered['WEAPON SOURCE COUNTRY'].value_counts().reset_index()
    vc.columns = ['Pays', "Nombre d'essais"]
    st.dataframe(vc, use_container_width=True)
