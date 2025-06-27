import streamlit as st

def init_session_state():
    defaults = {
        # Dataset A
        "df1": None,
        "df1_cols": [],
        "selected_cols_1": [],
        "df1_loaded": False,

        # Dataset B
        "df2": None,
        "df2_cols": [],
        "selected_cols_2": [],
        "df2_loaded": False,

        # Summary
        "summary_output_1": "",
        "summary_output_2": "",

        # Insights
        "insight_output_1": "",
        "insight_output_2": "",
        "insight_categories_1": [],
        "insight_categories_2": [],
        "selected_category_1": None,
        "selected_category_2": None,
        "category_insights_1": {},
        "category_insights_2": {},

        # Comparison
        "comparison_result": "",
        "comparison_visual": None,

        # Visuals
        "visual_output_1": "",
        "visual_output_2": "",

        # UI
        "selected_tab": "Summary",

        # File Hashes
        "file1_hash": None,
        "file2_hash": None
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_dataset_a_state():
    keys_to_reset = {
        "df1": None,
        "df1_cols": [],
        "selected_cols_1": [],
        "summary_output_1": "",
        "insight_output_1": "",
        "insight_categories_1": [],
        "selected_category_1": None,
        "category_insights_1": {},
        "visual_output_1": "",
        "df1_loaded": False,
        "file1_hash": None,
    }
    for key, value in keys_to_reset.items():
        st.session_state[key] = value


def reset_dataset_b_state():
    keys_to_reset = {
        "df2": None,
        "df2_cols": [],
        "selected_cols_2": [],
        "summary_output_2": "",
        "insight_output_2": "",
        "insight_categories_2": [],
        "selected_category_2": None,
        "category_insights_2": {},
        "visual_output_2": "",
        "df2_loaded": False,
        "file2_hash": None,
    }
    for key, value in keys_to_reset.items():
        st.session_state[key] = value
