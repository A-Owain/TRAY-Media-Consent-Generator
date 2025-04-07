import streamlit as st
from datetime import datetime

# Automatically get today's date
today_date = datetime.today().strftime('%Y-%m-%d')

st.set_page_config(page_title="TRAY Consent Form Generator")

st.title("📝 TRAY Media Consent Form Generator")

# Input fields
name = st.text_input("Full Name / الاسم الكامل")
department = st.text_input("Department/Title / القسم أو المسمى الوظيفي")

if st.button("Generate Consent Forms"):
    if name and department:
        # English-only version
        english_form = f"""
TRAY Media Consent Form

I, {name}, hereby give TRAY and Alraedah Digital the full right to record, photograph, and use my image, voice, or appearance in videos, photos, or audio recordings for marketing, sales, training, or promotional purposes.

I understand that these materials may be used on social media platforms, websites, presentations, or other public and internal channels. I waive any rights to inspect or approve the final content or to receive compensation.

Full Name: {name}
Department/Title: {department}
Signature: _______________________________
Date: {today_date}
"""

        # Arabic-only version
        arabic_form = f"""
نموذج موافقة على الظهور الإعلامي – TRAY

أنا {name} أُقرّ وأوافق على أن تقوم شركة TRAY وشركة الرائدة الرقمية بتصويري أو تسجيلي صوتيًا أو بصريًا، واستخدام صورتي أو صوتي أو اسمي في فيديوهات أو صور أو تسجيلات لأغراض تسويقية، تدريبية، أو ترويجية.

وأُدرك أن هذه المواد قد تُستخدم على وسائل التواصل الاجتماعي، أو الموقع الإلكتروني، أو العروض التقديمية، أو أي قنوات داخلية أو عامة. وأتنازل عن أي حق في مراجعة أو الموافقة على المحتوى النهائي أو المطالبة بأي تعويض مادي.

الاسم الكامل: {name}
القسم/المسمى الوظيفي: {department}
التوقيع: _______________________________
التاريخ: {today_date}
"""

        st.success("✅ Consent forms generated!")

        st.download_button(
            label="📄 Download English Consent Form",
            data=english_form,
            file_name=f"TRAY_Consent_EN_{name}.txt",
            mime="text/plain"
        )

        st.download_button(
            label="📄 Download Arabic Consent Form",
            data=arabic_form,
            file_name=f"TRAY_Consent_AR_{name}.txt",
            mime="text/plain"
        )
    else:
        st.warning("Please fill in both the name and department fields.")
