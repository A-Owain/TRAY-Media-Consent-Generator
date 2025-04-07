import streamlit as st
from fpdf import FPDF
from datetime import date
import arabic_reshaper
from bidi.algorithm import get_display
import os
from zipfile import ZipFile

# Helper: Arabic shaping
def reshape_arabic(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

# PDF builder
def create_pdf(lines, filename, is_arabic=False, font_size=11):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("NotoArabic", '', fname="NotoSansArabic-SemiBold.ttf", uni=True)
    pdf.set_font("NotoArabic", size=font_size)

    # Title
    if is_arabic:
        pdf.set_font_size(16)
        pdf.multi_cell(0, 10, reshape_arabic(lines[0]), align="R")
        pdf.ln(4)
        pdf.set_font_size(font_size)
    else:
        pdf.set_font_size(16)
        pdf.multi_cell(0, 10, lines[0], align="L")
        pdf.ln(4)
        pdf.set_font_size(font_size)

    # Body
    for line in lines[1:]:
        if line == "TABLE_BLOCK":
            pdf.ln(8)
            if is_arabic:
                pdf.cell(40, 10, reshape_arabic("الاسم:"), ln=0, align="R")
                pdf.cell(80, 10, "_____________________________", ln=0, align="R")
                pdf.ln(10)
                pdf.cell(40, 10, reshape_arabic("التوقيع:"), ln=0, align="R")
                pdf.cell(80, 10, "_____________________________", ln=0, align="R")
                pdf.ln(10)
                pdf.cell(40, 10, reshape_arabic("التاريخ:"), ln=0, align="R")
                pdf.cell(80, 10, selected_date.strftime('%Y-%m-%d'), ln=1, align="R")
            else:
                pdf.cell(40, 10, "Name:", ln=0)
                pdf.cell(80, 10, "_____________________________", ln=0)
                pdf.ln(10)
                pdf.cell(40, 10, "Signature:", ln=0)
                pdf.cell(80, 10, "_____________________________", ln=0)
                pdf.ln(10)
                pdf.cell(40, 10, "Date:", ln=0)
                pdf.cell(80, 10, selected_date.strftime('%Y-%m-%d'), ln=1)
            pdf.ln(5)
        else:
            txt = reshape_arabic(line) if is_arabic else line
            align = "R" if is_arabic else "L"
            pdf.multi_cell(0, 10, txt, align=align)

    pdf.output(filename)

# Streamlit UI
st.set_page_config(page_title="TRAY Consent Form Generator")
st.title("TRAY Media Consent Form Generator")

name = st.text_input("Full Name / الاسم الكامل")
selected_date = st.date_input("Select the date / اختر التاريخ", value=date.today())

if st.button("Generate & Download ZIP"):
    if name:
        safe_name = name.replace('/', '-').replace('\\', '-')
        folder = f"{safe_name} Media Consent"
        os.makedirs(folder, exist_ok=True)

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

        # Generate PDFs
        en_file = f"{folder}/{safe_name} English Media Consent.pdf"
        ar_file = f"{folder}/{safe_name} Arabic Media Consent.pdf"
        create_pdf(english_lines, en_file, is_arabic=False)
        create_pdf(arabic_lines, ar_file, is_arabic=True)

        # ZIP all
        zip_file = f"{folder}.zip"
        with ZipFile(zip_file, 'w') as zipf:
            zipf.write(en_file)
            zipf.write(ar_file)

        # Clean up intermediate files
        os.remove(en_file)
        os.remove(ar_file)
        os.rmdir(folder)

        with open(zip_file, 'rb') as f:
            st.download_button(
                label="Download Media Consent ZIP",
                data=f,
                file_name=f"{safe_name} Media Consent.zip",
                mime="application/zip"
            )

        os.remove(zip_file)
    else:
        st.warning("Please enter your name.")
