# Vastgoedzoeker Webtool – debug + verbeterde scraping ERA

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Streamlit configuratie
st.set_page_config(page_title="Vastgoedzoeker", layout="wide")

# Zoekcriteria
MAX_PRIJS = 750000
MIN_SLAAPKAMERS = 3
POSTCODES = ["1860", "1861", "1785", "1730", "1780"]

# ---------------------- IMMOWEB ----------------------
def scrape_immoweb():
    results = []
    # Tijdelijk uitschakelen tot JS scraping werkt
    return results

# ---------------------- ERA (met filters via zoek-URL) ----------------------
def scrape_era():
    results = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for postcode in POSTCODES:
        url = f"https://www.era.be/nl/te-koop?page=1&search={postcode}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        for listing in soup.select(".property-item"):
            try:
                adres = listing.select_one(".property-title").get_text(strip=True)
                prijs = listing.select_one(".property-price").get_text(strip=True)
                link_tag = listing.find("a", href=True)
                link = "https://www.era.be" + link_tag['href'] if link_tag else ""
                tuin = "Onbekend"
                slaapkamers = MIN_SLAAPKAMERS
                results.append({
                    "Datum": datetime.today().strftime('%Y-%m-%d'),
                    "Website": "ERA",
                    "Adres": adres,
                    "Prijs": prijs,
                    "Slaapkamers": slaapkamers,
                    "Tuin": tuin,
                    "Link": link
                })
            except:
                continue
    return results

# ---------------------- DEWAELE ----------------------
def scrape_dewaele():
    results = []
    url = "https://www.dewaele.com/nl/koop"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for listing in soup.select(".property-tile"):
        try:
            adres = listing.select_one(".property-tile__title").get_text(strip=True)
            prijs = listing.select_one(".property-tile__price").get_text(strip=True)
            link_tag = listing.find("a", href=True)
            link = "https://www.dewaele.com" + link_tag['href'] if link_tag else ""
            tuin = "Onbekend"
            slaapkamers = MIN_SLAAPKAMERS
            results.append({
                "Datum": datetime.today().strftime('%Y-%m-%d'),
                "Website": "Dewaele",
                "Adres": adres,
                "Prijs": prijs,
                "Slaapkamers": slaapkamers,
                "Tuin": tuin,
                "Link": link
            })
        except:
            continue
    return results

# ---------------------- GEGEVENS OPHALEN ----------------------
with st.spinner("Zoekertjes aan het ophalen van ERA & Dewaele..."):
    data = scrape_era() + scrape_dewaele()
    df = pd.DataFrame(data)

# ---------------------- STREAMLIT UI ----------------------
st.title("🏡 Nieuwe huizen in jouw regio")
st.markdown("Bekijk hier dagelijks nieuwe huizen in jouw regio met jouw criteria:")

st.write("Aantal resultaten gevonden:", len(df))
st.write(df)

# ---------------------- TABEL TONEN ----------------------
if not df.empty:
    st.dataframe(df, use_container_width=True)
    for i, row in df.iterrows():
        st.markdown(f"[{row['Adres']}]({row['Link']}) - {row['Prijs']} - {row['Slaapkamers']} slk - Tuin: {row['Tuin']} ({row['Website']})")
else:
    st.info("Geen resultaten gevonden voor vandaag met de opgegeven criteria.")
