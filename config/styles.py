import streamlit as st


def inject_css():
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    *, html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    .hero-container {
        background: linear-gradient(135deg, #0d0d1a 0%, #1a0a2e 40%, #2d1b4e 70%, #1a0a2e 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 20px;
        padding: 40px 50px;
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 30% 50%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
                    radial-gradient(circle at 70% 50%, rgba(6, 182, 212, 0.06) 0%, transparent 50%);
    }
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #e0e0ff 0%, #a78bfa 50%, #06b6d4 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
        position: relative;
        z-index: 1;
    }
    .hero-subtitle {
        font-family: 'Outfit', sans-serif;
        font-size: 1.1rem;
        color: #8b8baf;
        font-weight: 300;
        letter-spacing: 0.5px;
        position: relative;
        z-index: 1;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #12121f 0%, #1e1e35 100%);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 16px 48px rgba(139, 92, 246, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.08);
        border-color: rgba(139, 92, 246, 0.4);
    }
    [data-testid="stMetricLabel"] {
        color: #8b8baf;
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    [data-testid="stMetricValue"] {
        color: #e0e0ff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.9rem;
        font-weight: 600;
    }

    .section-header {
        font-family: 'Outfit', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #e0e0ff;
        padding: 12px 0;
        margin-top: 20px;
        margin-bottom: 10px;
        border-left: 4px solid #8b5cf6;
        padding-left: 16px;
        position: relative;
    }
    .section-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 16px;
        width: 60px;
        height: 2px;
        background: linear-gradient(90deg, #8b5cf6, transparent);
    }

    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(139, 92, 246, 0.15);
    }

    .stSidebar [data-testid="stSidebarContent"] {
        background: linear-gradient(180deg, #0d0d1a 0%, #1a0a2e 50%, #12121f 100%);
    }
    .stSidebar .stMarkdown h2 {
        font-family: 'Outfit', sans-serif;
        color: #a78bfa;
        font-weight: 600;
    }

    .streamlit-expanderHeader {
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
        background: rgba(139, 92, 246, 0.08);
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    .streamlit-expanderHeader:hover {
        background: rgba(139, 92, 246, 0.15);
    }

    .stPlotlyChart {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(139, 92, 246, 0.1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stPlotlyChart:hover {
        box-shadow: 0 8px 40px rgba(139, 92, 246, 0.12);
        border-color: rgba(139, 92, 246, 0.25);
    }

    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    .badge:hover {
        transform: scale(1.05);
    }
    .badge-purple { background: rgba(139,92,246,0.2); color: #a78bfa; border: 1px solid rgba(139,92,246,0.3); }
    .badge-cyan { background: rgba(6,182,212,0.2); color: #22d3ee; border: 1px solid rgba(6,182,212,0.3); }

    .custom-separator {
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(139,92,246,0.3) 50%, transparent 100%);
        margin: 30px 0;
        border: none;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def separator():
    st.markdown('<div class="custom-separator"></div>', unsafe_allow_html=True)


def section_header(text):
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)
