import streamlit as st
from datetime import datetime

# Set up current date
today_date = datetime.today().strftime('%Y-%m-%d')

st.set_page_config(page_title="TRAY Consent Form Generator")
st.title("📝 TRAY Media Consent Form Generator")

# Input fields
name = st.text_input("Full Name / الاسم الكامل")
department = st.text_input("Department/Title / القسم أو المسمى الوظيفي")

if st.button("Generate Consent Forms"):
    if name and department:
        # English form
        english_form = f"""
TRAY Media & Marketing Consent Form

In signing this form, you give Company AL-HALLOUL RAQMIYAH AL-RAEDEH For Information Technology (TRAY)
the unrestricted right and permission to copyright and use, publish, and republish photographs, video, audio,
words, or any other form of media (materials) in all forms of communications (including printed materials)
for promotional purposes (including, but not limited to, advertising, publicity, commercial, or display use),
illustration, exhibition, editorial, trade, or any other purpose whatsoever.

You acknowledge that you are not entitled to any acknowledgment, compensation or remuneration, royalties,
or any other payment from TRAY or other partners in respect to the use of any materials.
TRAY agrees not to use any photo or interview in a manner that may be deemed adverse or defamatory
to the person signing this form. You acknowledge that you relinquish any right you may have to examine
or approve the completed materials or their use(s).

By signing this form, you consent to TRAY using and publishing your name and materials for marketing
purposes or social media.

Name: {name}
Department/Title: {department}
Signature: _______________________________
Date: {today_date}

For questions, contact TRAY Marketing at: marketing@tray.sa
"""

        # Arabic form
        arabic_form = f"""
نموذج موافقة وسائل الإعلام والتسويق – TRAY

بتوقيعي على هذا النموذج، أوافق على منح شركة الحلول الرقمية الرائدة لتقنية المعلومات (TRAY)
الحق الكامل وغير المقيد في استخدام ونشر وإعادة نشر الصور، الفيديو، الصوت، الكلمات أو أي شكل آخر
من الوسائط (المواد) في جميع أشكال التواصل (بما في ذلك المواد المطبوعة) لأغراض ترويجية
(بما يشمل على سبيل المثال لا الحصر الإعلان، الدعاية، الاستخدام التجاري أو العروض، التحرير، أو أي غرض آخر).

أقر أنني لست مستحقًا لأي تعويض مالي أو مكافأة أو أي نوع من المدفوعات من TRAY أو أي من شركائها
فيما يتعلق باستخدام هذه المواد. كما توافق TRAY على عدم استخدام أي صورة أو مقابلة بشكل
قد يُعتبر مسيئًا أو تشهيريًا. وأقر أنني أتنازل عن أي حق في مراجعة أو الموافقة على المواد المنتجة أو استخدامها.

بتوقيعي على هذا النموذج، أوافق على استخدام TRAY لاسمي ووسائطي لأغراض التسويق أو وسائل التواصل الاجتماعي.

الاسم: {name}
القسم / المسمى الوظيفي: {department}
التوقيع: _______________________________
التاريخ: {today_date}

للاستفسارات، يرجى التواصل مع قسم التسويق في TRAY عبر البريد الإلكتروني: marketing@tray.sa
"""

        st.success("✅ Consent forms generated successfully!")

        # Download buttons
        st.download_button(
            label="📄 Download English Consent Form",
            data=english_form,
            file_name=f"TRAY_Consent_EN_{name.replace(' ', '_')}.txt",
            mime="text/plain"
        )

        st.download_button(
            label="📄 Download Arabic Consent Form",
            data=arabic_form,
            file_name=f"TRAY_Consent_AR_{name.replace(' ', '_')}.txt",
            mime="text/plain"
        )
    else:
        st.warning("Please fill in both the name and department fields.")
