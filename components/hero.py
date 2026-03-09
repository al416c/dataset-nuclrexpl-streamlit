import streamlit as st


def render_hero():
    st.markdown("""
<div class="hero-container">
    <div class="hero-title">Explosions nucléaires dans le monde</div>
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
