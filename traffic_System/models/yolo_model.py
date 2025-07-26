import torch
from ultralytics import YOLO

def load_yolo_model(model_path):
    try:
        model = YOLO(model_path).cuda()
        model.fuse()
        model.eval()
        print("YOLO model loaded successfully")
        
        # Print GPU information
        print(f"CUDA available: {torch.cuda.is_available()}")
        print(f"CUDA device count: {torch.cuda.device_count()}")
        if torch.cuda.is_available():
            print(torch.cuda.get_device_name(0))
            
        return model
    except Exception as e:
        print(f"Failed to load YOLO model: {e}")
        exit(1)