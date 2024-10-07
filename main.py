import streamlit as st
import requests

# Dify API key and URL
dify_api_key = "app-pDKDiDrZsMJv9vS2iVd8Bg1Y"
url = "https://api.dify.ai/v1/chat-messages"

st.set_page_config(
    page_title="ABU AI | Omega Brain | Chat",
    page_icon="dorado.jpeg",
    layout="wide",
)

# Hide the Streamlit Menu and "Made with Streamlit" footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Add a custom "About" button in the sidebar
with st.sidebar:
    if st.button("About ABU AI"):
        st.sidebar.write("""
        **ABU AI** is an intelligent chatbot designed to assist you in various tasks. 
        It is capable of understanding and conversing in over 50 languages, 
        including Azerbaijani, Turkish, English, Russian, Chinese, and Spanish. 
        Powered by advanced AI models, ABU AI is here to provide quick and accurate responses.
        """)

# Initialize session state variables
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar to handle chat history and New Chat button
st.sidebar.title("Chat History")
if st.sidebar.button("New Chat"):
    st.session_state.messages = []
    st.session_state.conversation_id = ""

# Display saved chat history in the sidebar
for i, chat in enumerate(st.session_state.chat_history):
    if st.sidebar.button(f"Chat {i + 1}"):
        st.session_state.messages = chat["messages"]
        st.session_state.conversation_id = chat["conversation_id"]

# Chat UI Design
st.title("ABU AI")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(f"<div style='background-color: #E1FFC7; border-radius: 10px; padding: 10px; margin: 5px 0; color: black;'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color: #0e5099; border-radius: 10px; padding: 10px; margin: 5px 0; color: black;'>{message['content']}</div>", unsafe_allow_html=True)

# Input for user prompt
prompt = st.chat_input("Enter your question here...")

# Text below the input field
st.markdown("<p style='color: #FF0000; text-align: center;'>ABU AI can make mistakes. Don't write any sensitive information. Check important info.</p>", unsafe_allow_html=True)

if prompt:
    with st.chat_message("user"):
        st.markdown(f"<div style='background-color: #E1FFC7; border-radius: 10px; padding: 10px; margin: 5px 0; color: black;'>{prompt}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        headers = {
            'Authorization': f'Bearer {dify_api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            "inputs": {},
            "query": prompt,
            "response_mode": "blocking",
            "conversation_id": st.session_state.conversation_id,
            "user": "aianytime",
            "files": []
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            response_data = response.json()

            full_response = response_data.get('answer', '')
            new_conversation_id = response_data.get('conversation_id', st.session_state.conversation_id)
            st.session_state.conversation_id = new_conversation_id

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
            full_response = "An error occurred while fetching the response."

        message_placeholder.markdown(f"<div style='background-color: #0e5099; border-radius: 10px; padding: 10px; margin: 5px 0; color: black;'>{full_response}</div>", unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Save the conversation history
    st.session_state.chat_history.append({
        "messages": st.session_state.messages.copy(),
        "conversation_id": st.session_state.conversation_id
    })

# Set styling for button and body
st.markdown(
    """
    <style>
    body {
        background-color: white;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
