import streamlit as st
from fpdf import FPDF
from datetime import date

# Page config
st.set_page_config(page_title="TRAY Consent Form Generator")
st.title("📝 TRAY Media Consent Form Generator")

# Inputs
name = st.text_input("Full Name / الاسم الكامل")
selected_date = st.date_input("Select the date / اختر التاريخ", value=date.today())

# Convert date to string
today_date = selected_date.strftime('%Y-%m-%d')

# PDF generation function
def generate_bilingual_pdf(english_lines, arabic_lines, filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font("NotoArabic", '', fname="NotoSansArabic-SemiBold.ttf", uni=True)
    pdf.set_font("NotoArabic", size=12)

    # English page
    pdf.add_page()
    for line in english_lines:
        if line == "TABLE_BLOCK":
            pdf.ln(8)
            pdf.cell(40, 10, "Name:", ln=0)
            pdf.cell(80, 10, "_____________________________", ln=0)
            pdf.ln(10)
            pdf.cell(40, 10, "Signature:", ln=0)
            pdf.cell(80, 10, "_____________________________", ln=0)
            pdf.ln(10)
            pdf.cell(40, 10, "Date:", ln=0)
            pdf.cell(80, 10, today_date, ln=1)
            pdf.ln(5)
        else:
            pdf.multi_cell(0, 10, line)

    # Arabic page
    pdf.add_page()
    for line in arabic_lines:
        if line == "TABLE_BLOCK":
            pdf.ln(8)
            pdf.cell(40, 10, "الاسم:", ln=0)
            pdf.cell(80, 10, "_____________________________", ln=0)
            pdf.ln(10)
            pdf.cell(40, 10, "التوقيع:", ln=0)
            pdf.cell(80, 10, "_____________________________", ln=0)
            pdf.ln(10)
            pdf.cell(40, 10, "التاريخ:", ln=0)
            pdf.cell(80, 10, today_date, ln=1)
            pdf.ln(5)
        else:
            pdf.multi_cell(0, 10, line)

    return pdf.output(dest='S').encode('latin-1'), filename

# Button and logic
if st.button("Generate Bilingual Consent PDF"):
    if name:
        # English content
        english_lines = [
            "TRAY Media & Marketing Consent Form",
            "",
            "In signing this form, I grant Company AL-HALLOUL RAQMIYAH AL-RAEDEH For Information Technology (TRAY)",
            "the unrestricted right and permission to record, photograph, and use my name, image, voice, or words",
            "in any media content created for marketing, social media, educational, promotional, or internal use.",
            "",
            "I understand that these materials may be used on websites, social media platforms, printed publications,",
            "and presentations. I acknowledge that I will not receive any compensation or have any rights to review or",
            "approve the final materials.",
            "",
            "By signing below, I consent to TRAY’s use of my content:",
            "TABLE_BLOCK",
            "For questions, contact TRAY Marketing: marketing@tray.sa"
        ]

        # Arabic content
        arabic_lines = [
            "نموذج موافقة وسائل الإعلام والتسويق – TRAY",
            "",
            "بتوقيعي على هذا النموذج، أُقرّ بمنح شركة الحلول الرقمية الرائدة لتقنية المعلومات (TRAY)",
            "الحق الكامل وغير المقيد في تصويري أو تسجيل صوتي أو استخدام اسمي أو صورتي أو صوتي أو كلماتي",
            "في أي محتوى إعلامي يتم إنتاجه لأغراض تسويقية أو تعليمية أو ترويجية أو داخلية.",
            "",
            "أفهم أن هذه المواد قد تُستخدم على المواقع الإلكترونية، منصات التواصل الاجتماعي، المطبوعات،",
            "والعروض التقديمية. وأُدرك أنني لن أتلقى أي تعويض مادي أو حق في مراجعة أو الموافقة على المواد النهائية.",
            "",
            "بالتوقيع أدناه، أوافق على استخدام TRAY لمحتواي:",
            "TABLE_BLOCK",
            "للاستفسارات، يرجى التواصل مع قسم التسويق: marketing@tray.sa"
        ]

        # Generate bilingual PDF
        file_name = f"TRAY_Consent_{name.replace(' ', '_')}.pdf"
        pdf_data, final_filename = generate_bilingual_pdf(english_lines, arabic_lines, file_name)

        st.success("✅ Bilingual PDF consent form generated!")
        st.download_button("📄 Download Bilingual PDF", data=pdf_data, file_name=final_filename, mime="application/pdf")
    else:
        st.warning("Please enter the name to generate the consent form.")
