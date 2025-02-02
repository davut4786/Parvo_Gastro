import streamlit as st
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# === MODELLERİ YÜKLE ===
# Eğitim sırasında kaydedilen modeli yükle
model_path = "gastroparvo_model.pkl"
with open(model_path, "rb") as file:
    model = pickle.load(file)

# MinMaxScaler'ı yükle (eğer kaydettiysen)
scaler_path = "scaler.pkl"
with open(scaler_path, "rb") as file:
    scaler = pickle.load(file)

# === STREAMLIT ARAYÜZÜ ===
st.markdown("<h1 style='text-align: center;'>Hastalık Durumu Tahmin Uygulaması</h1>", unsafe_allow_html=True)

# === KULLANICI GİRDİLERİ ===
st.markdown("**Kan Parametreleri**")
col1, col2, col3, col4 = st.columns(4)  # 4 sütun olacak şekilde düzenleme
with col1:
    cBasebC = st.number_input("cBasebC", value=0.0)
    pCO2 = st.number_input("pCO2", value=0.0)
with col2:
    pH = st.number_input("pH", value=0.0)
    pO2 = st.number_input("pO2", value=0.0)
with col3:
    cCa = st.number_input("cCa", value=0.0)
    cCl = st.number_input("cCl", value=0.0)
with col4:
    cGlu = st.number_input("cGlu", value=0.0)
    cK = st.number_input("cK", value=0.0)

# === İKİNCİ KISIM (diğer kan parametreleri) ===
col5, col6, col7, col8 = st.columns(4)
with col5:
    cLac = st.number_input("cLac", value=0.0)
    cNa = st.number_input("cNa", value=0.0)
with col6:
    ctHb = st.number_input("ctHb", value=0.0)
    WBC = st.number_input("WBC", value=0.0)

# === SEMPTOMLAR ===
st.markdown("**Belirtiler**")
col9, col10 = st.columns(2)
with col9:
    halsizlik = st.checkbox("Halsizlik")
    ishal = st.checkbox("İshal")
    istahsizlik = st.checkbox("İştahsızlık")
with col10:
    kusma = st.checkbox("Kusma")
    zayiflama = st.checkbox("Zayıflama")

# === TAHMİN BUTONU ===
if st.button("Tahmin Et"):
    # Kullanıcının girdilerini bir DataFrame'e çevir
    user_input = pd.DataFrame([[cBasebC, pCO2, pH, pO2, cCa, cCl, cGlu, cK, cLac, cNa, ctHb, WBC,
                                int(halsizlik), int(ishal), int(istahsizlik), int(kusma), int(zayiflama)]],
                              columns=["cBasebC", "pCO2", "pH", "pO2", "cCa", "cCl", "cGlu", "cK", "cLac", "cNa", "ctHb", "WBC",
                                       "halsizlik", "ishal", "istahsizlik", "kusma", "zayiflama"])
    
    # **Normalizasyon uygula**
    user_input_scaled = scaler.transform(user_input)
    
    # **Tahmin yap**
    prediction = model.predict(user_input_scaled)[0]
    
    # **Sonucu kullanıcıya göster**
    result_text = "Gastro Enteritis" if prediction == 0 else "Parvoviral Enteritis"
    st.markdown(f"<h2 style='text-align: center;'>Tahmin Sonucu: {result_text}</h2>", unsafe_allow_html=True)
