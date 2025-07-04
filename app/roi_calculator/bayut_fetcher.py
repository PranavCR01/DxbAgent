# roi_calculator/bayut_fetcher.py

import os
import pandas as pd
import requests
from datetime import datetime, timedelta

CACHE_FILE = "data/bayut_cache.parquet"
FRESHNESS_DAYS = 14
API_URL = "https://bayut-api1.p.rapidapi.com/properties_search"
API_KEY = "9a93a239f9msh18f27200e69485dp1a05d9jsn766c6d79faf0"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "bayut-api1.p.rapidapi.com",
    "Content-Type": "application/json"
}

def is_cache_fresh():
    return os.path.exists(CACHE_FILE) and (
        datetime.now() - datetime.fromtimestamp(os.path.getmtime(CACHE_FILE))
    ) < timedelta(days=FRESHNESS_DAYS)

def fetch_from_api(mode="for-sale"):
    print(f"🔄 Cache stale or missing. Fetching fresh data for mode: {mode}")
    
    payload = {
    "purpose": mode,
    "category": "apartments",
    "locations_ids": [2],  # Dubai
    "index": "popular",
    # remove tight filters to allow more matches
    "price_min": 10000,
    "price_max": 9999999,
}


    querystring = {"page": "0", "langs": "en"}

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, params=querystring)
        print(f"📡 API call status: {response.status_code} | Mode: {mode}")

        if response.status_code == 200:
            hits = response.json().get("hits", [])
            listings = []

            for item in hits:
                area = item.get("area", 100)
                listings.append({
                    "city": "Dubai",
                    "Neighborhood": item.get("location", [{}])[-1].get("name", "Unknown"),
                    "type": item.get("title", "").split()[0] or "Apartment",
                    "monthly_rent": item.get("price", 0) / 12 if mode == "for-rent" else None,
                    "price": item.get("price", 0),
                    "rental_mode": "long-term" if mode == "for-rent" else "resale",
                    "price_per_sqm": item.get("price", 0) / (area if area else 100)
                })

            df = pd.DataFrame(listings)
            if not df.empty:
                df.to_parquet(CACHE_FILE, index=False)
                print("💾 Cached to", CACHE_FILE)
            return df
        else:
            print(f"❌ Error: {response.status_code} | {response.text}")
            return pd.DataFrame()

    except Exception as e:
        print(f"❌ API Exception: {e}")
        return pd.DataFrame()

def get_dubai_data(mode="for-sale"):
    if is_cache_fresh():
        print("📂 Loading from cache...")
        return pd.read_parquet(CACHE_FILE)
    return fetch_from_api(mode)
