import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(
    page_title="Prediksi Dropout Mahasiswa - Jaya Jaya Institut",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    .dropout-box {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
    }
    .graduate-box {
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        color: white;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(base_dir, 'model')
    model = joblib.load(os.path.join(model_dir, 'model.joblib'))
    scaler = joblib.load(os.path.join(model_dir, 'scaler.joblib'))
    features = joblib.load(os.path.join(model_dir, 'features.joblib'))
    le = joblib.load(os.path.join(model_dir, 'label_encoder.joblib'))
    return model, scaler, features, le


model, scaler, features, le = load_model()

st.markdown('<div class="main-header">Sistem Prediksi Dropout Mahasiswa</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Jaya Jaya Institut - Early Warning System</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Prediksi Individual", "Informasi Model"])

with tab1:
    st.markdown("### Input Data Mahasiswa")
    st.markdown("Lengkapi data berikut untuk memprediksi risiko dropout mahasiswa.")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### Data Demografis")

        marital_options = {
            'Single': 1, 'Married': 2, 'Widower': 3,
            'Divorced': 4, 'Facto Union': 5, 'Legally Separated': 6
        }
        marital = st.selectbox("Status Perkawinan", list(marital_options.keys()))
        marital_val = marital_options[marital]

        gender = st.selectbox("Gender", ['Perempuan', 'Laki-laki'])
        gender_val = 0 if gender == 'Perempuan' else 1

        age = st.number_input("Usia saat Pendaftaran", min_value=17, max_value=60, value=20)

        nationality_options = {
            'Portuguese': 1, 'German': 2, 'Spanish': 6, 'Italian': 11,
            'Dutch': 13, 'English': 14, 'Brazilian': 41, 'Other': 1
        }
        nationality = st.selectbox("Kewarganegaraan", list(nationality_options.keys()))
        nationality_val = nationality_options[nationality]

        international = 1 if nationality != 'Portuguese' else 0
        displaced = st.selectbox("Displaced", ['Tidak', 'Ya'])
        displaced_val = 1 if displaced == 'Ya' else 0

        st.markdown("#### Data Pendaftaran")

        application_mode_options = {
            '1st phase - general contingent': 1,
            'Ordinance No. 612/93': 2,
            '1st phase - special (Azores)': 5,
            'Holders of other higher courses': 7,
            'Ordinance No. 854-B/99': 10,
            'International student (bachelor)': 15,
            '1st phase - special (Madeira)': 16,
            '2nd phase - general': 17,
            '3rd phase - general': 18,
            'Over 23 years old': 39,
            'Transfer': 42,
            'Change of course': 43,
            'Technological specialization diploma': 44,
            'Change of institution/course': 51,
            'Short cycle diploma holders': 53,
            'Change of inst/course (International)': 57
        }
        app_mode = st.selectbox("Jalur Pendaftaran", list(application_mode_options.keys()))
        app_mode_val = application_mode_options[app_mode]

        app_order = st.slider("Urutan Pilihan (0 = pilihan pertama)", 0, 9, 1)

        course_options = {
            'Biofuel Production Technologies': 33,
            'Animation and Multimedia Design': 171,
            'Social Service (evening)': 8014,
            'Agronomy': 9003,
            'Communication Design': 9070,
            'Veterinary Nursing': 9085,
            'Informatics Engineering': 9119,
            'Equinculture': 9130,
            'Management': 9147,
            'Social Service': 9238,
            'Tourism': 9254,
            'Nursing': 9500,
            'Oral Hygiene': 9556,
            'Advertising and Marketing Mgmt': 9670,
            'Journalism and Communication': 9773,
            'Basic Education': 9853,
            'Management (evening)': 9991
        }
        course = st.selectbox("Program Studi", list(course_options.keys()))
        course_val = course_options[course]

        daytime = st.selectbox("Waktu Kuliah", ['Siang (Daytime)', 'Malam (Evening)'])
        daytime_val = 1 if 'Siang' in daytime else 0

    with col_right:
        st.markdown("#### Latar Belakang Pendidikan")

        prev_qual_options = {
            'Secondary education': 1,
            'Higher education - bachelor': 2,
            'Higher education - degree': 3,
            'Higher education - master': 4,
            'Higher education - doctorate': 5,
            'Frequency of higher education': 6,
            '12th year - not completed': 9,
            '11th year - not completed': 10,
            'Basic education 3rd cycle': 19,
            'Basic education 2nd cycle': 38,
            'Technological specialization': 39,
            'Other': 12
        }
        prev_qual = st.selectbox("Kualifikasi Sebelumnya", list(prev_qual_options.keys()))
        prev_qual_val = prev_qual_options[prev_qual]

        prev_grade = st.number_input("Nilai Kualifikasi Sebelumnya (0-200)", 0.0, 200.0, 130.0, step=0.5)
        admission_grade = st.number_input("Nilai Masuk (0-200)", 0.0, 200.0, 130.0, step=0.5)

        mothers_qual = st.slider("Kualifikasi Ibu (1-44)", 1, 44, 19)
        fathers_qual = st.slider("Kualifikasi Ayah (1-44)", 1, 44, 12)
        mothers_occ = st.slider("Pekerjaan Ibu (kode 0-46)", 0, 46, 5)
        fathers_occ = st.slider("Pekerjaan Ayah (kode 0-46)", 0, 46, 9)

        st.markdown("#### Status Finansial")
        tuition = st.selectbox("Biaya Kuliah Lunas", ['Ya', 'Tidak'])
        tuition_val = 1 if tuition == 'Ya' else 0

        scholarship = st.selectbox("Penerima Beasiswa", ['Tidak', 'Ya'])
        scholarship_val = 1 if scholarship == 'Ya' else 0

        debtor = st.selectbox("Memiliki Tunggakan", ['Tidak', 'Ya'])
        debtor_val = 1 if debtor == 'Ya' else 0

        special_needs = st.selectbox("Kebutuhan Khusus", ['Tidak', 'Ya'])
        special_needs_val = 1 if special_needs == 'Ya' else 0

    st.markdown("---")
    st.markdown("#### Performa Akademik")

    sem_col1, sem_col2 = st.columns(2)

    with sem_col1:
        st.markdown("**Semester 1**")
        cu_1_credited = st.number_input("Mata kuliah dikreditkan (Sem 1)", 0, 30, 0, key="c1c")
        cu_1_enrolled = st.number_input("Mata kuliah diambil (Sem 1)", 0, 30, 6, key="c1e")
        cu_1_evaluations = st.number_input("Evaluasi (Sem 1)", 0, 50, 6, key="c1ev")
        cu_1_approved = st.number_input("Mata kuliah lulus (Sem 1)", 0, 30, 5, key="c1a")
        cu_1_grade = st.number_input("Nilai rata-rata (Sem 1, 0-20)", 0.0, 20.0, 12.0, step=0.1, key="c1g")
        cu_1_wo_eval = st.number_input("Tanpa evaluasi (Sem 1)", 0, 20, 0, key="c1w")

    with sem_col2:
        st.markdown("**Semester 2**")
        cu_2_credited = st.number_input("Mata kuliah dikreditkan (Sem 2)", 0, 30, 0, key="c2c")
        cu_2_enrolled = st.number_input("Mata kuliah diambil (Sem 2)", 0, 30, 6, key="c2e")
        cu_2_evaluations = st.number_input("Evaluasi (Sem 2)", 0, 50, 6, key="c2ev")
        cu_2_approved = st.number_input("Mata kuliah lulus (Sem 2)", 0, 30, 5, key="c2a")
        cu_2_grade = st.number_input("Nilai rata-rata (Sem 2, 0-20)", 0.0, 20.0, 12.0, step=0.1, key="c2g")
        cu_2_wo_eval = st.number_input("Tanpa evaluasi (Sem 2)", 0, 20, 0, key="c2w")

    st.markdown("---")
    st.markdown("#### Faktor Ekonomi Makro")

    eco_col1, eco_col2, eco_col3 = st.columns(3)
    with eco_col1:
        unemployment = st.number_input("Unemployment Rate (%)", 0.0, 30.0, 10.8, step=0.1)
    with eco_col2:
        inflation = st.number_input("Inflation Rate (%)", -5.0, 10.0, 1.4, step=0.1)
    with eco_col3:
        gdp = st.number_input("GDP", -10.0, 10.0, 1.74, step=0.01)

    st.markdown("---")

    if st.button("Prediksi Status Mahasiswa", type="primary", use_container_width=True):
        input_data = pd.DataFrame([{
            'Marital_status': marital_val,
            'Application_mode': app_mode_val,
            'Application_order': app_order,
            'Course': course_val,
            'Daytime_evening_attendance': daytime_val,
            'Previous_qualification': prev_qual_val,
            'Previous_qualification_grade': prev_grade,
            'Nacionality': nationality_val,
            'Mothers_qualification': mothers_qual,
            'Fathers_qualification': fathers_qual,
            'Mothers_occupation': mothers_occ,
            'Fathers_occupation': fathers_occ,
            'Admission_grade': admission_grade,
            'Displaced': displaced_val,
            'Educational_special_needs': special_needs_val,
            'Debtor': debtor_val,
            'Tuition_fees_up_to_date': tuition_val,
            'Gender': gender_val,
            'Scholarship_holder': scholarship_val,
            'Age_at_enrollment': age,
            'International': international,
            'Curricular_units_1st_sem_credited': cu_1_credited,
            'Curricular_units_1st_sem_enrolled': cu_1_enrolled,
            'Curricular_units_1st_sem_evaluations': cu_1_evaluations,
            'Curricular_units_1st_sem_approved': cu_1_approved,
            'Curricular_units_1st_sem_grade': cu_1_grade,
            'Curricular_units_1st_sem_without_evaluations': cu_1_wo_eval,
            'Curricular_units_2nd_sem_credited': cu_2_credited,
            'Curricular_units_2nd_sem_enrolled': cu_2_enrolled,
            'Curricular_units_2nd_sem_evaluations': cu_2_evaluations,
            'Curricular_units_2nd_sem_approved': cu_2_approved,
            'Curricular_units_2nd_sem_grade': cu_2_grade,
            'Curricular_units_2nd_sem_without_evaluations': cu_2_wo_eval,
            'Unemployment_rate': unemployment,
            'Inflation_rate': inflation,
            'GDP': gdp
        }])

        input_data = input_data[features]
        input_scaled = scaler.transform(input_data)

        prediction = model.predict(input_scaled)[0]
        probabilities = model.predict_proba(input_scaled)[0]

        predicted_label = le.inverse_transform([prediction])[0]
        dropout_prob = probabilities[0]
        graduate_prob = probabilities[1]

        st.markdown("### Hasil Prediksi")

        if predicted_label == 'Dropout':
            st.markdown(f"""
            <div class="result-box dropout-box">
                <h2>RISIKO DROPOUT</h2>
                <p style="font-size: 1.3rem;">Probabilitas Dropout: <strong>{dropout_prob*100:.1f}%</strong></p>
                <p style="font-size: 1.3rem;">Probabilitas Graduate: <strong>{graduate_prob*100:.1f}%</strong></p>
            </div>
            """, unsafe_allow_html=True)
            st.warning("Mahasiswa ini terdeteksi berisiko tinggi untuk dropout. Disarankan untuk segera memberikan bimbingan dan dukungan khusus.")
        else:
            st.markdown(f"""
            <div class="result-box graduate-box">
                <h2>PREDIKSI GRADUATE</h2>
                <p style="font-size: 1.3rem;">Probabilitas Graduate: <strong>{graduate_prob*100:.1f}%</strong></p>
                <p style="font-size: 1.3rem;">Probabilitas Dropout: <strong>{dropout_prob*100:.1f}%</strong></p>
            </div>
            """, unsafe_allow_html=True)
            st.success("Mahasiswa ini diprediksi akan menyelesaikan studi dengan baik.")

        st.markdown("---")
        st.markdown("#### Ringkasan Input")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.markdown(f"""
            <div class="metric-card">
                <strong>Performa Semester 1</strong><br>
                Lulus: {cu_1_approved} dari {cu_1_enrolled} MK<br>
                Nilai rata-rata: {cu_1_grade}
            </div>
            """, unsafe_allow_html=True)
        with col_s2:
            st.markdown(f"""
            <div class="metric-card">
                <strong>Performa Semester 2</strong><br>
                Lulus: {cu_2_approved} dari {cu_2_enrolled} MK<br>
                Nilai rata-rata: {cu_2_grade}
            </div>
            """, unsafe_allow_html=True)
        with col_s3:
            st.markdown(f"""
            <div class="metric-card">
                <strong>Status Finansial</strong><br>
                Biaya lunas: {tuition}<br>
                Beasiswa: {scholarship}<br>
                Tunggakan: {debtor}
            </div>
            """, unsafe_allow_html=True)


with tab2:
    st.markdown("### Tentang Model")
    st.markdown("""
    Model prediksi ini menggunakan algoritma **Random Forest Classifier** yang dilatih pada dataset
    performa mahasiswa Jaya Jaya Institut.
    """)

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Accuracy", "91.05%")
    col_m2.metric("ROC-AUC", "0.9542")
    col_m3.metric("Precision (Dropout)", "95%")
    col_m4.metric("Recall (Dropout)", "81%")

    st.markdown("### Konfigurasi Model")
    st.markdown("""
    | Parameter | Nilai |
    |-----------|-------|
    | Algorithm | Random Forest |
    | Estimators | 200 |
    | Max Depth | 15 |
    | Min Samples Split | 5 |
    | Min Samples Leaf | 2 |
    | Training Data | 2,904 sampel |
    | Test Data | 726 sampel |
    """)

    st.markdown("### Top 10 Faktor Paling Berpengaruh")
    top_features = {
        'Curricular_units_2nd_sem_approved': 0.2539,
        'Curricular_units_1st_sem_approved': 0.1340,
        'Curricular_units_2nd_sem_grade': 0.1225,
        'Curricular_units_1st_sem_grade': 0.0760,
        'Tuition_fees_up_to_date': 0.0624,
        'Age_at_enrollment': 0.0303,
        'Curricular_units_2nd_sem_evaluations': 0.0286,
        'Course': 0.0253,
        'Curricular_units_1st_sem_evaluations': 0.0239,
        'Admission_grade': 0.0225
    }

    feat_df = pd.DataFrame({
        'Fitur': list(top_features.keys()),
        'Importance': list(top_features.values())
    })
    st.bar_chart(feat_df.set_index('Fitur'))

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#888; font-size:0.85rem;'>"
    "Jaya Jaya Institut - Student Dropout Early Warning System</p>",
    unsafe_allow_html=True
)
