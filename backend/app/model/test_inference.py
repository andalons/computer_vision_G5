import cv2
from app.model.inference import LogoDetector

def main():
    video_path = "videos_descargados/video_2e7c397a.mp4"
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"❌ No se pudo abrir el vídeo: {video_path}")
        return

    detector = LogoDetector()
    frame_count, detections_total = 0, []

    print(f"🎥 Analizando {video_path}...\n")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        detections = detector.predict_frame(frame, conf=0.25, iou=0.6)
        if detections:
            print(f"✅ Frame {frame_count}: {len(detections)} detección(es)")
            for det in detections:
                print(f"   🏷️ {det['class']} | "
                      f"Conf: {det['confidence']:.2f} | "
                      f"BBox: {det['bbox']}")
            detections_total.extend(detections)

        # ⚡ Solo procesar los primeros 200 frames para no tardar demasiado
        if frame_count >= 200:
            break

    cap.release()

    print("\n📊 RESUMEN")
    print(f"Total de frames analizados: {frame_count}")
    print(f"Total de detecciones: {len(detections_total)}")

    if detections_total:
        brands = {}
        for d in detections_total:
            brands[d["class"]] = brands.get(d["class"], 0) + 1
        print("Detecciones por marca:")
        for brand, count in brands.items():
            print(f"   {brand}: {count}")

if __name__ == "__main__":
    main()
