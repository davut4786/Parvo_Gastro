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
numeric_inputs = {}
col1, col2, col3, col4 = st.columns(4)  # 4 sütun oluşturuluyor

# Sayısal verileri her sütuna yerleştir
for i, col in enumerate(columns):
    if i % 4 == 0:
        numeric_inputs[col] = col1.number_input(f"{col}", value=None, format="%.2f")
    elif i % 4 == 1:
        numeric_inputs[col] = col2.number_input(f"{col}", value=None, format="%.2f")
    elif i % 4 == 2:
        numeric_inputs[col] = col3.number_input(f"{col}", value=None, format="%.2f")
    else:
        numeric_inputs[col] = col4.number_input(f"{col}", value=None, format="%.2f")

# Kategorik ve bool değişkenleri alma
st.markdown("**Klinik Bulgular ve Hayvan Türü**")
categorical_inputs = {
    "halsizlik": st.checkbox("Halsizlik"),
    "ishal": st.checkbox("İshal"),
    "istahsizlik": st.checkbox("İştahsızlık"),
    "kusma": st.checkbox("Kusma"),
    "zayiflama": st.checkbox("Zayıflama"),
    "AnimalType_kedi": st.checkbox("Kedi"),
    "AnimalType_kopek": st.checkbox("Köpek"),
}

# Tahmin butonu
if st.button("Tahmin Et"):
    # Model giriş verisini hazırlama
    input_data = pd.DataFrame([{**numeric_inputs, **categorical_inputs}])
    
    # Eksik veri kontrolü
    if input_data.isnull().values.any():
        st.warning("Lütfen tüm alanları doldurun!")
    else:
        prediction = model.predict(input_data)[0]
        
        # Sonucu kullanıcı dostu formatta gösterme
        result_text = "Parvoviral Enteritis" if prediction == 1 else "Gastro Enteritis"
        st.markdown(f"<h2 style='text-align: center;'>Tahmin Sonucu: {result_text}</h2>", unsafe_allow_html=True)
