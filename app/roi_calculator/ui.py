# roi_calculator/ui.py
import streamlit as st
from app.roi_calculator.calculator import get_all_data, get_filtered_properties, calculate_estimates

INDIAN_CITIES = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad"]

def render_roi_ui():
    st.title(" Real Estate ROI & Rental Yield Calculator")
    st.markdown("Estimate your **returns and payback** from property investments in Dubai vs major Indian cities using real market data.")

    rental_mode_ui = st.radio(" Investment Type", ["Rental (long-term)", "Resale (for-sale)"])
    mode = "for-rent" if "Rental" in rental_mode_ui else "for-sale"
    rental_mode_tag = "long-term" if mode == "for-rent" else "resale"

    df = get_all_data(mode)

    budget = st.number_input(" Property Budget (in AED)", min_value=50000, max_value=10000000, step=10000)

    cities = sorted(df[df["rental_mode"] == rental_mode_tag]["city"].dropna().unique())
    city = st.selectbox(" City of Investment", cities)

    property_types = sorted(df[(df["city"] == city) & (df["rental_mode"] == rental_mode_tag)]["type"].dropna().unique())
    property_type = st.selectbox(" Property Type", property_types)

    compare_india = st.checkbox("Compare with India returns")
    comparison_mode = None
    if compare_india:
        comparison_mode = st.radio(" India Comparison Mode", ["India Equivalent Property", "Same AED Budget"])

    if st.button("Calculate ROI"):
        main_df = get_filtered_properties(df, city, property_type, rental_mode_tag)
        results_main = calculate_estimates(budget, main_df)

        india_results = None
        india_df = None
        india_equiv_price = None

        if compare_india:
            india_df = df[
                (df["city"].isin(INDIAN_CITIES)) &
                (df["type"].str.lower() == property_type.lower()) &
                (df["rental_mode"].str.lower() == rental_mode_tag.lower())
            ]
            if comparison_mode == "India Equivalent Property":
                india_equiv_price = india_df["price"].mean()
            india_results = calculate_estimates(
                budget, india_df, override_budget=india_equiv_price
            )

        st.header(" Estimated Returns")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"🇦🇪 {city}")
            if results_main["yield"] is None:
                st.warning(f"No listings found for {city}.")
            else:
                st.markdown(f"- **Projected Yield:** `{results_main['yield']}%`")
                st.markdown(f"- **Estimated ROI:** `{results_main['roi']}%`")
                st.markdown(f"- **Payback Period:** `{results_main['payback_years']} years`")

        with col2:
            if compare_india:
                st.subheader("🇮🇳 India")
                if india_results["yield"] is None:
                    st.warning("No India listings matched the filters.")
                else:
                    if comparison_mode == "India Equivalent Property":
                        st.caption(f"Using avg India price of **AED {round(india_equiv_price, 2):,.0f}**")
                    else:
                        st.caption("Using same AED budget as Dubai")
                    st.markdown(f"- **Projected Yield:** `{india_results['yield']}%`")
                    st.markdown(f"- **Estimated ROI:** `{india_results['roi']}%`")
                    st.markdown(f"- **Payback Period:** `{india_results['payback_years']} years`")

        with st.expander(" View Matching Listings (Sample)"):
            st.dataframe(main_df[["Neighborhood", "price_per_sqm", "monthly_rent"]].head(10))
