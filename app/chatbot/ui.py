#app/chatbot.ui.py
import streamlit as st
from app.chatbot.chatbot import build_chatbot_chain

def render_chatbot_ui():
    st.title(" Dubai Property FAQ Chatbot")
    st.markdown("Ask anything about laws, taxes, resale, or managing properties in Dubai.")

    # ⬇️ Question form
    with st.form("faq_form"):
        query = st.text_input(" Ask your question:")
        submitted = st.form_submit_button("Submit")

    if submitted and query:
        chain = build_chatbot_chain()
        with st.spinner("Thinking..."):
            result = chain.run(query)
        st.markdown(f"**Answer:** {result}")


