"""
Core chatbot logic and conversation management for TalentScout Hiring Assistant.
Handles context management, prompt engineering, and LLM interactions.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import json


class ConversationState(Enum):
    """Enum for different conversation states."""
    GREETING = "greeting"
    NAME_COLLECTION = "name_collection"
    CONTACT_COLLECTION = "contact_collection"
    EXPERIENCE_COLLECTION = "experience_collection"
    POSITION_COLLECTION = "position_collection"
    LOCATION_COLLECTION = "location_collection"
    TECH_STACK_COLLECTION = "tech_stack_collection"
    TECHNICAL_QUESTIONS = "technical_questions"
    CLOSING = "closing"
    ENDED = "ended"


@dataclass
class CandidateInfo:
    """Data class to store candidate information."""
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    years_of_experience: Optional[str] = None
    desired_positions: Optional[str] = None
    current_location: Optional[str] = None
    tech_stack: Optional[List[str]] = field(default_factory=list)
    technical_responses: Dict[str, str] = field(default_factory=dict)

    def to_dict(self):
        """Convert candidate info to dictionary."""
        return {
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "years_of_experience": self.years_of_experience,
            "desired_positions": self.desired_positions,
            "current_location": self.current_location,
            "tech_stack": self.tech_stack,
            "technical_responses": self.technical_responses
        }


class ConversationManager:
    """Manages the conversation flow and context for the hiring assistant."""

    # Exit keywords that end the conversation
    EXIT_KEYWORDS = ['exit', 'quit', 'goodbye', 'bye', 'leave', 'end', 'stop']

    def __init__(self):
        """Initialize conversation manager."""
        self.state: ConversationState = ConversationState.GREETING
        self.candidate_info = CandidateInfo()
        self.conversation_history: List[Dict[str, str]] = []
        self.current_question_index = 0
        self.generated_questions: List[str] = []

    def is_exit_intent(self, user_input: str) -> bool:
        """Check if user input contains exit keywords."""
        user_lower = user_input.lower().strip()
        return any(keyword in user_lower for keyword in self.EXIT_KEYWORDS)

    def add_to_history(self, role: str, content: str):
        """Add message to conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content
        })

    def get_conversation_context(self) -> str:
        """Get formatted conversation context for LLM."""
        context = "Conversation History:\n"
        for msg in self.conversation_history[-6:]:  # Last 6 messages for context
            context += f"{msg['role'].upper()}: {msg['content']}\n"
        return context

    def set_state(self, new_state: ConversationState):
        """Transition to a new conversation state."""
        self.state = new_state

    def get_current_state(self) -> ConversationState:
        """Get current conversation state."""
        return self.state

    def update_candidate_info(self, field: str, value):
        """Update candidate information."""
        if hasattr(self.candidate_info, field):
            setattr(self.candidate_info, field, value)

    def get_candidate_info(self) -> CandidateInfo:
        """Get current candidate information."""
        return self.candidate_info

    def set_technical_questions(self, questions: List[str]):
        """Set generated technical questions."""
        self.generated_questions = questions
        self.current_question_index = 0

    def get_next_question(self) -> Optional[str]:
        """Get next technical question."""
        if self.current_question_index < len(self.generated_questions):
            question = self.generated_questions[self.current_question_index]
            self.current_question_index += 1
            return question
        return None

    def has_more_questions(self) -> bool:
        """Check if there are more questions to ask."""
        return self.current_question_index < len(self.generated_questions)

    def is_info_complete(self) -> bool:
        """Check if all required candidate info is collected."""
        return all([
            self.candidate_info.full_name,
            self.candidate_info.email,
            self.candidate_info.phone,
            self.candidate_info.years_of_experience,
            self.candidate_info.desired_positions,
            self.candidate_info.current_location,
            self.candidate_info.tech_stack
        ])


class PromptManager:
    """Manages all prompts for the chatbot."""

    @staticmethod
    def get_system_prompt() -> str:
        """Get the system prompt for the chatbot."""
        return """You are TalentScout, an intelligent hiring assistant for a technology recruitment agency. 
Your role is to conduct initial screening interviews with candidates for technology positions.

RESPONSIBILITIES:
1. Greet candidates warmly and explain your purpose
2. Collect essential information (name, email, phone, experience, desired positions, location)
3. Ask about their tech stack in a conversational manner
4. Generate and ask technical questions based on their tech stack
5. Provide meaningful feedback and next steps
6. Exit gracefully when requested

CONSTRAINTS:
- Stay focused on hiring-related topics only
- Do not deviate from your purpose of screening candidates
- Maintain a professional and friendly tone
- Keep responses concise and clear
- If you don't understand something, ask for clarification

When collecting information, do so conversationally - don't list all questions at once."""

    @staticmethod
    def get_greeting_prompt() -> str:
        """Get the greeting prompt."""
        return """Welcome the candidate to TalentScout's Hiring Assistant. 
Briefly explain that you're an AI assistant here to help conduct their initial screening interview.
Ask them for their full name to start the process.
Keep it warm, professional, and encouraging."""

    @staticmethod
    def get_info_gathering_prompt(field: str, candidate_name: str = "") -> str:
        """Get prompts for gathering specific candidate information."""
        prompts = {
            "name": f"Ask the candidate for their full name if you don't have it yet.",
            "email": f"Ask {candidate_name} for their email address. Mention it will be used for follow-up communication.",
            "phone": f"Ask {candidate_name} for their phone number where they can be reached.",
            "experience": f"Ask {candidate_name} how many years of experience they have in software development/technology.",
            "position": f"Ask {candidate_name} what position(s) they're interested in at our recruitment agency.",
            "location": f"Ask {candidate_name} their current location or preferred working location.",
            "tech_stack": f"Ask {candidate_name} about their technical skills and tech stack. Include: programming languages, frameworks, databases, and tools they're proficient with. Ask them to list several technologies."
        }
        return prompts.get(field, "")

    @staticmethod
    def get_tech_questions_generation_prompt(tech_stack: List[str]) -> str:
        """Get prompt to generate technical questions."""
        tech_list = ", ".join(tech_stack)
        return f"""Generate 4-5 technical questions tailored to assess a candidate's proficiency in the following technologies: {tech_list}

Requirements:
- Questions should be practical and relevant to real-world scenarios
- Mix difficulty levels (some intermediate, some advanced)
- Ensure questions are specific to the technologies listed
- Each question should be clear and answerable
- Format: Number each question (1., 2., etc.)
- Return ONLY the questions, no additional text

Example format:
1. [Question about tech 1]
2. [Question about tech 2]
etc."""

    @staticmethod
    def get_fallback_prompt() -> str:
        """Get fallback prompt when chatbot doesn't understand."""
        return """The user input was unclear or off-topic. Politely acknowledge this and:
1. Apologize for not understanding
2. Briefly remind them of what you're here to help with (hiring screening)
3. Ask them to rephrase or redirect them back to the screening process
Keep it concise and helpful."""

    @staticmethod
    def get_closing_prompt(candidate_name: str) -> str:
        """Get closing prompt."""
        return f"""Thank {candidate_name} for their time in this screening interview.
Summarize what you've learned about them (key tech stack, experience level).
Inform them about next steps: mention that their information will be reviewed and they'll be contacted within 2-3 business days if there's a suitable match.
Keep it professional, warm, and encouraging."""


# Example usage and testing
if __name__ == "__main__":
    manager = ConversationManager()
    print(f"Initial state: {manager.get_current_state()}")
    print(f"Greeting prompt: {PromptManager.get_greeting_prompt()}")
