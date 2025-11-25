# Quick Start Guide - TalentScout Hiring Assistant

Get up and running with TalentScout in 5 minutes!

## Prerequisites

- Python 3.8+
- OpenAI API key (get one [here](https://platform.openai.com))
- A terminal or command prompt

## 1. Clone/Download Repository

```bash
cd "Talent Scout Hiring Assistant"
```

## 2. Setup (Choose One)

### Option A: Windows Users (Easiest)

Simply double-click: `setup.bat`

This will automatically:
- Create virtual environment
- Install dependencies
- Set up configuration
- Run tests
- Start the application

### Option B: macOS/Linux Users

```bash
bash setup.sh
```

### Option C: Manual Setup

```bash
# Create and activate virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 3. Configure API Key

Create a `.env` file in the project folder:

```
OPENAI_API_KEY=sk-your-key-here
DATA_SALT=your_salt_here
```

## 4. Run the Application

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at: `http://localhost:8501`

## 5. Start Using!

1. The chatbot will greet you
2. Provide your information as requested
3. Answer technical questions
4. Type "exit" when done

## Common Issues

### "API key not found"
- Make sure `.env` file exists
- Check API key is correct
- Restart the application

### "Port 8501 already in use"
- Use a different port: `streamlit run streamlit_app.py --server.port 8502`

### "Module not found"
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

## Next Steps

- Read the full [README.md](README.md)
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- See [DEPLOYMENT.md](DEPLOYMENT.md) for cloud deployment

## Need Help?

1. Check troubleshooting in README.md
2. Review test cases in tests.py
3. Check logs in the terminal

---

**Enjoy using TalentScout! 🚀**
