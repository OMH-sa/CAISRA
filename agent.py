import time
import random

print("--- Starting CAISRA Intelligent Agent ---")

# ==========================================
# 1. تعريف الوكيل الذكي (Define The AI Agent)
# ==========================================
class CaisraAgent:
    def __init__(self, motion_threshold=3.0):
        # الحد الفاصل بين المشهد الثابت والمتحرك
        self.motion_threshold = motion_threshold

    def make_decision(self, network_threat, motion_score):
        """
        هذه الدالة تمثل عقل الوكيل الذكي الذي يحلل المدخلات ويتخذ القرار
        """
        # الحالة الأولى: الشبكة مستقرة (لا يوجد تهديد)
        if not network_threat:
            return "NORMAL", "Stream is stable. Maximum 4K Quality."

        # الحالة الثانية: يوجد تهديد + المشهد ثابت (حركة بطيئة)
        if motion_score < self.motion_threshold:
            return "SMART_COMPRESSION", "Threat! Static Scene -> Action: Compressing Background (ROI)."

        # الحالة الثالثة: يوجد تهديد + المشهد متحرك (حركة سريعة)
        else:
            return "DYNAMIC_ROUTING", "Threat! Dynamic Scene -> Action: Switching to Backup Server."

# ==========================================
# 2. محاكاة البث المباشر (Simulating Live Stream)
# ==========================================
# تشغيل الوكيل الذكي
agent = CaisraAgent(motion_threshold=3.0)

# سنقوم بمحاكاة 10 ثوانٍ من البث المباشر بأحداث مختلفة
simulated_events = [
    {"time": 1, "threat": False, "motion": 1.2, "scenario": "Reporter is standing still, good network."},
    {"time": 2, "threat": False, "motion": 1.5, "scenario": "Reporter is standing still, good network."},
    {"time": 3, "threat": True,  "motion": 1.1, "scenario": "NETWORK DROP! Reporter is still standing."},
    {"time": 4, "threat": True,  "motion": 1.4, "scenario": "Network still bad. Reporter standing."},
    {"time": 5, "threat": False, "motion": 5.8, "scenario": "Network recovered. Reporter starts running!"},
    {"time": 6, "threat": False, "motion": 6.2, "scenario": "Network good. Reporter running."},
    {"time": 7, "threat": True,  "motion": 7.1, "scenario": "NETWORK DROP AGAIN! Reporter is running!"},
    {"time": 8, "threat": True,  "motion": 6.8, "scenario": "Network bad. Reporter running."},
    {"time": 9, "threat": False, "motion": 1.0, "scenario": "Network recovered. Reporter stops."},
]

print("\n[LIVE BROADCAST STARTED]\n")
print("-" * 70)
print(f"{'SEC':<5} | {'NETWORK THREAT':<15} | {'MOTION':<8} | {'AGENT DECISION (ACTION)':<20}")
print("-" * 70)

# ==========================================
# 3. تشغيل الحلقة الزمنية (Real-Time Loop)
# ==========================================
for event in simulated_events:
    time.sleep(1.5) # الانتظار لثانية ونصف لمحاكاة الوقت الفعلي
    
    # قراءة البيانات اللحظية
    current_threat = event["threat"]
    current_motion = event["motion"]
    
    # إرسال البيانات للوكيل الذكي ليتخذ القرار
    action, explanation = agent.make_decision(current_threat, current_motion)
    
    # طباعة حالة النظام والقرار
    threat_status = "DANGER!" if current_threat else "SAFE"
    print(f"{event['time']:<5} | {threat_status:<15} | {current_motion:<8} | [{action}]")
    print(f"      -> AI Thought Process: {explanation}")
    print("-" * 70)

print("\n[LIVE BROADCAST ENDED]")