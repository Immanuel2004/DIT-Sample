import streamlit as st

def render_data_preview():
    st.markdown("---")
    st.subheader("Dataset Preview")

    if st.session_state.df1 is not None:
        st.markdown("### Dataset A")
        df = st.session_state.df1
        cols = st.session_state.selected_cols_1 or df.columns.tolist()
        st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
        st.write("**Selected Columns:**", ", ".join(cols))
        st.dataframe(df[cols].head())

    if st.session_state.df2 is not None:
        st.markdown("### Dataset B")
        df = st.session_state.df2
        cols = st.session_state.selected_cols_2 or df.columns.tolist()
        st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
        st.write("**Selected Columns:**", ", ".join(cols))
        st.dataframe(df[cols].head())
