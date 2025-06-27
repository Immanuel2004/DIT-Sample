import streamlit as st

def init_session_state():
    session_defaults = {
        "df": None,
        "df_selected": None,
        "selected_cols": [],
        "chat_history": [],
        "insights": "",
        "visual_suggestions": [],

        "df1": None,
        "df2": None,
        "comparison_result": "",
        "compare_chat": [],
        
        "summary_output_1": "",
        "summary_output_2": "",
        "insight_output_1": "",
        "insight_output_2": "",

        "uploaded_file": None,
        "file1": None,
        "file2": None,
    }

    for key, value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
