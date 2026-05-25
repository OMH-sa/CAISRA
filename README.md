```markdown
# CAISRA: Content-Aware Intelligent Stream Routing Agent 
**Developed by:** [Osama Hurubi](https://github.com/OMH-sa)

**CAISRA** is a state-of-the-art, proactive AI system designed to eliminate live broadcasting latency and stream disruptions (buffering) caused by unexpected network drops. 

Instead of traditional reactive methods (which degrade video quality after the network fails), CAISRA uses a combination of **Time-Series Threat Detection** and **Lightweight Computer Vision** to anticipate network anomalies and execute content-aware mitigation strategies in real-time.

---

##  Key Features

* **Proactive Threat Detection:** Simulates and detects network bandwidth drops (Ping, Jitter, Packet Loss) using AI anomaly detection.
* **Content-Aware Vision:** Utilizes `YOLOv8-Nano` for real-time Reporter Face Detection (ROI) and `Farneback Optical Flow` for scene motion estimation.
* **Smart RoI Compression:** During a network drop in a static scene, the AI Agent applies an elegant professional blur (Gaussian Blur 21x21) to the background while maintaining crisp 4K bitrate focus exclusively on the reporter's face.
* **Dynamic Scenery Mode:** If the camera pans to a crowd or landscape (No Face + High Motion), the system intelligently aborts compression to avoid motion blur and switches to `[DYNAMIC ROUTING]` to protect the wide shot.
* **Real-Time OSD Dashboard:** On-Screen Display indicating network health, motion scores, and instantaneous AI Agent decisions.

---

##  Technology Stack

* **Language:** Python 3.x
* **Computer Vision:** OpenCV (`cv2`)
* **Object Detection:** Ultralytics (YOLOv8-Nano)
* **Machine Learning / AI:** Scikit-learn (Isolation Forest for Anomaly Detection)
* **Data Processing:** Pandas, NumPy
* **Visualization:** Matplotlib

---

##  Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/OMH-sa/CAISRA.git](https://github.com/OMH-sa/CAISRA.git)
   cd CAISRA

```

2. **Create and activate a virtual environment (Recommended):**
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

```


3. **Install dependencies:**
```bash
pip install opencv-python numpy ultralytics scikit-learn pandas matplotlib

```



---

##  Usage

Run the final integrated prototype. Ensure your webcam is connected.

```bash
python caisra_final.py

```

###  Simulation Scenario (caisra_final.py):

* **0s to 10s:** The network is stable. The stream runs normally with no compression.
* **10s to 30s:** A simulated network drop occurs!
* *If you are sitting still:* The background beautifully blurs (Smart Compression) protecting the bandwidth for your face.
* *If you move out of frame and pan the camera:* The AI detects a scenery shot, disables compression, and initiates dynamic backup routing.


* **30s onwards:** The network recovers, and the stream returns to normal. Press `q` to exit.

---

##  Project Structure

* `sensor.py`: Phase 1 - Independent visual context and motion tracking module.
* `network_sim.py`: Phase 2 - Generates synthetic time-series network data with injected anomalies.
* `threat_detector.py`: Phase 2b - Isolation Forest ML model to detect network threats.
* `agent.py`: Phase 3 - The logic matrix of the AI decision-making agent.
* `caisra_final.py`: **Phase 4 - The complete, integrated real-time prototype.**

---

*Designed and engineered by [Osama Hurubi](https://github.com/OMH-sa) as a conceptual solution for modern live-broadcasting challenges.*

```

```