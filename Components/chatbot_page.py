import streamlit as st
from .model import get_response

def show_chatbot_page(knowledge_model):
    st.title('Data Chat Bot')
    col1, col2 = st.columns([0.9, 0.2])
    with col1:
        st.write("Welcome to the KnowledgeSystem! Ask me anything:")

    # Container for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Key for text input to reset it after every response
    if "input_key" not in st.session_state:
        st.session_state.input_key = 0

    chat_history_container = st.container()

    # Display messages
    for message in st.session_state.messages:
        with chat_history_container:
            role, text = message
            if role == "User":
                st.text(f"User: {text}")
            else:
                st.text(text)  # Display the bot's text without the "Bot" label

    # Chat input at the bottom
    user_input = st.chat_input("Type your question here...")
    # user_input = st.text_input("Type your question here...", key=f"chat_input_{st.session_state.input_key}")

    # Submit on enter and handle the response
    if user_input:
        if st.session_state.get("last_input") != user_input:  # Ensure we do not process the same input repeatedly
            with st.spinner('Generating response...'):
                answer = get_response(user_input, knowledge_model)
                st.session_state.messages.append(("User", user_input))
                st.session_state.messages.append(("Bot", answer))
                st.session_state["last_input"] = user_input  # Update the last input
                st.session_state.input_key += 1  # Increment the key to reset the input field
            st.experimental_rerun()

    # Positioning clear history button
    with col2:
        if st.button("Clear History", key='clear_history'):
        # Clear the message history and last input
            st.session_state.messages = []
            if "last_input" in st.session_state:
                del st.session_state["last_input"]
            st.session_state.input_key = 0  # Reset input key to start fresh
            # Use rerun to refresh the page and display the cleared history
            st.experimental_rerun()
