import streamlit as st
from fpdf import FPDF
from datetime import date
import arabic_reshaper
from bidi.algorithm import get_display
from zipfile import ZipFile
import os

# Helper: Arabic shaping
def reshape_arabic(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

# PDF generation
def create_pdf(filename, lines, is_arabic, bg_image, selected_date, font_file):
    pdf = FPDF(format="A4")
    pdf.add_page()
    pdf.image(bg_image, x=0, y=0, w=210, h=297)

    pdf.add_font("NotoArabic", '', fname=font_file, uni=True)
    pdf.set_font("NotoArabic", size=11)

    top_margin_mm = 53.27
    text_width_mm = 191.21
    left_right_margin_mm = 9.397

    pdf.set_y(top_margin_mm)
    pdf.set_x(left_right_margin_mm)

    # Title
    if is_arabic:
        pdf.set_font_size(16)
        pdf.multi_cell(text_width_mm, 10, reshape_arabic(lines[0]), align='R')
    else:
        pdf.set_font_size(16)
        pdf.multi_cell(text_width_mm, 10, lines[0], align='L')

    pdf.set_font_size(11)
    pdf.ln(2)

    for line in lines[1:]:
        if line == "TABLE_BLOCK":
            pdf.ln(6)
            if is_arabic:
                pdf.multi_cell(text_width_mm, 10, reshape_arabic("الاسم: _____________________________"), align='R')
                pdf.multi_cell(text_width_mm, 10, reshape_arabic("التوقيع: _____________________________"), align='R')
                pdf.multi_cell(text_width_mm, 10, reshape_arabic(f"التاريخ: {selected_date.strftime('%Y-%m-%d')}"), align='R')
            else:
                pdf.multi_cell(text_width_mm, 10, "Name: _____________________________", align='L')
                pdf.multi_cell(text_width_mm, 10, "Signature: _____________________________", align='L')
                pdf.multi_cell(text_width_mm, 10, f"Date: {selected_date.strftime('%Y-%m-%d')}", align='L')
        else:
            txt = reshape_arabic(line) if is_arabic else line
            align = 'R' if is_arabic else 'L'
            pdf.multi_cell(text_width_mm, 10, txt, align=align)

    pdf.output(filename)

# Streamlit App
st.set_page_config(page_title="TRAY Consent Form Generator")
st.title("TRAY Media Consent Form Generator")

name = st.text_input("Full Name / الاسم الكامل")
selected_date = st.date_input("Select the date / اختر التاريخ", value=date.today())

if st.button("Generate & Download Consent ZIP"):
    if name:
        safe_name = name.replace('/', '-').replace('\\', '-')
        folder = f"{safe_name} Media Consent"
        os.makedirs(folder, exist_ok=True)

        # Content
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
        bg = "consent_background.png"
        font_path = "NotoSansArabic-SemiBold.ttf"

        en_pdf = f"{folder}/{safe_name} English Media Consent.pdf"
        ar_pdf = f"{folder}/{safe_name} Arabic Media Consent.pdf"

        create_pdf(en_pdf, english_lines, is_arabic=False, bg_image=bg, selected_date=selected_date, font_file=font_path)
        create_pdf(ar_pdf, arabic_lines, is_arabic=True, bg_image=bg, selected_date=selected_date, font_file=font_path)

        # Zip everything
        zip_file = f"{safe_name} Media Consent.zip"
        with ZipFile(zip_file, 'w') as zipf:
            zipf.write(en_pdf)
            zipf.write(ar_pdf)

        # Clean temp files
        os.remove(en_pdf)
        os.remove(ar_pdf)
        os.rmdir(folder)

        # Offer download
        with open(zip_file, 'rb') as f:
            st.download_button(
                label="Download Media Consent ZIP",
                data=f,
                file_name=zip_file,
                mime="application/zip"
            )

        os.remove(zip_file)
    else:
        st.warning("Please enter a name.")
