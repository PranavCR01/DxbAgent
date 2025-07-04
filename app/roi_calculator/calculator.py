#roi_calculator/ calculator.py

import pandas as pd
from app.roi_calculator.bayut_fetcher import get_dubai_data

INR_TO_AED = 0.044

def load_csv_data(path):
    df = pd.read_csv(path, encoding="ISO-8859-1")
    df = df.rename(columns={
        "City": "city",
        "Neighborh": "Neighborhood",
        "Type": "type",
        "Monthly Rent Long-Term": "monthly_rent",
        "Price (AED)": "price",
        "Rental Mode": "rental_mode"
    })

    df["price"] = df["price"].astype(str).str.replace('[^0-9.]', '', regex=True)
    df["monthly_rent"] = df["monthly_rent"].astype(str).str.replace('[^0-9.]', '', regex=True)

    indian_cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad"]
    df["is_india"] = df["city"].isin(indian_cities)

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["monthly_rent"] = pd.to_numeric(df["monthly_rent"], errors="coerce")

    df.loc[df["is_india"], "price"] *= INR_TO_AED
    df.loc[df["is_india"], "monthly_rent"] *= INR_TO_AED

    if "rental_mode" not in df.columns or df["rental_mode"].isnull().all():
        df["rental_mode"] = "long-term"

    df["price_per_sqm"] = df["price"] / 100
    return df.drop(columns=["is_india"])

def get_all_data(mode="for-sale"):
    dubai_df = get_dubai_data(mode)
    if dubai_df.empty:
        print(" Falling back to CSV data...")
        return load_csv_data("data/real_estate_listings.csv")
    return dubai_df

def get_filtered_properties(df, city, property_type, rental_strategy):
    return df[
        (df["city"].str.lower() == city.lower()) &
        (df["type"].str.lower() == property_type.lower()) &
        (df["rental_mode"].str.lower() == rental_strategy.lower())
    ]

def calculate_estimates(budget, listings_df, override_budget=None):
    if listings_df.empty:
        return {"yield": None, "roi": None, "payback_years": None, "used_budget": None}

    avg_price_per_sqm = listings_df["price_per_sqm"].mean()
    avg_rent_per_month = listings_df["monthly_rent"].mean()

    budget_used = override_budget if override_budget else budget
    estimated_annual_rent = avg_rent_per_month * 12
    rental_yield = (estimated_annual_rent / budget_used) * 100
    roi = rental_yield
    payback_years = budget_used / estimated_annual_rent

    return {
        "yield": round(rental_yield, 2),
        "roi": round(roi, 2),
        "payback_years": round(payback_years, 2),
        "used_budget": round(budget_used, 2)
    }
