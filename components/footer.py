import streamlit as st


def render_footer():
    st.markdown("""
<div style="
    text-align: center;
    padding: 40px 20px 30px;
    margin-top: 60px;
    background: linear-gradient(135deg, rgba(13,13,26,0.9) 0%, rgba(26,10,46,0.9) 100%);
    border-top: 1px solid rgba(139,92,246,0.2);
    border-radius: 20px 20px 0 0;
">
    <p style="font-family: 'Outfit', sans-serif; color: #555; font-size: 0.7rem; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 12px;">
        PROPULSÉ PAR
    </p>
    <div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; margin-bottom: 20px;">
        <span style="
            font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #06b6d4;
            background: rgba(6,182,212,0.1); border: 1px solid rgba(6,182,212,0.25);
            padding: 4px 14px; border-radius: 20px;
        ">Streamlit</span>
        <span style="
            font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #a78bfa;
            background: rgba(167,139,250,0.1); border: 1px solid rgba(167,139,250,0.25);
            padding: 4px 14px; border-radius: 20px;
        ">Pandas</span>
        <span style="
            font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #22d3ee;
            background: rgba(34,211,238,0.1); border: 1px solid rgba(34,211,238,0.25);
            padding: 4px 14px; border-radius: 20px;
        ">Plotly</span>
    </div>
    <a href="https://www.kaggle.com/datasets/" target="_blank" style="
        display: inline-block; font-family: 'Outfit', sans-serif; font-size: 0.85rem;
        color: #a78bfa; text-decoration: none;
        border: 1px solid rgba(139,92,246,0.3); border-radius: 12px;
        padding: 8px 24px;
        transition: all 0.3s ease;
    ">📦 Source Kaggle ↗</a>
</div>
""", unsafe_allow_html=True)
