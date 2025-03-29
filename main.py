from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
import mediapipe as mp
from audit import audit_encoding

app = FastAPI()


def extract_face_embedding(image_rgb):
    mp_face_mesh = mp.solutions.face_mesh
    with mp_face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True) as face_mesh:
        results = face_mesh.process(image_rgb)
        if not results.multi_face_landmarks:
            return None

        landmarks = results.multi_face_landmarks[0].landmark
        embedding = np.array([[l.x, l.y, l.z] for l in landmarks]).flatten()
        return embedding / np.linalg.norm(embedding)


@app.post("/audit/")
async def audit_image(file: UploadFile = File(...)):
    contents = await file.read()
    with open("temp.jpg", "wb") as f:
        f.write(contents)

    image_bgr = cv2.imread("temp.jpg")
    if image_bgr is None:
        return {"error": "Invalid image"}

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    embedding = extract_face_embedding(image_rgb)

    if embedding is None:
        return {"error": "No face detected or encoding failed."}

    audit_result = audit_encoding(embedding)
    return audit_result
