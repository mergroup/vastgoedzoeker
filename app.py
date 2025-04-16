# Vastgoedzoeker Webtool – Apify JSON integratie

import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Vastgoedzoeker", layout="wide")

# API endpoint van Apify dataset (demo)
APIFY_DATASET_URL = "https://api.apify.com/v2/datasets/NbICxEf2uPH0UunDc/items?clean=true"

# ---------------------- DATA OPHALEN ----------------------
def fetch_apify_results():
    try:
        response = requests.get(APIFY_DATASET_URL)
        response.raise_for_status()
        data = response.json()
        results = []
        for item in data:
            results.append({
                "Datum": datetime.today().strftime('%Y-%m-%d'),
                "Website": item.get("source", "Onbekend"),
                "Adres": item.get("address", "Onbekend"),
                "Prijs": item.get("price", "Onbekend"),
                "Slaapkamers": item.get("bedrooms", "?"),
                "Tuin": item.get("garden", "?"),
                "Link": item.get("url", "")
            })
        return pd.DataFrame(results)
    except Exception as e:
        st.error(f"Fout bij ophalen van Apify: {e}")
        return pd.DataFrame()

# ---------------------- UI ----------------------
st.title("🏡 Nieuwe huizen in jouw regio")
st.markdown("Bekijk hier dagelijks nieuwe huizen in jouw regio met jouw criteria:")

with st.spinner("Zoekertjes aan het laden via Apify..."):
    df = fetch_apify_results()

st.write("Aantal resultaten gevonden:", len(df))
st.write(df)

if not df.empty:
    st.dataframe(df, use_container_width=True)
    for i, row in df.iterrows():
        st.markdown(f"[{row['Adres']}]({row['Link']}) - {row['Prijs']} - {row['Slaapkamers']} slk - Tuin: {row['Tuin']} ({row['Website']})")
else:
    st.info("Geen resultaten gevonden voor vandaag met de opgegeven criteria.")
