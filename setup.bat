@echo off
echo.
echo ╔══════════════════════════════════════╗
echo ║   ⚡ BizForge Setup Script (Windows)  ║
echo ╚══════════════════════════════════════╝
echo.

cd backend

echo 📦 Creating virtual environment...
python -m venv venv

echo ✅ Activating...
call venv\Scripts\activate

echo 📥 Installing dependencies...
pip install -r requirements.txt

echo.
echo ╔══════════════════════════════════════╗
echo ║  ⚙️  IMPORTANT: Configure .env        ║
echo ╚══════════════════════════════════════╝
echo Edit backend\.env and add your API keys:
echo   GROQ_API_KEY=your_groq_key
echo   HF_API_KEY=your_huggingface_key
echo.
echo Then run: venv\Scripts\activate ^&^& python main.py
echo.
pause
