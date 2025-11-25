# Deployment Guide - TalentScout Hiring Assistant

## Deploy to Streamlit Cloud (FREE)

### Step 1: Prepare Your Repository
- ✅ Already done! Your repo is ready at: https://github.com/amartya3ac/ai-hiring-assistant

### Step 2: Deploy on Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Click **"New app"**
3. Select:
   - **Repository**: `amartya3ac/ai-hiring-assistant`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`

### Step 3: Add Secrets (IMPORTANT!)
1. In Streamlit Cloud dashboard, go to **"Manage app"** → **"Secrets"**
2. Add:
```toml
GEMINI_API_KEY = "your-actual-gemini-api-key"
LLM_PROVIDER = "gemini"
GEMINI_MODEL = "gemini-2.5-flash"
DATA_SALT = "talentscout_salt_2024"
```

3. Get your Gemini API key from: https://ai.google.dev/

### Step 4: Done!
Your app will deploy automatically and be live at:
`https://ai-hiring-assistantgit-<hash>.streamlit.app`

---

## Local Development

```bash
# Clone the repo
git clone https://github.com/amartya3ac/ai-hiring-assistant.git
cd ai-hiring-assistant

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run the app
streamlit run streamlit_app.py
```

---

## Environment Variables

| Variable | Required | Example | Notes |
|----------|----------|---------|-------|
| `LLM_PROVIDER` | Yes | `gemini` | Use "gemini" or "ollama" |
| `GEMINI_API_KEY` | Yes (if gemini) | `AIzaSy...` | Get from https://ai.google.dev/ |
| `GEMINI_MODEL` | No | `gemini-2.5-flash` | Default model |
| `DATA_SALT` | No | `talentscout_salt_2024` | For data encryption |

---

## Troubleshooting

**Error: "GEMINI_API_KEY not set"**
- Add `GEMINI_API_KEY` to Streamlit Cloud secrets (not environment variables)

**App runs locally but not on cloud?**
- Check that all files are committed to git
- Verify `.env` is in `.gitignore` (never commit secrets)

**Need Ollama support instead?**
- Set `LLM_PROVIDER=ollama` in secrets
- Ollama must be running on your local machine or accessible server

---

## Features

✅ AI-powered hiring assistant with intelligent screening  
✅ Candidate information collection (name, email, phone, experience, tech stack)  
✅ Dynamic technical questions based on candidate's skills  
✅ GDPR-compliant data storage with anonymization  
✅ Beautiful dark theme UI with animations  
✅ Free Google Gemini API integration  
✅ Fallback to local Ollama support  

---

## Support

For issues, visit: https://github.com/amartya3ac/ai-hiring-assistant/issues
