## outreach/ ui.py

import streamlit as st
import pandas as pd
from generator import get_or_create_template

st.set_page_config(page_title="AI Outreach Generator", layout="wide")

st.title("AI Outreach Assistant (Optimized for 1000s of Leads)")
st.write("Upload your lead CSV with columns: name, city, tone_a, tone_b (optional), usp_a, usp_b (optional).")
st.write("Generates personalized WhatsApp-ready messages with A/B variants using {name} and {city} placeholders.")

uploaded_file = st.file_uploader("Upload CSV (name, city, tone_a, tone_b, usp_a, usp_b)", type="csv")
use_whatsapp_format = st.checkbox("Format for WhatsApp export (line breaks as %0A)", value=True)

def format_whatsapp(message):
    return message.replace("\n", "%0A")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success(f"Uploaded {len(df)} leads")

    output = []
    progress = st.progress(0)
    total = len(df) * 2

    for i, row in df.iterrows():
        name = str(row.get("name", "Friend"))
        city = str(row.get("city", "your city"))
        tone_a = str(row.get("tone_a", "professional"))
        tone_b = str(row.get("tone_b", tone_a))
        usp_a = str(row.get("usp_a", "high ROI"))
        usp_b = str(row.get("usp_b", usp_a))

        for variant, tone, usp in zip(['A', 'B'], [tone_a, tone_b], [usp_a, usp_b]):
            template = get_or_create_template(city, tone, usp)
            message = template.replace("{name}", name).replace("{city}", city)
            if use_whatsapp_format:
                message = format_whatsapp(message)

            output.append({
                "name": name,
                "city": city,
                "tone": tone,
                "usp": usp,
                "ab_variant": variant,
                "message": message
            })
            progress.progress(len(output) / total)

    result_df = pd.DataFrame(output)
    st.dataframe(result_df)

    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download A/B Messages", data=csv, file_name="ab_test_outreach_messages.csv", mime='text/csv')
