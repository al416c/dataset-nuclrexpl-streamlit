import pandas as pd
import streamlit as st
from config.settings import COUNTRY_TRANSLATION, CSV_PATH


@st.cache_data
def load_data():
    return pd.read_csv(CSV_PATH)


def prepare_data(df):
    df['WEAPON SOURCE COUNTRY'] = df['WEAPON SOURCE COUNTRY'].replace(COUNTRY_TRANSLATION)
    df = df.assign(Yield_Average=(df['Data.Yeild.Lower'] + df['Data.Yeild.Upper']) / 2)
    df['Decade'] = df['Date.Year'].apply(lambda x: f"{(x // 10) * 10}s")
    df['Yield_Category'] = df['Yield_Average'].map(
        lambda x: '🟢 Faible (<20 kt)' if x < 20 else ('🟡 Moyen (20-1000 kt)' if x < 1000 else '🔴 Élevé (>1000 kt)')
    )
    return df


def filter_data(df, countries, years, yield_cats):
    return df[
        (df['WEAPON SOURCE COUNTRY'].isin(countries)) &
        (df['Date.Year'] >= years[0]) &
        (df['Date.Year'] <= years[1]) &
        (df['Yield_Category'].isin(yield_cats))
    ]
