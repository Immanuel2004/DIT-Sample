import streamlit as st
from utils.visualizer import visualize_from_llm_response
from chains.visual_suggestion_chain import suggest_visualizations
import streamlit as st
from utils.visualizer import (
    visualize_from_llm_response,
    visualize_comparison_side_by_side,
    visualize_comparison_overlay
)
from dotenv import load_dotenv

load_dotenv()


def render_visualizations_tab():
    st.title("AI-Powered Visual Suggestions")

    if st.session_state.df is None:
        st.warning("Please upload a dataset in the Upload & Insights section.")
        return

    with st.expander("Dataset Preview"):
        st.dataframe(st.session_state.df.head(), use_container_width=True)

    if st.button("✨ Suggest Visualizations"):
        with st.spinner("Generating suggestions..."):
            try:
                suggestions = suggest_visualizations(st.session_state.df.to_csv(index=False))
                st.session_state.visual_suggestions = suggestions
                st.success("Suggestions generated successfully.")
            except Exception as e:
                st.error(f"Failed to generate suggestions: {e}")

    if st.session_state.get("visual_suggestions"):
        st.subheader("Suggested Visualizations")
        for i, suggestion in enumerate(st.session_state.visual_suggestions):
            with st.expander(f"Suggestion {i+1}: {suggestion['title']}"):
                st.markdown(suggestion["description"])
                if st.button(f"Generate Chart {i+1}", key=f"viz_{i}"):
                    fig = visualize_from_llm_response(
                        st.session_state.df,
                        suggestion["title"],
                        suggestion
                    )
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Could not generate chart.")