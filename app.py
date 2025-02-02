import streamlit as st
import pickle
import pandas as pd

# Modeli yükle
model_path = "gastroparvo_model.pkl"
with open(model_path, "rb") as file:
    model = pickle.load(file)

# Streamlit başlığı ortalı
st.markdown("<h1 style='text-align: center;'>Hastalık Tahmin Uygulaması</h1>", unsafe_allow_html=True)

# Kullanıcıdan girdileri alma
st.markdown("**Hasta Bulguları ve Laboratuvar Sonuçları**")
columns = ["cBasebC", "pCO2", "pH", "pO2", "cCa", "cCl", "cGlu", "cK", "cLac", "cNa", "ctHb", "FCOHb", "FMetHb", "FO2Hb", "GRAN", "GRAN_A", "LYM", "LYM_A", "MON", "MON_A", "Hb", "HCT", "MCH", "MCHC", "MCV", "MPV", "PLT", "RBC", "RDW", "WBC"]

# Sayısal değişkenleri alma
if 'numeric_inputs' not in st.session_state:
    st.session_state.numeric_inputs = {col: None for col in columns}

col1, col2, col3, col4, col5, col6 = st.columns(6)

# Sayısal verileri her sütuna yerleştir
for i, col in enumerate(columns):
    if i % 6 == 0:
        st.session_state.numeric_inputs[col] = col1.number_input(f"{col}", value=st.session_state.numeric_inputs[col], format="%.2f")
    elif i % 6 == 1:
        st.session_state.numeric_inputs[col] = col2.number_input(f"{col}", value=st.session_state.numeric_inputs[col], format="%.2f")
    elif i % 6 == 2:
        st.session_state.numeric_inputs[col] = col3.number_input(f"{col}", value=st.session_state.numeric_inputs[col], format="%.2f")
    elif i % 6 == 3:
        st.session_state.numeric_inputs[col] = col4.number_input(f"{col}", value=st.session_state.numeric_inputs[col], format="%.2f")
    elif i % 6 == 4:
        st.session_state.numeric_inputs[col] = col5.number_input(f"{col}", value=st.session_state.numeric_inputs[col], format="%.2f")
    else:
        st.session_state.numeric_inputs[col] = col6.number_input(f"{col}", value=st.session_state.numeric_inputs[col], format="%.2f")

# Klinik Bulgular ve Hayvan Türü için kategorik veriler
st.markdown("**Klinik Bulgular ve Hayvan Türü**")
if 'categorical_inputs' not in st.session_state:
    st.session_state.categorical_inputs = {
        "halsizlik": False,
        "ishal": False,
        "istahsizlik": False,
        "kusma": False,
        "zayiflama": False,
        "AnimalType_kedi": 0,
        "AnimalType_kopek": 0,
    }

# 6 sütunlu düzenleme ile checkbox'lar
col1, col2, col3, col4, col5, col6 = st.columns(6)

st.session_state.categorical_inputs["halsizlik"] = col1.checkbox("Halsizlik", value=st.session_state.categorical_inputs["halsizlik"])
st.session_state.categorical_inputs["ishal"] = col1.checkbox("İshal", value=st.session_state.categorical_inputs["ishal"])
st.session_state.categorical_inputs["istahsizlik"] = col2.checkbox("İştahsızlık", value=st.session_state.categorical_inputs["istahsizlik"])
st.session_state.categorical_inputs["kusma"] = col2.checkbox("Kusma", value=st.session_state.categorical_inputs["kusma"])
st.session_state.categorical_inputs["zayiflama"] = col3.checkbox("Zayıflama", value=st.session_state.categorical_inputs["zayiflama"])

# Hayvan türü seçimi (ikili sütun: Kedi/Köpek)
animal_type = col4.radio("Hayvan Türü", ("Kedi", "Köpek"), index=0 if st.session_state.categorical_inputs["AnimalType_kedi"] == 1 else 1)
st.session_state.categorical_inputs["AnimalType_kedi"] = 1 if animal_type == "Kedi" else 0
st.session_state.categorical_inputs["AnimalType_kopek"] = 1 if animal_type == "Köpek" else 0

# Tahmin butonu
if st.button("Tahmin Et"):
    # Model giriş verisini hazırlama
    input_data = pd.DataFrame([{**st.session_state.numeric_inputs, **st.session_state.categorical_inputs}])

    # Eksik veri kontrolü
    missing_columns = input_data.columns[input_data.isnull().any()].tolist()
    if missing_columns:
        # Eksik sütunları kullanıcıya bildir
        missing_message = "Lütfen şu sütunları doldurun: " + ", ".join(missing_columns)
        st.warning(missing_message)
    else:
        try:
            prediction = model.predict(input_data)[0]
            
            # Sonucu kullanıcı dostu formatta gösterme
            result_text = "Parvoviral Enteritis" if prediction == 1 else "Gastro Enteritis"
            st.markdown(f"<h2 style='text-align: center;'>Tahmin Sonucu: {result_text}</h2>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Bir hata oluştu: {str(e)}")

# Temizle butonu
if st.button("Temizle"):
    # Tüm girişleri sıfırla
    st.session_state.numeric_inputs = {col: None for col in columns}
    st.session_state.categorical_inputs = {
        "halsizlik": False,
        "ishal": False,
        "istahsizlik": False,
        "kusma": False,
        "zayiflama": False,
        "AnimalType_kedi": 0,
        "AnimalType_kopek": 0,
    }
    # Sayfayı sıfırlama
    st.experimental_rerun()
