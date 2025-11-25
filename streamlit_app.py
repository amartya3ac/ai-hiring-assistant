"""
Streamlit UI for TalentScout Hiring Assistant.
Minimalistic design with clean interface.
"""

import streamlit as st
import os
from main import HiringAssistant
from utils.data_handler import DataHandler

# Page configuration
st.set_page_config(
    page_title="TalentScout",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Minimalistic CSS with Tailwind-inspired design and animations
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #1a1f35 100%);
        color: #e2e8f0;
    }
    
    .main {
        padding: 2rem 1rem;
        max-width: 700px;
        margin: 0 auto;
    }
    
    /* Header Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem 1.5rem;
        background: linear-gradient(135deg, rgba(30, 41, 82, 0.8), rgba(15, 23, 42, 0.8));
        border-radius: 1rem;
        border: 1px solid rgba(148, 163, 184, 0.1);
        backdrop-filter: blur(10px);
        animation: fadeInDown 0.6s ease-out;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    .header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: slideInUp 0.7s ease-out;
    }
    
    .header p {
        margin: 0.75rem 0 0 0;
        font-size: 1rem;
        color: #94a3b8;
        animation: slideInUp 0.8s ease-out;
    }
    
    /* Chat Container */
    .chat-container {
        min-height: 350px;
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: rgba(15, 23, 42, 0.6);
        border-radius: 1rem;
        border: 1px solid rgba(148, 163, 184, 0.1);
        backdrop-filter: blur(10px);
        animation: fadeIn 0.8s ease-out;
        overflow-y: auto;
        max-height: 500px;
    }
    
    /* Chat Messages */
    .stChatMessage {
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0.75rem;
        animation: slideInUp 0.4s ease-out;
        transition: all 0.3s ease;
    }
    
    .stChatMessage[data-testid="stChatMessageContent"] {
        color: #e2e8f0;
    }
    
    /* User Message */
    [data-testid="chatAvatarIcon-user"] ~ * {
        background: linear-gradient(135deg, rgba(96, 165, 250, 0.15), rgba(59, 130, 246, 0.1));
        border: 1px solid rgba(96, 165, 250, 0.3);
        margin-left: auto;
        max-width: 80%;
    }
    
    /* Assistant Message */
    [data-testid="chatAvatarIcon-assistant"] ~ * {
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.15), rgba(16, 185, 129, 0.1));
        border: 1px solid rgba(52, 211, 153, 0.3);
        margin-right: auto;
        max-width: 80%;
    }
    
    /* Chat Input */
    .stChatInputContainer {
        border-top: 1px solid rgba(148, 163, 184, 0.1);
        padding-top: 1.5rem;
        margin-top: 1.5rem;
        animation: slideInUp 0.6s ease-out;
    }
    
    input[type="text"] {
        background: linear-gradient(135deg, rgba(30, 41, 82, 0.9), rgba(15, 23, 42, 0.9));
        border: 2px solid rgba(96, 165, 250, 0.3);
        border-radius: 0.75rem;
        padding: 0.875rem 1rem;
        font-size: 0.95rem;
        color: #e2e8f0;
        transition: all 0.3s ease;
    }
    
    input[type="text"]:focus {
        border-color: rgba(96, 165, 250, 0.8);
        box-shadow: 0 0 20px rgba(96, 165, 250, 0.2);
        outline: none;
    }
    
    input[type="text"]::placeholder {
        color: #64748b;
    }
    
    /* End Message */
    .end-message {
        text-align: center;
        padding: 2rem 1.5rem;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(52, 211, 153, 0.1));
        border: 1px solid rgba(52, 211, 153, 0.3);
        border-radius: 1rem;
        color: #86efac;
        font-size: 1rem;
        animation: slideInUp 0.6s ease-out;
        backdrop-filter: blur(10px);
    }
    
    .end-message p {
        margin: 0.5rem 0;
    }
    
    .end-message p:first-child {
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(148, 163, 184, 0.1);
        color: #64748b;
        font-size: 0.85rem;
        animation: fadeIn 1s ease-out;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(148, 163, 184, 0.2), transparent);
        margin: 1.5rem 0;
    }
    
    /* Loading Animation */
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    .loading {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(96, 165, 250, 0.4);
        border-radius: 10px;
        transition: background 0.3s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(96, 165, 250, 0.6);
    }
    
    /* Button Styling */
    button {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        border: none;
        border-radius: 0.75rem;
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
    }
    
    button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }
    
    button:active {
        transform: translateY(0);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "assistant" not in st.session_state:
    try:
        st.session_state.assistant = HiringAssistant()
        st.session_state.conversation_started = False
        st.session_state.chat_history = []
        st.session_state.should_exit = False
        st.session_state.data_handler = DataHandler()
    except ValueError as e:
        st.error(f"❌ {str(e)}")
        st.info("Make sure Ollama is running at http://localhost:11434")
        st.stop()


def display_chat_history():
    """Display chat history in the UI."""
    for i, message_dict in enumerate(st.session_state.chat_history):
        if message_dict["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.write(message_dict["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(message_dict["content"])


def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown("""
        <div class="header">
            <h1>💼 TalentScout</h1>
            <p>AI-Powered Hiring Assistant</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get initial greeting if conversation hasn't started
    if not st.session_state.conversation_started:
        greeting = st.session_state.assistant.get_greeting()
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": greeting
        })
        st.session_state.conversation_started = True
    
    # Display chat history
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    display_chat_history()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Check if conversation should end
    if st.session_state.should_exit:
        st.markdown("""
            <div class="end-message">
                <p>✨ Interview Complete</p>
                <p>Thank you for your time!</p>
                <p style="font-size: 0.85rem; color: #64748b; margin-top: 0.75rem;">Your information has been saved and will be reviewed.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="footer">
                TalentScout © 2024 • AI-Powered Recruitment
            </div>
        """, unsafe_allow_html=True)
        return
    
    # Chat input
    user_input = st.chat_input(
        "Type your response...",
        key="chat_input"
    )
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Process input with assistant
        response, should_exit = st.session_state.assistant.process_user_input(user_input)
        
        # Add assistant response to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })
        
        # Save candidate info if conversation is ending
        if should_exit:
            candidate_info = st.session_state.assistant.conversation_manager.get_candidate_info()
            st.session_state.data_handler.save_candidate_info(candidate_info)
            st.session_state.should_exit = True
        
        # Rerun to update the UI
        st.rerun()
    
    st.markdown("""
        <div class="footer">
            TalentScout © 2024 • AI-Powered Recruitment
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
