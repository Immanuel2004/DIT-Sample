# components/sidebar.py

import streamlit as st
from dotenv import load_dotenv

load_dotenv
def render_sidebar():
    with st.sidebar:
        st.title("Dynamic Impact Tool")
        st.markdown("## :compass: Navigation")
        section = st.radio(
            "Choose a section",
            ["Single Dataset", "Dataset Comparison", "Summary & Export"],
            key="selected_tab"
        )

        st.markdown("---")
        st.markdown("## Upload Info")
        st.caption("Accepts CSV, Excel, or JSON (≤ 200MB)")
        
        st.markdown("## Model")
        st.markdown("Running on: **GROQ (LLaMA3)**")

        return section
