"""
Configuration module for TalentScout Hiring Assistant.
Manages application settings and constants.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""
    
    # LLM Configuration - Support both Ollama and Google Gemini
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # "gemini" or "ollama"
    
    # Google Gemini Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    # Ollama Configuration
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "neural-chat")
    
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-flash")
    
    # Data Configuration
    DATA_DIR = os.getenv("DATA_DIR", "data/candidate_info")
    DATA_SALT = os.getenv("DATA_SALT", "salt_2024_talentscout")
    DATA_RETENTION_DAYS = int(os.getenv("DATA_RETENTION_DAYS", "90"))
    
    # Conversation Configuration
    MAX_CONVERSATION_HISTORY = 10
    EXIT_KEYWORDS = ['exit', 'quit', 'goodbye', 'bye', 'leave', 'end', 'stop']
    
    # Technical Questions Configuration
    MIN_QUESTIONS = 3
    MAX_QUESTIONS = 5
    QUESTION_TEMPERATURE = 0.5
    
    # LLM Configuration
    LLM_TEMPERATURE = 0.7
    LLM_MAX_TOKENS = 500
    
    # UI Configuration
    PAGE_TITLE = "TalentScout Hiring Assistant"
    PAGE_ICON = "🤖"
    PAGE_LAYOUT = "centered"
    
    # Common Technologies List
    COMMON_TECHNOLOGIES = [
        # Programming Languages
        'Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'C#', 'Go', 'Rust', 'PHP', 'Ruby',
        'Kotlin', 'Swift', 'Scala', 'Perl', 'R', 'MATLAB', 'Dart', 'Objective-C',
        
        # Frontend Frameworks
        'React', 'Vue', 'Angular', 'Svelte', 'Next.js', 'Nuxt', 'jQuery',
        
        # Backend Frameworks
        'Django', 'Flask', 'FastAPI', 'Spring', 'Express', 'NestJS', 'Laravel', 'ASP.NET', 'Rails',
        
        # Databases
        'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Cassandra', 'Firebase', 'DynamoDB',
        'Oracle', 'SQL Server', 'MariaDB', 'Elasticsearch',
        
        # Cloud & DevOps
        'AWS', 'GCP', 'Azure', 'Docker', 'Kubernetes', 'Linux', 'Git', 'Jenkins', 'GitLab CI',
        
        # Web Technologies
        'HTML', 'CSS', 'SCSS', 'SQL', 'GraphQL', 'REST', 'API', 'WebSocket',
        
        # Data & ML
        'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy', 'Keras',
        
        # Other Tools
        'Git', 'Docker', 'Kubernetes', 'Jenkins', 'Apache', 'Nginx', 'RabbitMQ', 'Kafka'
    ]
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate critical configuration.
        
        Returns:
            True if configuration is valid
        """
        if cls.LLM_PROVIDER == "gemini":
            if not cls.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY not set in environment variables")
        elif cls.LLM_PROVIDER == "ollama":
            if not cls.OLLAMA_BASE_URL:
                raise ValueError("OLLAMA_BASE_URL not set in environment variables")
        return True


# Application constants
class Constants:
    """Application constants."""
    
    COMPANY_NAME = "TalentScout"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "Intelligent AI-powered hiring assistant for technology recruitment"
    
    # Interview flow messages
    WELCOME_MESSAGE = "Welcome to TalentScout! I'm your AI hiring assistant."
    
    # Error messages
    ERROR_NO_API_KEY = "API key not configured. Please set GEMINI_API_KEY or OLLAMA_BASE_URL in environment."
    ERROR_API_CONNECTION = "Unable to connect to LLM API. Please check your configuration."
    ERROR_DATA_SAVE = "Error saving candidate information. Please try again."
    
    # Success messages
    SUCCESS_DATA_SAVED = "Your information has been saved successfully."
    SUCCESS_INTERVIEW_COMPLETE = "Thank you for completing the interview!"
    
    # Validation messages
    VALIDATION_EMAIL_FORMAT = "Please provide a valid email address (e.g., email@example.com)"
    VALIDATION_PHONE_FORMAT = "Please provide a valid phone number"


# Logging configuration
class LogConfig:
    """Logging configuration."""
    
    LOG_DIR = "logs"
    LOG_FILE = os.path.join(LOG_DIR, "app.log")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Log format
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


# Feature flags
class FeatureFlags:
    """Feature flags for experimental features."""
    
    ENABLE_SENTIMENT_ANALYSIS = os.getenv("ENABLE_SENTIMENT_ANALYSIS", "false").lower() == "true"
    ENABLE_MULTILINGUAL = os.getenv("ENABLE_MULTILINGUAL", "false").lower() == "true"
    ENABLE_RESUME_PARSING = os.getenv("ENABLE_RESUME_PARSING", "false").lower() == "true"
    ENABLE_VIDEO_INTERVIEW = os.getenv("ENABLE_VIDEO_INTERVIEW", "false").lower() == "true"
    ENABLE_EMAIL_NOTIFICATIONS = os.getenv("ENABLE_EMAIL_NOTIFICATIONS", "false").lower() == "true"


if __name__ == "__main__":
    print("TalentScout Configuration")
    print(f"Model: {Config.LLM_MODEL}")
    print(f"Data Directory: {Config.DATA_DIR}")
    print(f"Data Retention: {Config.DATA_RETENTION_DAYS} days")
    print(f"API Key Set: {'Yes' if Config.OPENAI_API_KEY else 'No'}")
