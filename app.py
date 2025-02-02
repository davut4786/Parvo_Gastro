import streamlit as st
import pickle
import pandas as pd

# --------------------------
# Özel Tema Ayarları - İlk Satırda
# --------------------------
st.set_page_config(
    page_title="Hastalık Tahmin Uygulaması",
    page_icon="🧑‍⚕️",
    layout="wide",
    initial_sidebar_state="collapsed",
    theme={
        "base": "light",
        "backgroundColor": "#a7e7f9"
    }
)

# --------------------------
# Dosyaları Yükle
# --------------------------

# Scaler'ı yükleyin (scaler.pkl dosyasından)
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Modeli yükleyin (gastroparvo_model.pkl dosyasından)
with open("gastroparvo_model.pkl", "rb") as f:
    model = pickle.load(f)

# --------------------------
# Uygulama Başlığı
# --------------------------
st.markdown("<h1 style='text-align: center;'>Hastalık Tahmin Uygulaması</h1>", unsafe_allow_html=True)

# --------------------------
# Girdi Alanları İçin Ayarlar
# --------------------------
# Eğitimde kullandığınız sayısal sütunlar (float64 türündeki sütunlar)
columns = [
    "cBasebC", "pCO2", "pH", "pO2", "cCa", "cCl", "cGlu", "cK", "cLac", "cNa",
    "ctHb", "FCOHb", "FMetHb", "FO2Hb", "GRAN", "GRAN_A", "LYM", "LYM_A",
    "MON", "MON_A", "Hb", "HCT", "MCH", "MCHC", "MCV", "MPV", "PLT", "RBC",
    "RDW", "WBC"
]

# Session state başlangıç değerleri
if 'numeric_inputs' not in st.session_state:
    st.session_state.numeric_inputs = {col: None for col in columns}

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

# --------------------------
# Sayısal Girdiler (6 Sütunlu Düzen)
# --------------------------
st.markdown("**Hasta Bulguları ve Laboratuvar Sonuçları**")
col1, col2, col3, col4, col5, col6 = st.columns(6)
for i, col in enumerate(columns):
    # Her sütuna yerleştirirken, benzersiz key kullanıyoruz.
    key_val = f"{col}_input"
    if i % 6 == 0:
        st.session_state.numeric_inputs[col] = col1.number_input(col, value=None, format="%.2f", key=key_val)
    elif i % 6 == 1:
        st.session_state.numeric_inputs[col] = col2.number_input(col, value=None, format="%.2f", key=key_val)
    elif i % 6 == 2:
        st.session_state.numeric_inputs[col] = col3.number_input(col, value=None, format="%.2f", key=key_val)
    elif i % 6 == 3:
        st.session_state.numeric_inputs[col] = col4.number_input(col, value=None, format="%.2f", key=key_val)
    elif i % 6 == 4:
        st.session_state.numeric_inputs[col] = col5.number_input(col, value=None, format="%.2f", key=key_val)
    else:
        st.session_state.numeric_inputs[col] = col6.number_input(col, value=None, format="%.2f", key=key_val)

# --------------------------
# Kategorik Girdiler
# --------------------------
st.markdown("**Klinik Bulgular ve Hayvan Türü**")
col1, col2, col3, col4, col5, col6 = st.columns(6)
st.session_state.categorical_inputs["halsizlik"] = col1.checkbox("Halsizlik", value=False, key="halsizlik")
st.session_state.categorical_inputs["ishal"] = col1.checkbox("İshal", value=False, key="ishal")
st.session_state.categorical_inputs["istahsizlik"] = col2.checkbox("İştahsızlık", value=False, key="istahsizlik")
st.session_state.categorical_inputs["kusma"] = col2.checkbox("Kusma", value=False, key="kusma")
st.session_state.categorical_inputs["zayiflama"] = col3.checkbox("Zayıflama", value=False, key="zayiflama")
animal_type = col4.radio("Hayvan Türü", options=["Kedi", "Köpek"],
                           index=0 if st.session_state.categorical_inputs["AnimalType_kedi"] == 1 else 1,
                           key="animal_type")
st.session_state.categorical_inputs["AnimalType_kedi"] = 1 if animal_type == "Kedi" else 0
st.session_state.categorical_inputs["AnimalType_kopek"] = 1 if animal_type == "Köpek" else 0

# --------------------------
# Tahmin Butonu ve İşlemleri
# --------------------------
if st.button("Tahmin Et"):
    # Girdileri birleştirip DataFrame oluşturun
    input_data = pd.DataFrame([{**st.session_state.numeric_inputs, **st.session_state.categorical_inputs}])
    
    # Eksik veri kontrolü
    missing_columns = input_data.columns[input_data.isnull().any()].tolist()
    if missing_columns:
        st.warning("Lütfen şu sütunları doldurun: " + ", ".join(missing_columns))
    else:
        try:
            # Önemli: Sadece sayısal sütunları scaler ile dönüştürün
            input_data[columns] = scaler.transform(input_data[columns])
            prediction = model.predict(input_data)[0]
            result_text = "Parvoviral Enteritis" if prediction == 1 else "Gastro Enteritis"
            st.markdown(f"<h2 style='text-align: center;'>Tahmin Sonucu: {result_text}</h2>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Bir hata oluştu: {str(e)}")

# --------------------------
# Temizle Butonu
# --------------------------
if st.button("Temizle"):
    # Tüm session_state anahtarlarını temizleyelim
    st.session_state.numeric_inputs = {col: None for col in columns}  # Sayısal girişler boş olacak
    st.session_state.categorical_inputs = {
        "halsizlik": False,
        "ishal": False,
        "istahsizlik": False,
        "kusma": False,
        "zayiflama": False,
        "AnimalType_kedi": 0,
        "AnimalType_kopek": 0,
    }
    st.info("Form temizlendi. Lütfen tekrar veri giriniz.")
