# Vastgoedzoeker Webtool – Apify JSON integratie

import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Vastgoedzoeker", layout="wide")

# API endpoint van Apify dataset (demo)
APIFY_DATASET_URL = "https://api.apify.com/v2/datasets/8uWYDZ9AbBP5gWKnq/items?clean=true"
