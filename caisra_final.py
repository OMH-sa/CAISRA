import cv2
import numpy as np
from ultralytics import YOLO
import time

print("--- Starting CAISRA Final Integrated System ---")

# ==========================================
# 1. الإعدادات الأولية (System Initialization)
# ==========================================
model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open camera.")
    exit()

ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

start_time = time.time()
network_threat = False

print("\n[SYSTEM LIVE] Press 'q' to exit.")

# ==========================================
# 2. حلقة البث المباشر المتكاملة (Main Loop)
# ==========================================
while cap.isOpened():
    ret, frame2 = cap.read()
    if not ret:
        break
    
    output_frame = frame2.copy()
    next_frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    elapsed_time = int(time.time() - start_time)
    
    # محاكاة: انهيار الشبكة بين الثانية 10 و 30
    if 10 <= elapsed_time <= 30:
        network_threat = True
    else:
        network_threat = False

    # ------------------------------------------
    # أ. مستشعر المحتوى (YOLO & Optical Flow)
    # ------------------------------------------
    flow = cv2.calcOpticalFlowFarneback(prvs, next_frame, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    motion_score = np.mean(mag)
    
    results = model(frame2, stream=True, verbose=False)
    face_detected = False
    face_bbox = None
    
    for r in results:
        boxes = r.boxes
        for box in boxes:
            if int(box.cls[0]) == 0: 
                face_detected = True
                face_bbox = box.xyxy[0].cpu().numpy().astype(int)
                break
        if face_detected:
            break

    # ------------------------------------------
    # ب. عقل الوكيل الذكي (AI Agent Decision)
    # ------------------------------------------
    current_action = "NORMAL"
    
    if network_threat:
        # الحالة 1: يوجد وجه + حركة بطيئة = ضغط ذكي
        if face_detected and motion_score < 3.0:
            current_action = "SMART_COMPRESSION"
            
        # الحالة 2: لا يوجد وجه (الكاميرا موجهة لمنظر) + حركة الكاميرا عالية = وضع المشهد
        elif not face_detected and motion_score > 3.0:
            current_action = "SCENERY_MODE"
            
        # الحالة 3: حركة المراسل سريعة جداً = توجيه ديناميكي
        else:
            current_action = "DYNAMIC_ROUTING"

    # ------------------------------------------
    # ج. طبقة التنفيذ الفعلي (Execution Layer)
    # ------------------------------------------
    if current_action == "SMART_COMPRESSION" and face_detected:
        x1, y1, x2, y2 = face_bbox
        # استخدام القيمة 21 كما اتفقنا للحصول على عزل احترافي ومريح للعين
        blurred_frame = cv2.GaussianBlur(frame2, (21, 21), 0)
        
        mask = np.zeros_like(frame2)
        cv2.rectangle(mask, (x1, y1), (x2, y2), (255, 255, 255), -1)
        
        output_frame = np.where(mask == 255, frame2, blurred_frame)
        cv2.rectangle(output_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(output_frame, "Protected ROI", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    elif current_action == "DYNAMIC_ROUTING":
        cv2.putText(output_frame, "[ROUTING TO BACKUP SERVER...]", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)

    elif current_action == "SCENERY_MODE":
        # النظام يدرك أن هذا منظر مهم، فيحمي الصورة بالكامل من الضغط ويتجه للـ Routing
        cv2.putText(output_frame, "[SCENERY MODE: PROTECTING WIDE SHOT -> ROUTING]", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    # ------------------------------------------
    # د. لوحة التحكم والعرض (OSD / Dashboard)
    # ------------------------------------------
    overlay = output_frame.copy()
    cv2.rectangle(overlay, (0, 0), (output_frame.shape[1], 110), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, output_frame, 0.4, 0, output_frame)

    network_status = "DANGER (Drop)" if network_threat else "STABLE"
    color_status = (0, 0, 255) if network_threat else (0, 255, 0)
    
    cv2.putText(output_frame, f"TIME: {elapsed_time}s | NETWORK: {network_status}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_status, 2)
    cv2.putText(output_frame, f"MOTION SCORE: {motion_score:.2f}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(output_frame, f"AGENT ACTION: {current_action}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow('CAISRA - Final Integrated Prototype', output_frame)
    prvs = next_frame

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("\n--- CAISRA System Shutdown ---")