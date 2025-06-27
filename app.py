import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from components.sidebar import render_sidebar
from components.summary_section import render_summary_tab
from components.insights_section import render_insights_tab
from components.comparison_section import render_comparison_tab
from components.export_section import render_export_tab
from components.visualizations_section import render_visualizations_tab
from components.chatbot_section import render_chat_interface

from utils.state_manager import init_session_state
from utils.chat_history_manager import save_chat_history, load_chat_history
from utils.file_loader import load_data

from auth import login

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# 🌍 Load environment variables
load_dotenv()

# ⚙️ Streamlit app config
st.set_page_config(page_title="Dynamic Impact Tool", layout="wide")

# 🧠 Initialize session state
init_session_state()

# 🔁 Default session state setup
session_defaults = {
    "df": None,
    "df1": None,
    "df2": None,
    "summary_output_1": "",
    "summary_output_2": "",
    "insight_output_1": "",
    "insight_output_2": "",
    "comparison_result": "",
    "compare_chat": [],
    "chat_history": [],
    "visual_suggestions": [],
}

for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# 📂 Path input upload for single dataset
# st.sidebar.markdown("---")
# st.sidebar.markdown("**📁 Load Dataset from Path**")
# path_input = st.sidebar.text_input("Enter path to CSV/Excel file")

# if path_input:
#     try:
#         st.session_state.df = load_data(path_input)
#         st.sidebar.success("✅ Dataset loaded successfully.")
#     except Exception as e:
#         st.sidebar.error(f"❌ Failed to load dataset: {e}")

path_input = None 

# 📍 Sidebar section selector
section = render_sidebar()

# 🧩 Section-based view rendering
if section == "Single Dataset":
    render_summary_tab()
    render_insights_tab()
    render_visualizations_tab()

    if st.session_state.df is not None:
        render_chat_interface(context="single", df=st.session_state.df)

elif section == "Dataset Comparison":
    render_comparison_tab()  # contains internal chat interface call with merged_df

elif section == "Summary & Export":
    render_export_tab()

# 💾 Save chat history
save_chat_history("chat_history.json", st.session_state.chat_history)


