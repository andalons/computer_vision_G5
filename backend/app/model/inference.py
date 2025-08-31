"""
ONNX model inference utilities
"""
import onnxruntime as ort
import numpy as np
import cv2

# Load the model once at startup
MODEL_PATH = "backend/app/model/brand_model.onnx"
session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])

def preprocess_frame(frame):
    """
    Preprocess frame before feeding it into the ONNX model.
    """
    # Resize to 640x640 (what the model expects)
    resized = cv2.resize(frame, (640, 640))
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    arr = rgb.astype(np.float32) / 255.0   # normalize [0,1]

    # Shape: (H, W, C) -> (N, C, H, W)
    arr = np.transpose(arr, (2, 0, 1))     # (3, 640, 640)
    arr = np.expand_dims(arr, axis=0)      # (1, 3, 640, 640)
    return arr

def predict_brand(frame):
    """
    Run inference on a video frame.
    Returns model raw outputs (probabilities, boxes, etc).
    """
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    inp = preprocess_frame(frame)
    preds = session.run([output_name], {input_name: inp})[0]

    return preds

# Lista de clases entrenadas (ejemplo, cámbiala según tu dataset YOLO)
CLASSES = ["361", "adidas", "anta", "erke", "kappa", "lining", "nb", "nike", "puma", "xtep"]

def postprocess(predictions, conf_threshold=0.25, iou_threshold=0.45, img_size=640):
    """
    Postprocess YOLO ONNX outputs into bounding boxes, confidences, and class labels.
    """
    # Shape (1, 14, 8400) -> (8400, 14)
    preds = np.squeeze(predictions).T

    print("🔍 Raw prediction sample (first 5 rows):")
    print(preds[:5])  

    boxes = preds[:, :4]   # x, y, w, h
    scores = preds[:, 4]   # objectness
    class_probs = preds[:, 5:]  # class probabilities

    results = []

    for i in range(len(boxes)):
        box = boxes[i]
        score = scores[i]
        class_id = np.argmax(class_probs[i])
        class_score = class_probs[i][class_id] * score

        if class_score < conf_threshold:
            continue

        # YOLO gives center_x, center_y, width, height → convert to x1,y1,x2,y2
        cx, cy, w, h = box
        x1 = int((cx - w/2))
        y1 = int((cy - h/2))
        x2 = int((cx + w/2))
        y2 = int((cy + h/2))

        results.append({
            "class": CLASSES[class_id] if class_id < len(CLASSES) else f"class_{class_id}",
            "confidence": float(class_score),
            "bbox": [x1, y1, x2, y2]
        })

    # Aplicar NMS (Non-Maximum Suppression)
    results = non_max_suppression(results, iou_threshold)
    return results


def non_max_suppression(detections, iou_threshold=0.45):
    """
    Simple NMS to remove overlapping bounding boxes.
    """
    if not detections:
        return []

    detections = sorted(detections, key=lambda x: x["confidence"], reverse=True)
    final_dets = []

    while detections:
        best = detections.pop(0)
        final_dets.append(best)
        detections = [d for d in detections if iou(d["bbox"], best["bbox"]) < iou_threshold]

    return final_dets


def iou(box1, box2):
    """
    Compute IoU between two boxes [x1, y1, x2, y2]
    """
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

    union = box1_area + box2_area - inter_area
    return inter_area / union if union > 0 else 0
