from fpdf import FPDF
import tempfile
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Dynamic Impact Tool Report", ln=True, align="C")
        self.ln(5)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_text_color(0, 0, 128)
        self.cell(0, 10, title, ln=True, align="L")
        self.ln(2)

    def chapter_body(self, text):
        self.set_font("Arial", "", 11)
        self.set_text_color(0)
        self.multi_cell(0, 8, text)
        self.ln()

def generate_pdf_report(insights, chat_logs):
    pdf = PDF()
    pdf.add_page()

    if insights:
        pdf.chapter_title("📝 Dataset Insight Summary")
        pdf.chapter_body(insights)

    if chat_logs:
        pdf.chapter_title("💬 Chat History")
        for item in chat_logs:
            user = item.get("user", "")
            assistant = item.get("assistant", {}).get("response", item.get("assistant", ""))
            pdf.set_font("Arial", "B", 11)
            pdf.multi_cell(0, 8, f"User: {user}")
            pdf.set_font("Arial", "", 11)
            pdf.multi_cell(0, 8, f"AI: {assistant}")
            pdf.ln(3)

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            pdf.output(tmp_file.name)
            return tmp_file.name
    except Exception as e:
        print(f"[PDF ERROR] {e}")
        return None
