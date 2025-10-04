from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageEnhance, ImageFilter
import io, base64

app = FastAPI()

# allowing access to the front
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def pil_to_base64(img: Image.Image):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

@app.post("/process")
async def process(file: UploadFile = File(...), phase: str = Form(...)):
    image = Image.open(io.BytesIO(await file.read()))

    if phase == "arterial":
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
    elif phase == "venous":
        image = image.filter(ImageFilter.GaussianBlur(2))

    return {"image": pil_to_base64(image)}
