import streamlit as st
import pandas as pd
from datetime import datetime
from chains.comparison_chain import compare_datasets
from utils.comparator import quick_dataframe_comparison
from utils.file_loader import load_data
from utils.visualizer import (
    visualize_comparison_side_by_side,
    visualize_comparison_overlay,
    visualize_from_llm_response,
)
from utils.chat_handler import handle_user_query_dynamic


def render_comparison_tab():
    st.title("🆚 Dataset Comparison")
    col1, col2 = st.columns(2)

    # Dataset A Upload + Path
    with col1:
        uploaded_file1 = st.file_uploader("Upload Dataset A", type=["csv", "xlsx"], key="fileA")
        dataset_a_path = st.text_input("Or enter path/URL for Dataset A", key="pathA")

        if uploaded_file1:
            st.session_state.df1 = load_data(uploaded_file1)
        elif dataset_a_path:
            try:
                st.session_state.df1 = load_data(dataset_a_path)
            except Exception as e:
                st.error(f"❌ Failed to load Dataset A: {e}")

    # Dataset B Upload + Path
    with col2:
        uploaded_file2 = st.file_uploader("Upload Dataset B", type=["csv", "xlsx"], key="fileB")
        dataset_b_path = st.text_input("Or enter path/URL for Dataset B", key="pathB")

        if uploaded_file2:
            st.session_state.df2 = load_data(uploaded_file2)
        elif dataset_b_path:
            try:
                st.session_state.df2 = load_data(dataset_b_path)
            except Exception as e:
                st.error(f"❌ Failed to load Dataset B: {e}")

    if st.session_state.df1 is not None and st.session_state.df2 is not None:
        df1 = st.session_state.df1
        df2 = st.session_state.df2
        cols1 = df1.columns.tolist()
        cols2 = df2.columns.tolist()
        common_cols = list(set(cols1).intersection(set(cols2)))

        if len(common_cols) < 4:
            st.warning("⚠️ At least 4 common columns are required for meaningful comparison.")
            return

        st.subheader("🤖 AI Comparison")
        if st.button("Run AI Comparison"):
            try:
                rows1 = df1[common_cols].sample(min(5, len(df1))).to_dict(orient="records")
                rows2 = df2[common_cols].sample(min(5, len(df2))).to_dict(orient="records")

                comparison = compare_datasets(common_cols, common_cols, rows1, rows2)
                st.session_state.comparison_result = comparison
                st.success("✅ AI Comparison completed successfully.")
            except Exception as e:
                st.error(f"❌ Error during comparison: {e}")

        if st.session_state.get("comparison_result"):
            st.markdown("### 🧠 AI-Generated Comparison Result")
            st.markdown(st.session_state.comparison_result)

        st.subheader("📊 Structural Overview")
        structural = quick_dataframe_comparison(df1, df2)
        st.json(structural)

        # Visualization Controls
        st.subheader("📈 Visual Comparison")
        col_x, col_y, col_type = st.columns(3)
        with col_x:
            x_axis = st.selectbox("X Axis", df1.columns, key="x_axis")
        with col_y:
            y_axis = st.selectbox("Y Axis", df1.columns, key="y_axis")
        with col_type:
            chart_type = st.selectbox("Chart Type", ["bar", "line", "scatter"])

        view = st.radio("Comparison Type", ["Overlay", "Side-by-Side"])

        if view == "Side-by-Side":
            fig1, fig2 = visualize_comparison_side_by_side(df1, df2, x_axis, y_axis, chart_type)
            col1, col2 = st.columns(2)
            with col1:
                if fig1: st.plotly_chart(fig1, use_container_width=True)
            with col2:
                if fig2: st.plotly_chart(fig2, use_container_width=True)
        else:
            fig, explanation = visualize_comparison_overlay(df1, df2, x_axis, y_axis, chart_type=chart_type)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                st.caption(explanation)

        # Chat Interface
        st.divider()
        st.markdown("### 💬 Chat About This Comparison")

        if st.button("🗑️ Clear Chat History", key="clear_compare_chat"):
            st.session_state.compare_chat = []
            st.rerun()

        for chat in st.session_state.compare_chat:
            with st.chat_message("user"):
                st.markdown(chat["user"])
            with st.chat_message("assistant"):
                st.markdown(chat["assistant"].get("response", chat["assistant"]))

        compare_query = st.chat_input("Ask a question about both datasets...")
        if compare_query:
            with st.chat_message("user"):
                st.markdown(compare_query)
            with st.chat_message("assistant"):
                merged_df = pd.concat([df1, df2], ignore_index=True)
                merged_df["__dataset__"] = ["Dataset A"] * len(df1) + ["Dataset B"] * len(df2)
                model = st.session_state.get("model_source", "groq")
                result = handle_user_query_dynamic(compare_query, merged_df, model_source=model)

                st.session_state.compare_chat.append({
                    "timestamp": datetime.now().isoformat(),
                    "user": compare_query,
                    "assistant": result
                })

                if isinstance(result["response"], dict) and "chart_type" in result["response"]:
                    fig = visualize_from_llm_response(merged_df, compare_query, result["response"])
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("⚠️ Could not generate visualization from chat.")
                else:
                    st.markdown(result["response"])

                if result.get("follow_ups"):
                    st.markdown("**💡 Follow-up Questions:**")
                    for i, q in enumerate(result["follow_ups"], 1):
                        st.markdown(f"- {q}")

    else:
        st.info("📂 Please upload or link both datasets to begin.")