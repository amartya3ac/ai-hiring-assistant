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

# Minimalistic CSS
st.markdown("""
    <style>
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    body {
        background-color: #ffffff;
        color: #1a1a1a;
    }
    .main {
        padding: 1.5rem 1rem;
        max-width: 600px;
        margin: 0 auto;
    }
    .stChatMessage {
        padding: 0.75rem;
        margin-bottom: 0.75rem;
        border-radius: 0.5rem;
        background-color: transparent;
    }
    .stChatMessage[data-testid="stChatMessageContent"] {
        color: #1a1a1a;
    }
    .header {
        text-align: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #e0e0e0;
    }
    .header h1 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 600;
        color: #1a1a1a;
    }
    .header p {
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
        color: #666;
    }
    .chat-container {
        min-height: 300px;
        margin-bottom: 1.5rem;
    }
    .stChatInputContainer {
        border-top: 1px solid #e0e0e0;
        padding-top: 1rem;
    }
    input[type="text"] {
        background-color: #f5f5f5;
        border: 1px solid #e0e0e0;
        border-radius: 0.5rem;
        padding: 0.75rem;
        font-size: 0.95rem;
    }
    .end-message {
        text-align: center;
        padding: 2rem 1rem;
        color: #666;
        font-size: 0.9rem;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #e0e0e0;
        color: #999;
        font-size: 0.8rem;
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
                <p>✓ Interview complete. Thank you for your time!</p>
                <p style="font-size: 0.85rem; color: #999;">Your information has been saved.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="footer">
                TalentScout © 2024
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
            TalentScout © 2024
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
