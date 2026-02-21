import os
import time
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
HF_API_KEY = os.getenv("HF_API_KEY", "")
IBM_MODEL = os.getenv("IBM_MODEL", "ibm-granite/granite-4.0-h-350m")

# ==================== GROQ CLIENT ====================
groq_client = None
try:
    from groq import Groq
    if GROQ_API_KEY:
        groq_client = Groq(api_key=GROQ_API_KEY)
        print("✅ Groq client initialized!")
    else:
        print("⚠️  Warning: GROQ_API_KEY not set in .env")
except Exception as e:
    print(f"❌ Groq init failed: {e}")

# ==================== IBM GRANITE (LOCAL) ====================
granite_model = None
granite_tokenizer = None

def load_granite():
    global granite_model, granite_tokenizer
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        device = "cpu"
        model_id = IBM_MODEL
        print(f"🔷 Loading IBM Granite {model_id}...")
        granite_tokenizer = AutoTokenizer.from_pretrained(
            model_id, trust_remote_code=True, token=HF_API_KEY or None
        )
        granite_model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float32,
            trust_remote_code=True,
            token=HF_API_KEY or None,
        ).to(device)
        granite_model.eval()
        print("✅ IBM Granite loaded!")
    except Exception as e:
        print(f"❌ Granite load failed: {e}")
        granite_model = None
        granite_tokenizer = None

# Attempt to load Granite at startup
load_granite()


# ==================== HELPER: GROQ TEXT GENERATION ====================
async def generate_with_groq(prompt: str, max_tokens: int = 500, system: str = "") -> str:
    if not groq_client:
        return "❌ Error: Groq API key not configured. Please add GROQ_API_KEY to your .env file."
    try:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.8,
            top_p=0.95,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Groq generation error: {str(e)}"


# ==================== HELPER: IBM GRANITE CHAT ====================
async def generate_with_granite(prompt: str, max_new_tokens: int = 300) -> str:
    if granite_model is None or granite_tokenizer is None:
        # Fallback to Groq for chat if Granite not loaded
        return await generate_with_groq(
            prompt,
            max_tokens=300,
            system="You are BizForge, an expert AI branding assistant. Give concise, actionable branding advice.",
        )
    try:
        import torch
        inputs = granite_tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = granite_model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.7,
                pad_token_id=granite_tokenizer.eos_token_id,
            )
        full = granite_tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Return only newly generated text
        return full[len(prompt):].strip() or full.strip()
    except Exception as e:
        return f"❌ Granite error: {str(e)}"


# ==================== FEATURE FUNCTIONS ====================

async def generate_brand_names(industry: str, keywords: str, tone: str, language: str) -> str:
    system = (
        "You are BizForge, a creative AI branding expert. Generate unique, memorable, "
        "brand-ready names. Be creative and original."
    )
    prompt = (
        f"Generate 10 unique brand name suggestions for a {tone.lower()} {industry} brand. "
        f"Keywords/themes: {keywords}. "
        f"For each name, provide: the name in bold, a one-line tagline, and why it works. "
        f"Format as a numbered list. Language: {language}."
    )
    return await generate_with_groq(prompt, max_tokens=600, system=system)


async def generate_marketing_content(
    brand_description: str, tone: str, content_type: str, language: str
) -> str:
    system = (
        "You are BizForge, an expert marketing copywriter. Create compelling, "
        "on-brand marketing content that converts."
    )
    type_map = {
        "product_description": "product description",
        "social_post": "social media post (Instagram/LinkedIn)",
        "email": "professional marketing email",
        "ad_copy": "advertisement copy",
        "tagline": "brand tagline and slogan options",
    }
    readable_type = type_map.get(content_type, content_type)
    prompt = (
        f"Create a {tone.lower()}-toned {readable_type} for this brand: '{brand_description}'. "
        f"Make it engaging, authentic, and persuasive. Language: {language}."
    )
    return await generate_with_groq(prompt, max_tokens=500, system=system)


async def analyze_sentiment(text: str, brand_tone: str) -> str:
    system = (
        "You are BizForge, an expert in brand communication and sentiment analysis. "
        "Provide structured, actionable insights."
    )
    prompt = (
        f"Analyze this customer review/text and provide:\n"
        f"1. **Overall Sentiment**: (Positive/Neutral/Negative) with confidence %\n"
        f"2. **Key Points Mentioned**: bullet list\n"
        f"3. **Emotional Tone**: description\n"
        f"4. **Brand Tone Alignment**: how well it aligns with '{brand_tone}' brand tone\n"
        f"5. **Professional Rewrite**: rewrite it in a professional, polished tone\n\n"
        f"Text to analyze:\n\"{text}\""
    )
    return await generate_with_groq(prompt, max_tokens=600, system=system)


async def get_color_palette(tone: str, industry: str) -> str:
    system = (
        "You are BizForge, a professional brand identity designer. "
        "Provide specific, actionable color recommendations."
    )
    prompt = (
        f"Create a complete brand color palette for a {tone.lower()} {industry} brand. Provide:\n"
        f"1. **Primary Color**: HEX code + name + why it works\n"
        f"2. **Secondary Color**: HEX code + name + usage\n"
        f"3. **Accent Color**: HEX code + name + usage\n"
        f"4. **Background Color**: HEX code\n"
        f"5. **Text Color**: HEX code\n"
        f"6. **Font Pairing**: recommended heading + body font\n"
        f"7. **Overall Mood**: 2-sentence description\n"
        f"Format clearly with HEX codes prominently displayed."
    )
    return await generate_with_groq(prompt, max_tokens=500, system=system)


async def chat_with_ai(message: str) -> str:
    system = (
        "You are BizForge, an expert AI branding assistant powered by IBM Granite. "
        "You help startups and entrepreneurs with branding strategy, naming, identity, "
        "marketing, and business growth. Be concise, warm, and actionable."
    )
    prompt = f"User question: {message}"
    return await generate_with_granite(prompt)


async def generate_logo_prompt(brand_name: str, industry: str, keywords: str) -> str:
    system = (
        "You are BizForge, an expert brand designer. Generate professional, "
        "detailed logo prompts suitable for AI image generation."
    )
    prompt = (
        f"Create a detailed, professional logo generation prompt for:\n"
        f"- Brand Name: {brand_name}\n"
        f"- Industry: {industry}\n"
        f"- Keywords/Style: {keywords}\n\n"
        f"Provide:\n"
        f"1. **Logo Concept**: detailed description of the logo design\n"
        f"2. **DALL-E/Midjourney Prompt**: ready-to-use image generation prompt\n"
        f"3. **Style Notes**: colors, typography, iconography guidance\n"
        f"4. **Logo Variations**: suggest 2-3 alternative concepts"
    )
    return await generate_with_groq(prompt, max_tokens=500, system=system)


async def generate_logo_image(logo_prompt: str) -> dict:
    """Generate logo image using HuggingFace SDXL Inference API."""
    if not HF_API_KEY:
        return {
            "success": False,
            "image_url": None,
            "error": "HF_API_KEY not configured. Please add it to .env",
        }
    try:
        import requests as req
        enhanced = (
            f"Professional brand logo: {logo_prompt}. "
            "Modern minimalist vector design, clean lines, white background, "
            "high quality, professional branding."
        )
        api_url = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        payload = {"inputs": enhanced}
        response = req.post(api_url, headers=headers, json=payload, timeout=60)

        if response.status_code == 200:
            # Use absolute path relative to this file
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            logos_dir = os.path.join(BASE_DIR, "frontend", "static", "generated_logos")
            os.makedirs(logos_dir, exist_ok=True)
            timestamp = int(time.time())
            filename = f"logo_{timestamp}.png"
            filepath = os.path.join(logos_dir, filename)
            with open(filepath, "wb") as f:
               f.write(response.content)
            return {
               "success": True,
               "image_url": f"/static/generated_logos/{filename}",
               "error": None,
            }
            timestamp = int(time.time())
            filename = f"logo_{timestamp}.png"
            filepath = os.path.join("frontend/static/generated_logos", filename)
            with open(filepath, "wb") as f:
                f.write(response.content)
            return {
                "success": True,
                "image_url": f"/static/generated_logos/{filename}",
                "error": None,
            }
        else:
            return {
                "success": False,
                "image_url": None,
                "error": f"SDXL API error {response.status_code}: {response.text[:200]}",
            }
    except Exception as e:
        return {"success": False, "image_url": None, "error": str(e)}
