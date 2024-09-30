import requests
import streamlit as st 

# Dify API key and URL
dify_api_key = "app-pDKDiDrZsMJv9vS2iVd8Bg1Y"
url = "https://api.dify.ai/v1/chat-messages"

st.set_page_config(
    page_title="ABU AI | Chat",  # Change the title here
    page_icon="🤖",  # Set the robot emoji as the favicon
    layout="wide",  # You can set layout to "centered" or "wide"
)

# Streamlit app title
st.title("ABU AI")
st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Your Friendly AI Assistant</h2>", unsafe_allow_html=True)

# Initialize session state for conversation tracking
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages in the chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(f"<div style='background-color: #E1FFC7; border-radius: 10px; padding: 10px; margin: 5px 0; color: black;'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color: #D1E7FF; border-radius: 10px; padding: 10px; margin: 5px 0; color: black;'>{message['content']}</div>", unsafe_allow_html=True)

# Input for user prompt
prompt = st.chat_input("Enter your question here...")

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
            # Send request to Dify API
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            response_data = response.json()

            full_response = response_data.get('answer', '')
            new_conversation_id = response_data.get('conversation_id', st.session_state.conversation_id)
            st.session_state.conversation_id = new_conversation_id

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
            full_response = "An error occurred while fetching the response."

        # Display the assistant's response
        message_placeholder.markdown(f"<div style='background-color: #D1E7FF; border-radius: 10px; padding: 10px; margin: 5px 0; color: black;'>{full_response}</div>", unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
