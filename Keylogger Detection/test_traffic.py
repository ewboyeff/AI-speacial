# Wireshark’dan olingan trafik faylini keylogger uchun sinash (Mahalliy muhit uchun)

# 1. Kerakli kutubxonalar
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
from sklearn.preprocessing import StandardScaler

# TensorFlow oneDNN xabarini o'chirish
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# 2. Fayllarni yo'lini aniqlash
base_path = r"D:\Pdp\2-kurs\AI\Keylogger Detection"
traffic_file = f"{base_path}\\trafik.csv"
model_file = f"{base_path}\\keylogger_model.pkl"  # yoki keylogger_model.h5
scaler_file = f"{base_path}\\scaler.pkl"
features_file = f"{base_path}\\features.pkl"
output_file = f"{base_path}\\traffic_predictions.csv"

# 3. Ma'lumotlarni o'qish
print("Trafik faylini o'qish...")
try:
    traffic_data = pd.read_csv(traffic_file)
except FileNotFoundError:
    raise FileNotFoundError(f"'{traffic_file}' fayli topilmadi. Iltimos, faylni to'g'ri joylashtiring.")

print("Trafik fayl ustunlari:", traffic_data.columns)

# 4. Model uchun kerakli ustunlarni aniqlash
print("Model uchun kerakli ustunlarni yuklash...")
try:
    selected_features = joblib.load(features_file)
except FileNotFoundError:
    raise FileNotFoundError(f"'{features_file}' fayli topilmadi.")

print("Model uchun kerakli ustunlar:", selected_features)

# 5. Ustunlarni moslashtirish va ma'lumotlarni boyitish
# Wireshark ustunlarini moslashtirish
column_mapping = {
    'Source': ' Source IP',
    'Destination': ' Destination IP',
    'Source Port': ' Source Port',
    'Destination Port': ' Destination Port',
    'Protocol': ' Protocol',
    'Length': 'Total Length of Fwd Packets',
}
traffic_data = traffic_data.rename(columns=column_mapping)

# Qo'shimcha xususiyatlarni hisoblash
# Flow Duration ni hisoblash (taxminiy)
if 'Time' in traffic_data.columns:
    traffic_data['Time'] = pd.to_datetime(traffic_data['Time'], errors='coerce')
    traffic_data[' Flow Duration'] = (traffic_data['Time'].max() - traffic_data['Time'].min()).total_seconds() * 1e6 if traffic_data['Time'].notna().any() else 0

# Fwd Packet Length Max, Mean va boshqalarni hisoblash (taxminiy)
if 'Length' in traffic_data.columns:
    traffic_data[' Fwd Packet Length Max'] = traffic_data['Length'].max()
    traffic_data[' Fwd Packet Length Mean'] = traffic_data['Length'].mean()
    traffic_data[' Fwd Packet Length Std'] = traffic_data['Length'].std()
    traffic_data[' Max Packet Length'] = traffic_data['Length'].max()
    traffic_data[' Packet Length Std'] = traffic_data['Length'].std()

# Yetishmayotgan ustunlarni 0 bilan to'ldirish
for feature in selected_features:
    if feature not in traffic_data.columns:
        traffic_data[feature] = 0
        print(f"{feature} ustuni topilmadi, 0 bilan to'ldirildi.")

# 6. Ma'lumotlarni tayyorlash
new_data = traffic_data[selected_features].values  # Xususiyat nomlarini olib tashlash
print("Ma'lumotlarni o'lchovlash...")
try:
    scaler = joblib.load(scaler_file)
except FileNotFoundError:
    raise FileNotFoundError(f"'{scaler_file}' fayli topilmadi.")

new_data_scaled = scaler.transform(new_data)

# 7. Modelni yuklash va bashorat qilish
print("Modelni yuklash...")
try:
    model = joblib.load(model_file)  # XGBoost modeli
    print("XGBoost modeli yuklandi.")
except:
    try:
        model = tf.keras.models.load_model(model_file.replace('.pkl', '.h5'))  # Deep Learning modeli
        print("Deep Learning modeli yuklandi.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Model fayli ('{model_file}' yoki '.h5') topilmadi.")

if 'predict_proba' in dir(model):
    predictions = model.predict(new_data_scaled)
    probabilities = model.predict_proba(new_data_scaled)[:, 1]
else:
    probabilities = model.predict(new_data_scaled, verbose=0).flatten()
    predictions = (probabilities > 0.5).astype(int)

# 8. Natijalarni chiqarish
print("Bashoratlar (0=Normal, 1=Keylogger):", predictions)
print("Keylogger ehtimolligi (0.0-1.0):", probabilities)

# 9. Natijalarni saqlash
results = pd.DataFrame({
    'Prediction': predictions,
    'Keylogger_Probability': probabilities
})
results.to_csv(output_file, index=False)
print(f"Natijalar '{output_file}' fayliga saqlandi.")

print("Sinov muvaffaqiyatli yakunlandi!")