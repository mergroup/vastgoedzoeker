# Vastgoedzoeker Webtool – verbeterde scraping ERA + debug

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

st.set_page_config(page_title="Vastgoedzoeker", layout="wide")

MAX_PRIJS = 750000
MIN_SLAAPKAMERS = 3
POSTCODES = ["1860", "1861", "1785", "1730", "1780"]

# ---------------------- ERA ----------------------
def scrape_era():
    results = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for postcode in POSTCODES:
        url = f"https://www.era.be/nl/te-koop/{postcode}?page=1"
        st.write(f"Ophalen van ERA: {url}")
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            listings = soup.find_all("div", class_="views-row")
            st.write(f"{len(listings)} resultaten gevonden voor {postcode} op ERA")

            for listing in listings:
                try:
                    title_tag = listing.find("div", class_="title")
                    adres = title_tag.get_text(strip=True) if title_tag else "Onbekend"
                    prijs_tag = listing.find("div", class_="prijs")
                    prijs = prijs_tag.get_text(strip=True) if prijs_tag else "Onbekend"
                    link_tag = listing.find("a", href=True)
                    link = "https://www.era.be" + link_tag['href'] if link_tag else ""

                    results.append({
                        "Datum": datetime.today().strftime('%Y-%m-%d'),
                        "Website": "ERA",
                        "Adres": adres,
                        "Prijs": prijs,
                        "Slaapkamers": MIN_SLAAPKAMERS,
                        "Tuin": "Onbekend",
                        "Link": link
                    })
                except Exception as e:
                    st.write(f"Fout in listing: {e}")
                    continue
        except Exception as e:
            st.error(f"Fout bij ophalen ERA: {e}")
    return results

# ---------------------- GEGEVENS OPHALEN ----------------------
with st.spinner("Zoekertjes aan het ophalen van ERA..."):
    data = scrape_era()
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
