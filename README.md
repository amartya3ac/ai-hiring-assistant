# TalentScout Hiring Assistant

## Project Overview

**TalentScout Hiring Assistant** is an intelligent AI-powered chatbot designed to automate the initial screening process for technology recruitment. Built with Streamlit and powered by OpenAI's GPT models, the assistant conducts interactive interviews with candidates, collects essential information, and generates technical questions tailored to their tech stack.

### Key Features

- **Automated Screening**: Conducts initial interviews without human intervention
- **Intelligent Information Gathering**: Collects name, email, phone, experience, desired positions, location, and tech stack
- **Dynamic Technical Questions**: Generates 4-5 technical questions based on candidate's declared technologies
- **Context-Aware Conversations**: Maintains conversation flow with intelligent context management
- **Data Privacy**: GDPR-compliant data handling with anonymization and secure storage
- **Fallback Mechanisms**: Gracefully handles unclear inputs and maintains conversation purpose
- **Clean UI**: Intuitive Streamlit interface with real-time chat display

---

## Installation Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key
- Git (for version control)

### Step 1: Clone Repository or Extract Files

```bash
# If using Git
git clone <repository-url>
cd "Talent Scout Hiring Assistant"

# Or navigate to the project folder
cd "Talent Scout Hiring Assistant"
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here
DATA_SALT=your_custom_salt_here
```

To get an OpenAI API key:
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API keys
4. Create a new secret key
5. Copy and paste it into your `.env` file

### Step 5: Run the Application

```bash
streamlit run streamlit_app.py
```

The application will open in your browser at `http://localhost:8501`

---

## Usage Guide

### Starting the Interview

1. Open the application in your browser
2. The chatbot will greet you with a welcome message
3. Follow the prompts to provide your information

### Information Collection

The interview will ask you for:

1. **Full Name**: Your complete name
2. **Email Address**: Valid email for follow-up communication
3. **Phone Number**: Contact number
4. **Years of Experience**: Your technical experience
5. **Desired Positions**: Positions you're interested in
6. **Current Location**: Your location or preferred working location
7. **Tech Stack**: Programming languages, frameworks, and tools you know

### Technical Questions

After providing your tech stack, the assistant will generate and ask 4-5 technical questions specific to your technologies. Answer each question thoroughly to demonstrate your proficiency.

### Ending the Interview

To end the interview at any time:
- Type `exit`, `quit`, `goodbye`, or `bye`
- The assistant will provide a closing message and save your information

### Resetting the Chat

Use the "Reset Chat" button in the sidebar to start a new interview session.

---

## Technical Details

### Architecture

```
├── core.py                 # Conversation manager & prompt templates
├── main.py                 # LLM integration (OpenAI API)
├── streamlit_app.py        # Streamlit UI interface
├── utils/
│   └── data_handler.py     # Data storage & GDPR compliance
├── data/
│   └── candidate_info/     # Anonymized candidate data
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### Technologies Used

- **Streamlit**: Interactive web UI framework
- **OpenAI API**: GPT-3.5-turbo language model
- **Python**: Core programming language
- **Pydantic**: Data validation
- **Cryptography**: Data security
- **Pandas**: Data processing

### Libraries & Versions

| Library | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.28.1 | Frontend interface |
| openai | 1.3.8 | LLM integration |
| pydantic | 2.5.0 | Data validation |
| cryptography | 41.0.7 | Data encryption |
| python-dotenv | 1.0.0 | Environment variables |

### Key Components

#### 1. **ConversationManager** (core.py)
- Tracks conversation state
- Manages candidate information
- Handles conversation history
- Detects exit intents

#### 2. **PromptManager** (core.py)
- Provides system prompts
- Generates information-gathering prompts
- Creates dynamic technical question prompts
- Manages fallback prompts

#### 3. **HiringAssistant** (main.py)
- Integrates with OpenAI API
- Processes user input based on conversation state
- Routes to appropriate handlers
- Generates technical questions dynamically

#### 4. **DataHandler** (utils/data_handler.py)
- Saves candidate information securely
- Anonymizes personally identifiable information (PII)
- Provides GDPR compliance features
- Maintains audit logs

---

## Prompt Design

### 1. System Prompt

The system prompt establishes the assistant's role and constraints:

```
You are TalentScout, an intelligent hiring assistant for a technology recruitment agency.
Your role is to conduct initial screening interviews with candidates.
```

**Key Design Decisions**:
- Clear role definition
- Scope limitations (hiring focus only)
- Behavior constraints (professional, focused)

### 2. Information Gathering Prompts

Each information-gathering step has a specific prompt:

- **Name Collection**: Asks for full name conversationally
- **Contact Collection**: Requests email and phone separately
- **Experience**: Asks about years in technology
- **Position Interests**: Inquires about desired roles
- **Location**: Determines geographic preference
- **Tech Stack**: Comprehensive technology proficiency inquiry

**Design Philosophy**:
- Conversational tone (not robotic)
- One piece of information at a time
- Context-aware follow-ups

### 3. Technical Question Generation

When a candidate provides their tech stack, the system generates tailored questions:

```
Generate 4-5 technical questions tailored to [Python, Django, PostgreSQL]
Requirements:
- Practical and relevant scenarios
- Mixed difficulty levels
- Technology-specific
- Clear and answerable
```

**Optimization Strategies**:
- **Temperature = 0.5**: Lower temperature for more consistent, technical questions
- **Dynamic Selection**: Questions adapt to actual tech stack provided
- **Quality Diversity**: Mix of conceptual and practical questions

### 4. Fallback Prompts

When input is unclear:

```
The user input was unclear or off-topic. Politely acknowledge and redirect.
Remind them of your purpose while being helpful.
```

---

## Challenges & Solutions

### Challenge 1: Context Maintenance

**Problem**: Losing conversation context across multiple turns.

**Solution**:
- Implemented `ConversationManager` to maintain message history
- Store last 6 messages for LLM context window optimization
- Track conversation state with explicit state machine

### Challenge 2: Tech Stack Parsing

**Problem**: Extracting and identifying technologies from free-form text.

**Solution**:
- Built `_parse_tech_stack()` function with:
  - Pre-defined list of 50+ common technologies
  - Case-insensitive matching
  - Fallback to word tokenization if no matches found

### Challenge 3: Exit Intent Detection

**Problem**: Users could get stuck in the conversation.

**Solution**:
- Implemented `is_exit_intent()` with multiple exit keywords
- Added "Exit Interview" button in sidebar
- Graceful conversation closing

### Challenge 4: Data Privacy Compliance

**Problem**: Storing sensitive candidate information safely.

**Solution**:
- **Anonymization**: Hash PII using SHA-256
- **Anonymous IDs**: Generate random IDs, not tied to names
- **Audit Logs**: Track all data access
- **Data Retention**: Auto-delete after 90 days
- **GDPR Features**: Right to be forgotten, data export

### Challenge 5: Technical Question Quality

**Problem**: Generated questions sometimes not aligned with tech stack.

**Solution**:
- Lower temperature (0.5) for consistency
- Post-processing to remove numbering
- Validation before presenting to user
- Fallback to generic question if generation fails

### Challenge 6: State Management in Streamlit

**Problem**: Streamlit reruns entire script on input, losing state.

**Solution**:
- Store all state in `st.session_state`
- Persistent chat history across reruns
- Candidate information preserved
- LLM assistant instance reused

---

## Data Privacy & Security

### GDPR Compliance Features

1. **Data Anonymization**
   - PII (email, phone, name) are hashed
   - Anonymous IDs generated independently
   - No direct mapping between candidate and data

2. **Data Retention Policy**
   - Automatic deletion after 90 days
   - Configurable retention period
   - Deletion confirmed via audit logs

3. **Right to be Forgotten**
   - `delete_candidate_info()` method removes all traces
   - Audit log entry recorded for compliance

4. **Data Portability**
   - `export_data()` method supports JSON and CSV export
   - Candidates can request their data

5. **Audit Logging**
   - All operations logged with timestamp
   - Tracks: save, retrieve, delete, errors
   - Helps with compliance audits

### Best Practices Implemented

- Environment variables for sensitive data (.env file)
- SHA-256 hashing for PII
- Separate anonymous ID generation
- Encrypted storage recommendations in comments
- No logging of sensitive information

---

## Running Locally

### Quick Start

```bash
# 1. Activate virtual environment
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

# 2. Run Streamlit app
streamlit run streamlit_app.py

# 3. Open browser to http://localhost:8501
```

### Testing the Application

1. **Test Basic Flow**:
   - Complete a full interview
   - Check sidebar for collected information
   - Verify closing message

2. **Test Exit Intent**:
   - Type "exit" or "quit"
   - Verify interview ends gracefully

3. **Test Data Storage**:
   - Check `data/candidate_info/` folder for saved JSON files
   - Verify anonymization (no real names/emails visible)

4. **Test Fallback**:
   - Enter unclear input (e.g., "xyz123")
   - Verify assistant redirects appropriately

---

## Cloud Deployment (Optional Bonus)

### AWS Deployment with Streamlit Cloud

**Prerequisites**:
- GitHub account with repo
- AWS account (optional, for backend)
- Streamlit Community Cloud account

**Steps**:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit: TalentScout Hiring Assistant"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Select this repository
   - Deploy

3. **Configure Secrets**
   - In Streamlit Cloud settings, add:
   ```
   OPENAI_API_KEY = "your-api-key"
   DATA_SALT = "your-salt"
   ```

4. **Share Live Link**
   - Streamlit Cloud provides public URL
   - Example: `https://talentscout-hiring.streamlit.app/`

### Alternative: AWS EC2 Deployment

1. Launch EC2 instance (t3.micro)
2. Install Python and dependencies
3. Clone repository
4. Run: `streamlit run streamlit_app.py --server.port 80`
5. Use Elastic IP for static URL

---

## Project Structure

```
Talent Scout Hiring Assistant/
├── core.py                      # Conversation & prompt management
├── main.py                      # LLM integration
├── streamlit_app.py             # Streamlit UI
├── requirements.txt             # Dependencies
├── .gitignore                   # Git ignore patterns
├── .env.example                 # Environment template
├── README.md                    # This file
├── utils/
│   ├── __init__.py
│   └── data_handler.py          # Data storage & privacy
├── data/
│   ├── candidate_info/          # Stored candidates
│   └── activity_log.json        # Audit log
└── prompts/                     # Prompt templates (optional)
```

---

## Version History

### Version 1.0 (Current)
- Initial release
- Core chatbot functionality
- Information gathering
- Technical question generation
- Data privacy implementation
- Streamlit UI

### Planned Features (v1.1+)
- Multi-language support
- Sentiment analysis
- Email follow-up integration
- Admin dashboard
- Resume parsing
- Video interview component

---

## Troubleshooting

### Issue: OpenAI API Key Not Found
**Solution**: Ensure `.env` file exists and contains `OPENAI_API_KEY=<your-key>`

### Issue: Streamlit App Won't Start
**Solution**: 
```bash
pip install --upgrade streamlit
streamlit run streamlit_app.py
```

### Issue: Chat History Lost on Refresh
**Solution**: This is expected behavior in Streamlit. Use "Reset Chat" to start fresh.

### Issue: Technical Questions Not Generated
**Solution**: 
- Check OpenAI API is working
- Verify API key has proper permissions
- Check API usage limits

### Issue: Data Not Saving
**Solution**:
- Ensure `data/candidate_info/` folder exists
- Check write permissions
- Verify OPENAI_API_KEY is set

---

## Contributing

To contribute improvements:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes and test
4. Commit: `git commit -m "Add your feature"`
5. Push: `git push origin feature/your-feature`
6. Create Pull Request

---

## License

This project is provided as-is for educational purposes.

---

## Support & Contact

For questions or issues:
- Check the Troubleshooting section
- Review Streamlit documentation: https://docs.streamlit.io/
- OpenAI API docs: https://platform.openai.com/docs/
- GDPR compliance: https://gdpr.eu/

---

## Acknowledgments

- Streamlit for the amazing UI framework
- OpenAI for powerful language models
- Python community for excellent libraries

---

**Last Updated**: November 2024
**Project Status**: Active Development
