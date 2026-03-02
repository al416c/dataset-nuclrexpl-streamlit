PAGE_CONFIG = dict(
    page_title="☢️ Explosions Nucléaires",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="expanded",
)

COUNTRY_TRANSLATION = {
    'USSR': 'URSS',
    'USA': 'États-Unis',
    'FRANCE': 'France',
    'CHINA': 'Chine',
    'INDIA': 'Inde',
    'PAKISTAN': 'Pakistan',
    'UK': 'UK',
    'NORTH KOREA': 'Corée du Nord',
}

COUNTRY_COLORS = {
    'États-Unis': '#8b5cf6',
    'URSS': '#ef4444',
    'France': '#3b82f6',
    'Chine': '#f59e0b',
    'UK': '#10b981',
    'Inde': '#ec4899',
    'Pakistan': '#06b6d4',
    'Corée du Nord': '#f97316',
}

PIE_COLORS = ['#8b5cf6', '#06b6d4', '#f59e0b', '#10b981', '#ef4444', '#ec4899', '#6366f1', '#14b8a6']

GRADIENT_SCALE = [[0, '#2d1b4e'], [0.5, '#7c3aed'], [1, '#06b6d4']]
PURPLE_SCALE = [[0, '#1a0a2e'], [0.5, '#6d28d9'], [1, '#a78bfa']]

BASE_LAYOUT = dict(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(13,13,26,0.5)',
    font=dict(family='Outfit, sans-serif', size=12, color='#c0c0e0'),
)

GRID_STYLE = dict(gridcolor='rgba(139,92,246,0.1)')

CSV_PATH = "nuclear_explosions.csv"
