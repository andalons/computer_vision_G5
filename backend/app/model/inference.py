import cv2
from ultralytics import YOLO
from backend.app.model.download_model import get_model_path

# Variable global del detector
global_detector = None

class LogoDetector:
    def __init__(self):
        model_path = get_model_path()
        self.model = YOLO(model_path)
        self.class_names = self.model.names  

    def predict_frame(self, frame, conf=0.35, iou=0.5, stream_buffer=True):
        """
        Corre predicción YOLO en un frame.
        Devuelve detecciones como lista de dicts.
        """
        results = self.model.predict(
            source=frame,
            conf=conf,
            iou=iou,
            verbose=False
        )

        detections = []
        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf_score = float(box.conf[0])
            class_id = int(box.cls[0])
            detections.append({
                "class": self.class_names[class_id],
                "confidence": conf_score,
                "bbox": [int(x1), int(y1), int(x2), int(y2)]
            })
        return detections


def preload_detector():
    """
    Precarga el modelo en memoria para evitar retrasos
    cuando se llame por primera vez desde el endpoint.
    """
    global global_detector
    if global_detector is None:
        print("🔄 Precargando modelo YOLO...")
        global_detector = LogoDetector()
        print("✅ Modelo YOLO cargado en memoria")
    return global_detector
