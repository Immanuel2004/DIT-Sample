import streamlit as st
from chains.insight_chain import generate_autonomous_insights
from dotenv import load_dotenv



def render_insights_tab():
    st.title("🔍 Autonomous Insight Generator")

    if (
        st.session_state.get("df") is None
        and st.session_state.get("df1") is None
        and st.session_state.get("df2") is None
    ):
        st.warning("⚠️ Please upload at least one dataset to begin.")
        return

    # Build available dataset options
    available_datasets = []
    if st.session_state.get("df") is not None:
        available_datasets.append("Single Dataset")
    if st.session_state.get("df1") is not None:
        available_datasets.append("Dataset A")
    if st.session_state.get("df2") is not None:
        available_datasets.append("Dataset B")

    selected_dataset = st.radio("Select Dataset for Insights", available_datasets, horizontal=True)

    # Pick correct DataFrame
    if selected_dataset == "Single Dataset":
        selected_df = st.session_state.df
    elif selected_dataset == "Dataset A":
        selected_df = st.session_state.df1
    else:
        selected_df = st.session_state.df2

    if selected_df is not None:
        with st.expander(f"📄 {selected_dataset} Preview"):
            st.dataframe(selected_df.head(), use_container_width=True)

        if st.button(f"🚀 Generate Insights for {selected_dataset}"):
            cols = selected_df.columns.tolist()
            sample_rows = selected_df[cols].sample(min(5, len(selected_df))).to_dict(orient="records")

            # Store insight output in the right session key
            if selected_dataset == "Dataset A":
                st.session_state["insight_output_1"] = generate_autonomous_insights(cols, sample_rows)
            elif selected_dataset == "Dataset B":
                st.session_state["insight_output_2"] = generate_autonomous_insights(cols, sample_rows)
            else:
                st.session_state["insight_output"] = generate_autonomous_insights(cols, sample_rows)

        # Pick correct insight output key
        if selected_dataset == "Dataset A":
            output_key = "insight_output_1"
        elif selected_dataset == "Dataset B":
            output_key = "insight_output_2"
        else:
            output_key = "insight_output"

        if st.session_state.get(output_key):
            st.markdown(f"#### 🧠 Insights for {selected_dataset}")
            st.markdown(st.session_state[output_key])
    else:
        st.warning(f"⚠️ {selected_dataset} is not uploaded yet.")
