import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("--- Starting Network Data Simulation ---")

# ==========================================
# 1. إعداد المتغيرات (Setup Variables)
# ==========================================
total_seconds = 1000 # محاكاة 1000 ثانية من البث المباشر
time_steps = np.arange(total_seconds)

# ==========================================
# 2. توليد البيانات الطبيعية (Normal Network Behavior)
# ==========================================
# زمن الاستجابة (Ping) طبيعي حول 20ms مع تذبذب طفيف
ping = np.random.normal(loc=20.0, scale=2.0, size=total_seconds)
# التذبذب (Jitter) طبيعي حول 5ms
jitter = np.random.normal(loc=5.0, scale=1.0, size=total_seconds)
# فقدان الحزم (Packet Loss) صفر في الحالة الطبيعية
packet_loss = np.zeros(total_seconds)

# ==========================================
# 3. محاكاة الانهيار / الاختناق (Simulating Network Anomaly/Threat)
# ==========================================
# لنفترض أن البث سيتعرض لانهيار في الشبكة بين الثانية 600 والثانية 800
anomaly_start = 600
anomaly_end = 800

print(f"Injecting Network Anomaly between {anomaly_start}s and {anomaly_end}s...")

# زيادة هائلة في زمن الاستجابة (يصل إلى 150ms)
ping[anomaly_start:anomaly_end] += np.random.normal(loc=130.0, scale=15.0, size=(anomaly_end - anomaly_start))
# تذبذب عنيف جداً
jitter[anomaly_start:anomaly_end] += np.random.normal(loc=40.0, scale=5.0, size=(anomaly_end - anomaly_start))
# فقدان حزم عشوائي يصل إلى 10%
packet_loss[anomaly_start:anomaly_end] = np.random.uniform(low=1.0, high=10.0, size=(anomaly_end - anomaly_start))

# ==========================================
# 4. حفظ البيانات وعرضها (Save and Visualize)
# ==========================================
# تجميع البيانات في جدول (DataFrame)
df = pd.DataFrame({
    'Time(s)': time_steps,
    'Ping(ms)': ping,
    'Jitter(ms)': jitter,
    'Packet_Loss(%)': packet_loss
})

# حفظ البيانات في ملف CSV لكي يقرأه الذكاء الاصطناعي في المرحلة القادمة
df.to_csv('network_data.csv', index=False)
print("Data saved successfully to 'network_data.csv'.")

# رسم البيانات بيانيا لرؤية "شكل الخطر"
plt.figure(figsize=(12, 8))

# رسم الـ Ping
plt.subplot(3, 1, 1)
plt.plot(df['Time(s)'], df['Ping(ms)'], color='blue', label='Ping (ms)')
plt.axvspan(anomaly_start, anomaly_end, color='red', alpha=0.3, label='Network Threat')
plt.legend()
plt.title('Simulated Network Stream Health')

# رسم الـ Jitter
plt.subplot(3, 1, 2)
plt.plot(df['Time(s)'], df['Jitter(ms)'], color='orange', label='Jitter (ms)')
plt.axvspan(anomaly_start, anomaly_end, color='red', alpha=0.3)
plt.legend()

# رسم الـ Packet Loss
plt.subplot(3, 1, 3)
plt.plot(df['Time(s)'], df['Packet_Loss(%)'], color='red', label='Packet Loss (%)')
plt.axvspan(anomaly_start, anomaly_end, color='red', alpha=0.3)
plt.legend()
plt.xlabel('Time (seconds)')

plt.tight_layout()
print("Opening the chart... Close the chart window to end the script.")
plt.show()