import os
import streamlit as st
from utils.pdf_exporter import generate_pdf_report
from dotenv import load_dotenv

load_dotenv()

def render_export_tab():
    st.title("📤 Export Summary")

    has_summary_1 = bool(st.session_state.get("summary_output_1"))
    has_summary_2 = bool(st.session_state.get("summary_output_2"))
    has_chat_logs = bool(st.session_state.get("chat_history")) or bool(st.session_state.get("compare_chat"))

    if has_summary_1 or has_summary_2:
        st.markdown("### 🧾 Final Summary")

        combined = ""
        if has_summary_1:
            combined += "### Dataset A Summary\n" + st.session_state.summary_output_1 + "\n\n"
        if has_summary_2:
            combined += "### Dataset B Summary\n" + st.session_state.summary_output_2

        st.text_area("📑 Combined Summary", combined, height=300)

        if st.button("🖨️ Generate PDF Report"):
            path = generate_pdf_report(
                insights=combined,
                chat_logs=st.session_state.chat_history + st.session_state.compare_chat
            )
            if path and os.path.exists(path):
                with open(path, "rb") as f:
                    st.download_button("⬇ Download Report", f, file_name="summary_report.pdf")
            else:
                st.error("❌ PDF generation failed.")

    else:
        st.info("⚠️ No summary data available. Please generate summaries from the previous tabs.")
