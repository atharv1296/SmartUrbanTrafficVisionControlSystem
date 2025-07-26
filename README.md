# **Smart Urban Traffic Vision & Control System** 🚦🤖🚗🚑

A real-time traffic monitoring and control system that uses **YOLO object detection** to count vehicles, detect ambulances, estimate speeds, and dynamically adjust traffic signals.

---

## **Features**
✅ **Vehicle Detection** - Counts cars, trucks, buses, motorcycles, and ambulances  
🚑 **Ambulance Priority** - Emergency vehicle detection triggers signal override  
📊 **Traffic Analytics** - Logs vehicle counts, speeds, and congestion to MySQL  
📈 **Dynamic Signal Timing** - Adjusts green light duration based on traffic density  
📷 **Multi-Camera Support** - Processes feeds from 4 directions (North, South, East, West)  
⚡ **GPU Acceleration** - Uses PyTorch with CUDA for fast inference  

---

## **Installation**

### **1. Prerequisites**
- Python 3.8+
- NVIDIA GPU (Recommended) with CUDA 11.8
- MySQL Server

### **2. Clone the Repository**
```bash
git clone https://github.com/atharv1296/SmartUrbanTrafficVision&ControlSystem
```

### **3. Set Up Virtual Environment**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\activate   # Windows
```

### **4. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **5. Database Setup**
1. Create a MySQL database named `traffic_db`
2. Update `config.py` with your MySQL credentials:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'your_username',
       'password': 'your_password',
       'database': 'traffic_db'
   }
   ```
3. Run the setup script:
   ```bash
   python -m traffic_system.database.db_setup
   ```

---

## **Usage**
```bash
python main.py
```

## **Configuration**
Edit `config.py` to customize:
- Camera sources (RTSP/HTTP/IP cameras)
- Traffic light timing parameters
- Detection sensitivity thresholds

```python
# Minimum/Maximum green light duration (seconds)
DAY_MIN_GREEN = 15
DAY_MAX_GREEN = 120

# Vehicle classes to detect
VEHICLE_CLASSES = {'car', 'motorcycle', 'bus', 'truck', 'ambulance'}
```

---

## **Project Structure**
```
traffic_management_system/
│
├── .gitattributes
├── README.md
├── requirements.txt
│
├── resources/
│   ├── videos/
│   ├── mask.png
│   └── key.json
│
├── Yolo-Weights/
│   ├── yolov8l.pt
│   └── yolov12l.pt
│
└── traffic_system/
    ├── main.py
    ├── config.py
    ├── traffic_control.py
    │
    ├── database/
    │   ├── db_setup.py
    │   └── db_operations.py
    │
    ├── detection/
    │   ├── vehicle_counter.py
    │   └── speed_estimator.py
    │
    ├── models/
    │   └── yolo_model.py
    │
    └── utils/
        └── visualization.py               
```

---

## **Troubleshooting**
- **CUDA Errors**: Verify compatible PyTorch+CUDA versions
- **MySQL Connection Issues**: Check credentials in `config.py`
- **Camera Feed Problems**: Test RTSP/HTTP streams with VLC first

---

**Developed by [Atharv Pawar]**  
📧 Contact: atharvpawar1296@gmail.com  
🌐 GitHub: [github.com/atharv1296](https://github.com/atharv1296)  

---

🚀 **Happy Traffic Optimizing!** 🚀  

---

### **Screenshot**
![Traffic System Demo](Photos\Screenshot 2025-07-27 005640.png) *(Example visualization of vehicle detection)*

---
