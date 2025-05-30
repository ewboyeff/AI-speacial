
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

# FastAPI ilovasini yaratish
app = FastAPI(
    title="Malaria Detection API",
    description="Bu API foydalanuvchi yuklagan rasmni tahlil qilib, malaria kasalligini aniqlaydi.",
    version="1.0.0"
)

# CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelni yuklash
MODEL_PATH = "output/malaria_cnn_final.h5"
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model muvaffaqiyatli yuklandi!")
except Exception as e:
    print(f"Modelni yuklashda xatolik: {e}")
    raise Exception("Modelni yuklashda xatolik yuz berdi!")

# Rasmni qayta ishlash funksiyasi
def preprocess_image(image: Image.Image, target_size=(128, 128)):
    try:
        image = image.resize(target_size, Image.Resampling.LANCZOS)
        img_array = np.array(image)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Rasmni qayta ishlashda xatolik: {str(e)}")

# Bashorat qilish funksiyasi
def predict_image(img_array):
    try:
        prediction = model.predict(img_array, verbose=0)
        raw_prediction = prediction[0][0]  # Asl ehtimollik
        class_idx = int(prediction > 0.5)
        # Bashoratni teskari qilamiz, chunki model noto'g'ri o'qitilgan bo'lishi mumkin
        class_idx = 1 - class_idx  # 0 ni 1 ga, 1 ni 0 ga o'zgartiramiz
        # Confidence ni yaxshilash uchun asl ehtimollikni teskari qilamiz
        confidence = 1 - raw_prediction if class_idx == 1 else raw_prediction
        class_label = ['Uninfected', 'Infected'][class_idx]
        return class_label, float(confidence)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bashorat qilishda xatolik: {str(e)}")

# API endpoint
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Faqat rasm fayllari qabul qilinadi!")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        img_array = preprocess_image(image)
        class_label, confidence = predict_image(img_array)
        return JSONResponse(content={
            "status": "success",
            "prediction": class_label,
            "confidence": confidence
        })
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Xatolik yuz berdi: {str(e)}")

# API ni ishga tushirish uchun asosiy kod
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

