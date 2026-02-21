import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from models import (
    BrandRequest, ContentRequest, SentimentRequest,
    ColorRequest, ChatRequest, LogoRequest,
)
from ai_services import (
    generate_brand_names,
    generate_marketing_content,
    analyze_sentiment,
    get_color_palette,
    chat_with_ai,
    generate_logo_prompt,
    generate_logo_image,
)

load_dotenv()

app = FastAPI(title="BizForge API", version="1.0.0")

# ─── CORS ────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── PATHS ───────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
frontend_path = BASE_DIR / "frontend"
static_path = frontend_path / "static"

os.makedirs(static_path / "generated_logos", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


# ─── FRONTEND ROUTES ─────────────────────────────────────────────────────────
@app.get("/")
async def serve_index():
    return FileResponse(str(frontend_path / "index.html"))


@app.get("/branding")
async def serve_branding():
    return FileResponse(str(frontend_path / "branding.html"))


@app.get("/{page}.html")
async def serve_page(page: str):
    file_path = frontend_path / f"{page}.html"
    if file_path.exists():
        return FileResponse(str(file_path))
    return FileResponse(str(frontend_path / "index.html"))


# ─── API ROUTES ──────────────────────────────────────────────────────────────

@app.post("/api/generate-brand")
async def generate_brand_endpoint(request: BrandRequest):
    try:
        result = await generate_brand_names(
            request.industry,
            request.keywords,
            request.tone,
            request.language,
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-content")
async def generate_content_endpoint(request: ContentRequest):
    try:
        result = await generate_marketing_content(
            request.brand_description,
            request.tone,
            request.content_type,
            request.language,
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze-sentiment")
async def analyze_sentiment_endpoint(request: SentimentRequest):
    try:
        result = await analyze_sentiment(request.text, request.brand_tone)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/get-colors")
async def get_colors_endpoint(request: ColorRequest):
    try:
        result = await get_color_palette(request.tone, request.industry)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        result = await chat_with_ai(request.message)
        return {"success": True, "data": {"content": result}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-logo")
async def generate_logo_endpoint(request: LogoRequest):
    try:
        # Step 1: Generate logo prompt via Groq
        logo_prompt_text = await generate_logo_prompt(
            request.brand_name, request.industry, request.keywords
        )
        # Step 2: Generate image via SDXL
        image_result = await generate_logo_image(logo_prompt_text)
        return {
            "success": True,
            "data": {
                "logo_prompt": logo_prompt_text,
                "image_url": image_result.get("image_url"),
                "image_generated": image_result.get("success", False),
                "image_error": image_result.get("error"),
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/transcribe-voice")
async def transcribe_voice(audio_file: UploadFile = File(...)):
    try:
        import speech_recognition as sr
        from io import BytesIO

        audio_content = await audio_file.read()
        temp_path = "temp_audio.wav"
        with open(temp_path, "wb") as f:
            f.write(audio_content)

        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)

        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

        return {"success": True, "text": text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Transcription failed: {str(e)}")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "BizForge API"}


# ─── STARTUP ─────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    print("\n" + "=" * 60)
    print("🚀 BizForge Backend Started!")
    print("=" * 60)
    print("🌐 API running at http://localhost:8000")
    print(f"📁 Frontend path: {frontend_path}")
    print(f"🖼️  Static files: {static_path}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

