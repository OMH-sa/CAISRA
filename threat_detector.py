import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

print("--- Starting AI Threat Detection Model ---")

# ==========================================
# 1. تحميل بيانات الشبكة (Load Data)
# ==========================================
try:
    df = pd.read_csv('network_data.csv')
    print("Data loaded successfully.")
except FileNotFoundError:
    print("Error: 'network_data.csv' not found. Please run network_sim.py first.")
    exit()

# المتغيرات التي سيتعلم منها الذكاء الاصطناعي
features = ['Ping(ms)', 'Jitter(ms)', 'Packet_Loss(%)']
X = df[features]

# ==========================================
# 2. بناء وتدريب نموذج الذكاء الاصطناعي (Train Model)
# ==========================================
print("Training Isolation Forest Anomaly Detector...")

# contamination: نسبة البيانات التي نتوقع أن تكون "خبيثة" أو بها خلل (وضعناها 20%)
model = IsolationForest(contamination=0.2, random_state=42)

# التدريب والاكتشاف في نفس الوقت
# النموذج سيعيد قيمة (-1) للبيانات الشاذة/الخطر، وقيمة (1) للبيانات الطبيعية
df['Anomaly_Score'] = model.fit_predict(X)

# تحويل القيم لتكون أسهل في الفهم: 1 = خطر، 0 = طبيعي
df['Threat_Detected'] = df['Anomaly_Score'].apply(lambda x: 1 if x == -1 else 0)

print("Training complete! Threats identified.")

# ==========================================
# 3. عرض النتائج وتحليل ذكاء النموذج (Visualization)
# ==========================================
# سنقوم برسم خط يوضح الـ Ping، ونضع نقاطاً حمراء حيث اكتشف الذكاء الاصطناعي الخطر
plt.figure(figsize=(12, 6))

# رسم مسار البيانات الطبيعي (Ping)
plt.plot(df['Time(s)'], df['Ping(ms)'], color='blue', label='Ping (ms) - Normal', alpha=0.6)

# استخراج النقاط التي قرر النظام أنها (تهديد / انقطاع)
threats = df[df['Threat_Detected'] == 1]

# رسم النقاط الحمراء فوق الأماكن الخطرة
plt.scatter(threats['Time(s)'], threats['Ping(ms)'], color='red', label='AI Detected Threat!', s=20)

plt.title('AI Network Threat Detection (Isolation Forest)')
plt.xlabel('Time (seconds)')
plt.ylabel('Ping (ms)')
plt.legend()
plt.tight_layout()

print("Opening results chart... Close the window to end the script.")
plt.show()