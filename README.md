# ⚡ BizForge — GenAI-Powered Branding Suite

> Powered by **IBM Granite** · **Groq LLaMA-3.3-70B** · **Stable Diffusion XL**

---

## 📁 Project Structure

```
BizForgeGenAI/
├── backend/
│   ├── main.py            ← FastAPI app (all routes)
│   ├── ai_services.py     ← All AI model integrations
│   ├── models.py          ← Pydantic request schemas
│   ├── requirements.txt   ← Python dependencies
│   └── .env               ← API keys (edit this!)
├── frontend/
│   ├── index.html         ← Landing page
│   ├── branding.html      ← All branding tools (tabs)
│   └── static/
│       ├── style.css
│       └── generated_logos/   ← Auto-created on run
├── setup.sh               ← Linux/Mac setup script
├── setup.bat              ← Windows setup script
└── README.md
```

---

## 🚀 Quick Start

### Step 1 — Get API Keys

| Service | URL | What it's used for |
|---------|-----|-------------------|
| **Groq Cloud** | https://console.groq.com | LLaMA-3.3-70B text generation |
| **Hugging Face** | https://huggingface.co/settings/tokens | IBM Granite model + SDXL images |

### Step 2 — Configure .env

Edit `backend/.env`:
```
GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
GROQ_MODEL="llama-3.3-70b-versatile"
HF_API_KEY="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
IBM_MODEL="ibm-granite/granite-4.0-h-350m"
```

### Step 3 — Install & Run

**Windows:**
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Linux / Mac:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Step 4 — Open in Browser

```
http://localhost:8000
```

---

## 🛠️ Features

| Feature | Endpoint | AI Model |
|---------|----------|----------|
| Brand Name Generator | POST /api/generate-brand | Groq LLaMA |
| Logo Prompt + Image | POST /api/generate-logo | Groq + SDXL |
| Marketing Content | POST /api/generate-content | Groq LLaMA |
| Design System / Colors | POST /api/get-colors | Groq LLaMA |
| Sentiment Analysis | POST /api/analyze-sentiment | Groq LLaMA |
| AI Branding Chat | POST /api/chat | IBM Granite (fallback: Groq) |
| Voice Transcription | POST /api/transcribe-voice | Google Speech-to-Text |

---

## ⚠️ Notes

- **IBM Granite** loads locally — this requires ~2GB RAM and takes 30-60s on first start.  
  If it fails to load, the chat falls back to Groq automatically — everything still works.
- **SDXL image generation** requires a valid `HF_API_KEY`. Without it, logo prompts still  
  generate (text only) — the image step is skipped gracefully.
- **Voice input** uses browser's Web Speech API (Chrome/Edge recommended) on the frontend,  
  with a server-side Google Speech Recognition fallback via file upload.

---

## 🔧 Troubleshooting

| Problem | Fix |
|---------|-----|
| `Groq API error` | Check GROQ_API_KEY in .env |
| `Granite load failed` | Normal on low RAM — chat uses Groq fallback |
| `SDXL 503 error` | HF model is loading — retry in 20s |
| `CORS error` | Make sure you access via `http://localhost:8000` |
| `Module not found` | Run `pip install -r requirements.txt` inside venv |
