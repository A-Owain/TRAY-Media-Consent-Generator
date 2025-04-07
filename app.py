import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Current date
today_date = datetime.today().strftime('%Y-%m-%d')

st.set_page_config(page_title="TRAY Consent Form Generator")
st.title("📝 TRAY Media Consent Form Generator")

# Input fields
name = st.text_input("Full Name / الاسم الكامل")
department = st.text_input("Department/Title / القسم أو المسمى الوظيفي")

def generate_pdf(content, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font("ArialUnicode", '', fname="ArialUnicodeMS.ttf", uni=True)
    pdf.set_font("ArialUnicode", size=12)
    for line in content.split('\n'):
        pdf.multi_cell(0, 10, line)
    return pdf.output(dest='S').encode('latin-1'), filename

if st.button("Generate Consent PDFs"):
    if name and department:
        # English PDF content
        english_content = f"""TRAY Media & Marketing Consent Form

In signing this form, I grant Company AL-HALLOUL RAQMIYAH AL-RAEDEH For Information Technology (TRAY) the unrestricted right and permission to record, photograph, and use my name, image, voice, or words in any media content created for marketing, social media, educational, promotional, or internal use.

I understand that these materials may be used on websites, social media platforms, printed publications, and presentations. I acknowledge that I will not receive any compensation or have any rights to review or approve the final materials.

Name: {name}
Department/Title: {department}
Signature: _______________________________
Date: {today_date}

For questions, contact TRAY Marketing: marketing@tray.sa
"""

        # Arabic PDF content
        arabic_content = f"""نموذج موافقة وسائل الإعلام والتسويق – TRAY

بتوقيعي على هذا النموذج، أُقرّ بمنح شركة الحلول الرقمية الرائدة لتقنية المعلومات (TRAY) الحق الكامل وغير المقيد في تصويري أو تسجيل صوتي أو استخدام اسمي أو صورتي أو صوتي أو كلماتي في أي محتوى إعلامي يتم إنتاجه لأغراض تسويقية أو تعليمية أو ترويجية أو داخلية.

أفهم أن هذه المواد قد تُستخدم على المواقع الإلكترونية، منصات التواصل الاجتماعي، المطبوعات، والعروض التقديمية. وأُدرك أنني لن أتلقى أي تعويض مادي أو حق في مراجعة أو الموافقة على المواد النهائية.

الاسم: {name}
القسم / المسمى الوظيفي: {department}
التوقيع: _______________________________
التاريخ: {today_date}

للاستفسارات، يرجى التواصل مع التسويق: marketing@tray.sa
"""

        st.success("✅ PDF consent forms generated!")

        # Generate PDFs
        en_pdf, en_filename = generate_pdf(english_content, f"TRAY_Consent_EN_{name.replace(' ', '_')}.pdf")
        ar_pdf, ar_filename = generate_pdf(arabic_content, f"TRAY_Consent_AR_{name.replace(' ', '_')}.pdf")

        # Download buttons
        st.download_button("📄 Download English PDF", data=en_pdf, file_name=en_filename, mime="application/pdf")
        st.download_button("📄 Download Arabic PDF", data=ar_pdf, file_name=ar_filename, mime="application/pdf")

    else:
        st.warning("Please fill in both the name and department fields.")
