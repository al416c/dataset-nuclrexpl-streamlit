import streamlit as st


def render_footer():
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
