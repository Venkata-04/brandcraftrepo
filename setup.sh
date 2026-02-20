#!/bin/bash
# ─── BizForge Setup & Run Script (Linux / Mac) ───────────────────────────────

echo ""
echo "╔══════════════════════════════════════╗"
echo "║   ⚡ BizForge Setup Script            ║"
echo "╚══════════════════════════════════════╝"
echo ""

# Navigate to backend
cd backend

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate
source venv/bin/activate
echo "✅ Virtual environment activated"

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "╔══════════════════════════════════════╗"
echo "║  ⚙️  IMPORTANT: Configure your .env   ║"
echo "╚══════════════════════════════════════╝"
echo "Edit backend/.env and add:"
echo "  GROQ_API_KEY=your_groq_key"
echo "  HF_API_KEY=your_huggingface_key"
echo ""
echo "Then run:  source venv/bin/activate && python main.py"
echo ""
