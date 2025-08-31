import cv2
from inference import predict_brand, postprocess

def main():
    video_path = "videos_descargados/video_2e7c397a.mp4"
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    detections_total = []
    block_size = 50   # nº de frames por bloque
    max_blocks = 20   # seguridad: no más de 20 bloques (1000 frames)

    while cap.isOpened() and len(detections_total) == 0 and (frame_count // block_size) < max_blocks:
        print(f"\n🔍 Revisando frames {frame_count} → {frame_count + block_size}...")
        block_detections = []

        for i in range(block_size):
            ret, frame = cap.read()
            if not ret:
                break

            preds = predict_brand(frame)
            results = postprocess(preds, conf_threshold=0.001)  # umbral bajo para debug
            if results:
                print(f"✅ Frame {frame_count+i}: {results}")
                block_detections.extend(results)

        detections_total.extend(block_detections)
        frame_count += block_size

    cap.release()

    if detections_total:
        print(f"\n🎯 Encontradas {len(detections_total)} detecciones en {frame_count} frames")
    else:
        print("\n⚠️ No se detectó nada en los primeros", frame_count, "frames")

if __name__ == "__main__":
    main()