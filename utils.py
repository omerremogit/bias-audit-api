import os
import cv2
import numpy as np
import pandas as pd
import mediapipe as mp


def extract_face_embedding(image_rgb):
    mp_face_mesh = mp.solutions.face_mesh
    with mp_face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True) as face_mesh:
        results = face_mesh.process(image_rgb)
        if not results.multi_face_landmarks:
            return None

        landmarks = results.multi_face_landmarks[0].landmark
        embedding = np.array([[l.x, l.y, l.z] for l in landmarks]).flatten()
        return embedding / np.linalg.norm(embedding)


def load_dataset(dataset_path):
    mp_face_detection = mp.solutions.face_detection
    data = []

    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detector:
        for idx, file in enumerate(os.listdir(dataset_path)):
            try:
                if not file.lower().endswith((".jpg", ".jpeg", ".png")):
                    continue

                print(f"🖼️ [{idx}] Processing {file}")

                # Parse metadata from filename (age_gender_race_date.jpg)
                age, gender, race, _ = file.split("_")
                img_path = os.path.join(dataset_path, file)

                # Load image with OpenCV
                image_bgr = cv2.imread(img_path)
                if image_bgr is None:
                    print(f"⚠️ Failed to load image {file}")
                    continue

                image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
                h, w, _ = image_rgb.shape

                # Detect face
                results = face_detector.process(image_rgb)

                if results.detections:
                    print(f"✅ Face detected in {file}")
                    embedding = extract_face_embedding(image_rgb)
                    if embedding is not None:
                        print(f"💾 Encoding successful for {file}")
                        data.append({
                            "filename": file,
                            "gender": int(gender),
                            "race": int(race),
                            "encoding": embedding
                        })
                    else:
                        print(f"⚠️ Encoding failed for {file}")
                else:
                    print(f"❌ No face found in {file}")

            except Exception as e:
                print(f"🔥 Skipping {file}: {e}")
                continue

    return pd.DataFrame(data)