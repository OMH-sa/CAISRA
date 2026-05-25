import cv2
import numpy as np
from ultralytics import YOLO

# ==========================================
# الإعدادات الأولية (Initial Setup)
# ==========================================

# 1. تحميل نموذج YOLOv8-Nano (الخفيف جداً والسرير) للتعرف على الأشخاص
try:
    print("Loading YOLOv8 model...")
    model = YOLO('yolov8n.pt') 
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Make sure ultralytics is installed: pip install ultralytics")
    exit()

# 2. إعداد الكاميرا (استخدام الكاميرا الافتراضية 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open camera.")
    exit()

# 3. إعدادات حساب التدفق البصري (Motion Detection)
# سنحتاج للإطار الأول لبدء المقارنة
ret, frame1 = cap.read()
if not ret:
    print("Error: Cannot read the first frame from the camera.")
    cap.release()
    exit()

# تحويل الإطار الأول للأبيض والأسود (الأسهل للحساب)
prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

# متغيرات لتخزين البيانات النهائية التي سيحتاجها الوكيل الذكي لاحقاً
motion_score = 0.0
face_detected = False
face_bbox = None # (x1, y1, x2, y2)

print("\n--- Visual Context Sensor Started ---")
print("Press 'q' on your keyboard to exit.")

# ==========================================
# حلقة التشغيل الرئيسية (Real-Time Loop)
# ==========================================
while cap.isOpened():
    # أ. قراءة الإطار الحالي
    ret, frame2 = cap.read()
    if not ret:
        break
    
    # نسخة من الإطار للعرض والرسم عليها
    output_frame = frame2.copy()
    
    # ب. تحويل الإطار الحالي للأبيض والأسود (لحساب الحركة)
    next_frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # ------------------------------------------
    # الجزء الأول: التعرف على المحتوى (Face/Person Detection)
    # ------------------------------------------
    # تشغيل النموذج على الإطار الحالي
    # verbose=False لعدم طباعة التفاصيل في موجه الأوامر كل إطار
    results = model(frame2, stream=True, verbose=False)
    
    face_detected = False
    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            # فئة 0 في مجموعة بيانات COCO هي 'person' (شخص)
            if cls == 0: 
                face_detected = True
                # الحصول على إحداثيات المربع المحيط (ROI) وتحويلها لأرقام صحيحة
                face_bbox = box.xyxy[0].cpu().numpy().astype(int)
                break # نكتفي باكتشاف شخص واحد لتبسيط النموذج الأولي
        if face_detected:
            break

    # ------------------------------------------
    # الجزء الثاني: حساب حركة المشهد (Dense Optical Flow)
    # ------------------------------------------
    # حساب التدفق البصري باستخدام خوارزمية Farneback
    # تقارن بين الإطار السابق والإطار الحالي
    flow = cv2.calcOpticalFlowFarneback(prvs, next_frame, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    
    # حساب "مستوى الحركة" (Motion Score)
    # نحسب حجم متجهات التدفق، ثم نأخذ متوسطها للمشهد كله
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    motion_score = np.mean(mag)
    
    # ------------------------------------------
    # الجزء الثالث: التصور والرسم (Visualization)
    # ------------------------------------------
    
    # 1. رسم المربع حول وجه المراسل (ROI) إذا تم اكتشافه
    if face_detected:
        x1, y1, x2, y2 = face_bbox
        # رسم مستطيل أخضر
        cv2.rectangle(output_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # كتابة نص توضيحي فوق المربع
        cv2.putText(output_frame, "Reporter (ROI)", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 2. عرض البيانات الرقمية على الشاشة
    # خلفية سوداء خفيفة للنص أسفل الشاشة
    overlay = output_frame.copy()
    cv2.rectangle(overlay, (0, output_frame.shape[0] - 80), (output_frame.shape[1], output_frame.shape[0]), (0, 0, 0), -1)
    # دمج الخلفية مع الإطار الأصلي بشفافية
    cv2.addWeighted(overlay, 0.6, output_frame, 0.4, 0, output_frame)

    # نص البيانات الذي سيتغير لحظياً
    data_text = f"Motion Score: {motion_score:.2f} | Face: {'YES' if face_detected else 'NO'}"
    cv2.putText(output_frame, data_text, (20, output_frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # ج. عرض الإطار النهائي للمستخدم
    cv2.imshow('CAISRA - Phase 1: Visual Context Sensor', output_frame)

    # د. تحديث الإطار "السابق" ليكون جاهزاً للمقارنة في الدورة القادمة
    prvs = next_frame

    # الخروج عند الضغط على مفتاح 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# تنظيف الموارد وإغلاق الكاميرا
cap.release()
cv2.destroyAllWindows()
print("\n--- Sensor stopped successfully ---")