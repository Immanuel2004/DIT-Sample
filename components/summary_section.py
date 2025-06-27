import streamlit as st
from utils.file_loader import load_data
from chains.summary_chain import generate_summary
from dotenv import load_dotenv

load_dotenv()

def render_summary_tab():
    st.title("📝 Dataset Summary")

    if st.session_state.df is None:
        # File uploader
        uploaded_file = st.file_uploader("Upload a dataset (CSV, Excel, JSON)", type=["csv", "xlsx", "json"])

        # Path input
        st.markdown("**Or enter dataset path or URL:**")
        dataset_path = st.text_input("Path or URL to dataset")

        if uploaded_file:
            try:
                st.session_state.df = load_data(uploaded_file)
                st.session_state.df_selected = st.session_state.df
                st.success("✅ Dataset uploaded and loaded successfully.")
            except Exception as e:
                st.error(f"❌ Failed to load uploaded file: {e}")

        elif dataset_path:
            try:
                st.session_state.df = load_data(dataset_path)
                st.session_state.df_selected = st.session_state.df
                st.success("✅ Dataset loaded from path successfully.")
            except Exception as e:
                st.error(f"❌ Failed to load dataset from path: {e}")

    if st.session_state.df is not None:
        df = st.session_state.df
        with st.expander("📄 Dataset Preview"):
            st.dataframe(df.head(), use_container_width=True)

        if st.button("📊 Generate Summary"):
            cols = df.columns.tolist()
            sample = df[cols].sample(min(5, len(df))).to_dict(orient="records")
            st.session_state.summary_output_1 = generate_summary(cols, sample)

        if st.session_state.summary_output_1:
            st.markdown("### 🧠 Dataset Summary")
            st.markdown(st.session_state.summary_output_1)

    else:
        st.info("📂 Upload a file or provide a path to begin summary analysis.")
