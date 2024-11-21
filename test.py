import openai
import streamlit as st
from openai import OpenAI

# Set up the Streamlit page
st.title("🤖 Job Bot - AI Assistant")

# Set OpenAI API Key (retrieve from Streamlit secrets)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize session states
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"  # Default OpenAI model

if "messages" not in st.session_state:
    # Store the chat messages (user + assistant)
    st.session_state["messages"] = []

# Initialize the OpenAI client
client = OpenAI(api_key=openai.api_key)

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input box for user prompt
if prompt := st.chat_input("Ask me anything about your Job Description!"):
    # Append user input to session messages
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot's response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()  # Placeholder for streaming
        full_response = ""

        # Use the user's input as the content for the conversation
        content = prompt  # User's input as content

        # Call OpenAI API using client.chat.completions.create (corrected method)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": content,  # Send the actual user input here
                }
            ],
            # Use the current model from session state
            model=st.session_state["openai_model"],
        )

        # Corrected response access:
        # The correct way to access the content in the response object is:
        full_response = chat_completion.choices[0].message.content

        # Streaming the response to the user
        message_placeholder.markdown(full_response)

    # Append assistant's response to session messages
    st.session_state["messages"].append(
        {"role": "assistant", "content": full_response})
