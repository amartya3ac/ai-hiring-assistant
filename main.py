"""
LLM Integration module for TalentScout Hiring Assistant.
Handles communication with Google Gemini or Ollama APIs.
"""

import os
import requests
from typing import Optional, List, Tuple
from dotenv import load_dotenv
from core import ConversationManager, PromptManager, ConversationState

# Load environment variables
load_dotenv()

# Try to import Google Generative AI
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class HiringAssistant:
    """Main class for the Hiring Assistant chatbot with LLM integration."""

    def __init__(self, provider: Optional[str] = None, model: str = "neural-chat"):
        """
        Initialize the Hiring Assistant with Gemini or Ollama.
        
        Args:
            provider: LLM provider ("gemini" or "ollama")
            model: LLM model to use
        """
        self.provider = provider or os.getenv("LLM_PROVIDER", "gemini")
        self.conversation_manager = ConversationManager()
        self.system_prompt = PromptManager.get_system_prompt()
        
        if self.provider == "gemini":
            self._init_gemini()
        elif self.provider == "ollama":
            self._init_ollama(model)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def _init_gemini(self):
        """Initialize Google Gemini API."""
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai not installed. Run: pip install google-generativeai")
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your-gemini-api-key-here":
            raise ValueError("GEMINI_API_KEY not set or invalid. Please add your API key to .env file.")
        
        genai.configure(api_key=api_key)
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.gemini_model = genai.GenerativeModel(self.model_name)

    def _init_ollama(self, model: str):
        """Initialize Ollama."""
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "neural-chat")
        
        if not self._test_ollama_connection():
            raise ValueError(f"Cannot connect to Ollama at {self.base_url}")

    def _test_ollama_connection(self) -> bool:
        """Test connection to Ollama server."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False

    def _call_llm(self, messages: List[dict], temperature: float = 0.7) -> Optional[str]:
        """
        Call the LLM API with the given messages.
        
        Args:
            messages: List of message dictionaries
            temperature: Temperature for response generation
            
        Returns:
            Generated response or None if error
        """
        if self.provider == "gemini":
            return self._call_gemini(messages, temperature)
        else:
            return self._call_ollama(messages, temperature)

    def _call_gemini(self, messages: List[dict], temperature: float = 0.7) -> Optional[str]:
        """Call Google Gemini API."""
        try:
            # Format messages for Gemini
            prompt_text = ""
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                prompt_text += f"{role}: {content}\n"
            
            response = self.gemini_model.generate_content(
                prompt_text,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=500,
                )
            )
            return response.text.strip() if response.text else None
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return None

    def _call_ollama(self, messages: List[dict], temperature: float = 0.7) -> Optional[str]:
        """Call Ollama API."""
        try:
            prompt_text = ""
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                prompt_text += f"{role}: {content}\n"
            
            prompt_text += "assistant: "
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt_text,
                    "temperature": temperature,
                    "stream": False,
                    "num_predict": 500
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                print(f"Ollama Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Ollama Error: {e}")
            return None

    def get_greeting(self) -> str:
        """Generate greeting message."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": PromptManager.get_greeting_prompt()}
        ]
        response = self._call_llm(messages, temperature=0.8)
        
        if response:
            self.conversation_manager.add_to_history("assistant", response)
            self.conversation_manager.set_state(ConversationState.NAME_COLLECTION)
            return response
        return "Welcome to TalentScout! I'm your AI hiring assistant. Could you please share your full name to get started?"

    def process_user_input(self, user_input: str) -> Tuple[str, bool]:
        """
        Process user input and generate appropriate response.
        
        Args:
            user_input: The user's message
            
        Returns:
            Tuple of (response_message, should_exit)
        """
        if self.conversation_manager.is_exit_intent(user_input):
            return self._generate_closing_message(), True

        self.conversation_manager.add_to_history("user", user_input)
        current_state = self.conversation_manager.get_current_state()

        if current_state == ConversationState.NAME_COLLECTION:
            return self._handle_name_collection(user_input)
        elif current_state == ConversationState.CONTACT_COLLECTION:
            return self._handle_contact_collection(user_input)
        elif current_state == ConversationState.EXPERIENCE_COLLECTION:
            return self._handle_experience_collection(user_input)
        elif current_state == ConversationState.POSITION_COLLECTION:
            return self._handle_position_collection(user_input)
        elif current_state == ConversationState.LOCATION_COLLECTION:
            return self._handle_location_collection(user_input)
        elif current_state == ConversationState.TECH_STACK_COLLECTION:
            return self._handle_tech_stack_collection(user_input)
        elif current_state == ConversationState.TECHNICAL_QUESTIONS:
            return self._handle_technical_questions(user_input)
        else:
            return self._handle_fallback(user_input)

    def _handle_name_collection(self, user_input: str) -> tuple[str, bool]:
        """Handle name collection state."""
        self.conversation_manager.update_candidate_info("full_name", user_input.strip())
        self.conversation_manager.set_state(ConversationState.CONTACT_COLLECTION)
        
        response = self._generate_response(
            f"Great! I've noted your name as {user_input.strip()}. "
            f"Now, could you please share your email address?"
        )
        return response, False

    def _handle_contact_collection(self, user_input: str) -> tuple[str, bool]:
        """Handle contact information collection."""
        candidate = self.conversation_manager.get_candidate_info()
        emails = self._extract_email(user_input)
        phones = self._extract_phone(user_input)
        
        if candidate.email:
            if phones:
                self.conversation_manager.update_candidate_info("phone", phones[0])
                self.conversation_manager.set_state(ConversationState.EXPERIENCE_COLLECTION)
                return self._generate_response(
                    f"Perfect! Phone saved: {phones[0]}. How many years of experience do you have?"
                ), False
            else:
                return self._generate_response(
                    "I couldn't find a valid phone number. Could you provide it in formats like: 123-456-7890 or (123) 456-7890?"
                ), False
        
        if not emails:
            return self._generate_response(
                "I couldn't find a valid email address. Could you please provide your email in the format: yourname@example.com?"
            ), False
        
        self.conversation_manager.update_candidate_info("email", emails[0])
        
        if phones:
            self.conversation_manager.update_candidate_info("phone", phones[0])
            self.conversation_manager.set_state(ConversationState.EXPERIENCE_COLLECTION)
            response = self._generate_response(
                f"Thank you! Email: {emails[0]}, Phone: {phones[0]}. How many years of experience do you have?"
            )
        else:
            response = self._generate_response(
                f"Got your email: {emails[0]}. Could you also share your phone number?"
            )
        
        return response, False

    def _handle_experience_collection(self, user_input: str) -> tuple[str, bool]:
        """Handle experience collection."""
        self.conversation_manager.update_candidate_info("years_of_experience", user_input.strip())
        self.conversation_manager.set_state(ConversationState.POSITION_COLLECTION)
        
        response = self._generate_response(
            f"Perfect! {user_input.strip()} years noted. What positions interest you?"
        )
        return response, False

    def _handle_position_collection(self, user_input: str) -> tuple[str, bool]:
        """Handle position interest collection."""
        self.conversation_manager.update_candidate_info("desired_positions", user_input.strip())
        self.conversation_manager.set_state(ConversationState.LOCATION_COLLECTION)
        
        response = self._generate_response(
            f"Great! Interested in: {user_input.strip()}. What's your preferred location?"
        )
        return response, False

    def _handle_location_collection(self, user_input: str) -> tuple[str, bool]:
        """Handle location collection."""
        self.conversation_manager.update_candidate_info("current_location", user_input.strip())
        self.conversation_manager.set_state(ConversationState.TECH_STACK_COLLECTION)
        
        response = self._generate_response(
            f"{user_input.strip()} noted. Tell me about your tech stack."
        )
        return response, False

    def _handle_tech_stack_collection(self, user_input: str) -> tuple[str, bool]:
        """Handle tech stack collection and generate technical questions."""
        tech_items = self._parse_tech_stack(user_input)
        self.conversation_manager.update_candidate_info("tech_stack", tech_items)
        
        questions = self._generate_technical_questions(tech_items)
        self.conversation_manager.set_technical_questions(questions)
        self.conversation_manager.set_state(ConversationState.TECHNICAL_QUESTIONS)
        
        if questions:
            response = (
                f"Excellent! Tech stack: {', '.join(tech_items)}.\n\n"
                f"Q1: {questions[0]}"
            )
        else:
            response = "Let me prepare some technical questions for you..."
        
        return response, False

    def _handle_technical_questions(self, user_input: str) -> tuple[str, bool]:
        """Handle technical question response."""
        current_index = self.conversation_manager.current_question_index - 1
        question_num = current_index + 1
        
        self.conversation_manager.candidate_info.technical_responses[f"question_{question_num}"] = user_input
        
        if self.conversation_manager.has_more_questions():
            next_question = self.conversation_manager.get_next_question()
            response = f"Great answer!\n\nQ{question_num + 1}: {next_question}"
            return response, False
        else:
            self.conversation_manager.set_state(ConversationState.CLOSING)
            closing_message = self._generate_closing_message()
            return closing_message, True

    def _handle_fallback(self, user_input: str) -> tuple[str, bool]:
        """Handle fallback for unclear input."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": PromptManager.get_fallback_prompt()},
            {"role": "user", "content": f"User said: {user_input}"}
        ]
        response = self._call_llm(messages)
        
        if not response:
            response = "Could you rephrase your answer? I'm here to help screen candidates."
        
        self.conversation_manager.add_to_history("assistant", response)
        return response, False

    def _generate_response(self, message: str) -> str:
        """Generate a conversational response."""
        self.conversation_manager.add_to_history("assistant", message)
        return message

    def _generate_technical_questions(self, tech_stack: List[str]) -> List[str]:
        """Generate technical questions based on tech stack."""
        if not tech_stack:
            return []
        
        prompt = PromptManager.get_tech_questions_generation_prompt(tech_stack)
        messages = [
            {"role": "system", "content": "You are an expert technical interviewer."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_llm(messages, temperature=0.5)
        if not response:
            return ["Tell me about a challenging project you've worked on."]
        
        questions = []
        for line in response.split('\n'):
            line = line.strip()
            if line and len(line) > 10:
                questions.append(line)
        
        return questions[:5]

    def _generate_closing_message(self) -> str:
        """Generate closing message."""
        candidate = self.conversation_manager.get_candidate_info()
        if candidate.full_name:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": PromptManager.get_closing_prompt(candidate.full_name)}
            ]
            response = self._call_llm(messages, temperature=0.7)
            if response:
                return response
        
        return (
            "Thank you for your time! Your information has been recorded. "
            "We'll be in touch within 2-3 business days. Have a great day!"
        )

    def _extract_email(self, text: str) -> List[str]:
        """Extract email addresses from text."""
        import re
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(pattern, text)

    def _extract_phone(self, text: str) -> List[str]:
        """Extract phone numbers from text."""
        import re
        patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            r'\b\(\d{3}\)\s?\d{3}[-.]?\d{4}\b',
            r'\b\+?1?\s?\d{10}\b'
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches
        return []

    def _parse_tech_stack(self, text: str) -> List[str]:
        """Parse tech stack from user input."""
        common_techs = [
            'Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'C#', 'Go', 'Rust', 'PHP', 'Ruby',
            'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Flask', 'FastAPI', 'Spring', 'Express',
            'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Cassandra', 'Firebase',
            'AWS', 'GCP', 'Azure', 'Docker', 'Kubernetes', 'Linux', 'Git',
            'HTML', 'CSS', 'SQL', 'GraphQL', 'REST', 'API'
        ]
        
        found_techs = []
        text_lower = text.lower()
        
        for tech in common_techs:
            if tech.lower() in text_lower:
                found_techs.append(tech)
        
        if not found_techs:
            items = [item.strip() for item in text.replace(',', ' ').replace(';', ' ').split()]
            found_techs = [item for item in items if len(item) > 2]
        
        return found_techs if found_techs else ['General Web Development']


if __name__ == "__main__":
    try:
        assistant = HiringAssistant()
        print("Hiring Assistant initialized successfully!")
    except Exception as e:
        print(f"Error: {e}")
        print("Please ensure you have configured either Gemini API key or Ollama properly")
