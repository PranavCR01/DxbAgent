# main.py

import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

from app.roi_calculator.ui import render_roi_ui
from app.chatbot.ui import render_chatbot_ui

st.set_page_config(page_title="Dubai Property Tools", layout="wide")

# Sidebar content
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose Tool", [" ROI Calculator", " FAQ Chatbot"])

# Extra sidebar links

    # ℹ️ Sidebar links
st.sidebar.markdown("""
### Moving to Dubai? Explore:
- [Quality of Life](https://www.numbeo.com/quality-of-life/in/Dubai)
- [Cost of Living](https://www.numbeo.com/cost-of-living/in/Dubai)
- [Crime Rate](https://www.numbeo.com/crime/in/Dubai)
- [Healthcare](https://www.numbeo.com/health-care/in/Dubai)
- [Traffic](https://www.numbeo.com/traffic/in/Dubai)
""", unsafe_allow_html=True)

# === QR Code for contact info ===
st.sidebar.markdown("**Save My Contact:**")

vcard = """BEGIN:VCARD
VERSION:3.0
FN:Pranav CR (Dubai Properties)
TEL:+971500000000
EMAIL:prc@illinois.edu
END:VCARD
"""

qr = qrcode.make(vcard)
buffer = BytesIO()
qr.save(buffer, format="PNG")
buffer.seek(0)
st.sidebar.image(Image.open(buffer), caption="Scan to Save Contact", use_container_width=True)

# Render selected page
if app_mode == " ROI Calculator":
    render_roi_ui()
elif app_mode == " FAQ Chatbot":
    render_chatbot_ui()
