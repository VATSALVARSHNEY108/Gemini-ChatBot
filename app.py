import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
from langchain.callbacks.base import BaseCallbackHandler
import google.generativeai as genai


# Custom callback handler for streaming responses
class StreamlitCallbackHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


# Initialize Streamlit app
st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🔥🔥 Vastal AI Chatbot 🔥🔥")
st.markdown("---")

# Sidebar for API key input
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input(
        "Enter your Gemini API Key:",
        type="password",
        help="Get your free API key from https://makersuite.google.com/app/apikey"
    )

    if st.button("Get API Key"):
        st.markdown("[Get your free Gemini API key here](https://makersuite.google.com/app/apikey)")

    st.markdown("---")

    # Model selection
    model_name = st.selectbox(
        "Select Model:",
        ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"],
        index=0,
        help="gemini-1.5-flash is fastest and free"
    )

    # Temperature setting
    temperature = st.slider(
        "Temperature:",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more random"
    )

    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.memory = ConversationBufferMemory(return_messages=True)
        st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)


# Initialize the chatbot
def initialize_chatbot(api_key, model_name, temperature):
    """Initialize the Gemini chatbot with LangChain"""
    try:
        # Configure the API key
        genai.configure(api_key=api_key)

        # Initialize the LangChain Gemini chat model
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=api_key,
            convert_system_message_to_human=True
        )

        return llm
    except Exception as e:
        st.error(f"Error initializing chatbot: {str(e)}")
        return None


# Main chat interface
if api_key:
    # Initialize chatbot
    chatbot = initialize_chatbot(api_key, model_name, temperature)

    if chatbot:
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate AI response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()

                try:
                    # Add user message to memory
                    st.session_state.memory.chat_memory.add_user_message(prompt)

                    # Get conversation history
                    history = st.session_state.memory.chat_memory.messages

                    # Create messages for the model
                    messages = []
                    for msg in history:
                        if isinstance(msg, HumanMessage):
                            messages.append(HumanMessage(content=msg.content))
                        elif isinstance(msg, AIMessage):
                            messages.append(AIMessage(content=msg.content))

                    # Add current prompt
                    messages.append(HumanMessage(content=prompt))

                    # Generate response
                    with st.spinner("Thinking..."):
                        response = chatbot.invoke(messages)
                        full_response = response.content

                    # Display response
                    message_placeholder.markdown(full_response)

                    # Add AI response to memory and chat history
                    st.session_state.memory.chat_memory.add_ai_message(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})

                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")

        # Display usage tips
        with st.expander("💡 Usage Tips"):
            st.markdown("""
            - **Get your API key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey) to get your free Gemini API key
            - **Model Selection**: 
              - `gemini-1.5-flash`: Fastest and most cost-effective
              - `gemini-1.5-pro`: More capable for complex tasks
              - `gemini-pro`: Standard model
            - **Temperature**: Controls randomness (0 = deterministic, 1 = very random)
            - **Memory**: The bot remembers your conversation history
            - **Clear Chat**: Use the sidebar button to start a new conversation
            """)

        # Display model info
        with st.expander("🔧 Current Configuration"):
            st.write(f"**Model**: {model_name}")
            st.write(f"**Temperature**: {temperature}")
            st.write(f"**Messages in conversation**: {len(st.session_state.messages)}")

else:
    st.info("👆 Please enter your Gemini API key in the sidebar to start chatting!")
    st.markdown("""
    ### How to get started:

    1. **Get your free API key**:
       - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
       - Sign in with your Google account
       - Create a new API key

    2. **Enter the API key** in the sidebar

    3. **Start chatting!**

    ### Features:
    - 💬 **Conversational Memory**: Remembers your chat history
    - 🎛️ **Configurable Models**: Choose between different Gemini models
    - 🌡️ **Temperature Control**: Adjust response creativity
    - 🧹 **Clear History**: Start fresh conversations
    - 🚀 **Free to use**: Using Google's free Gemini API
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666;">
        Built by as you know 
    </div>
    """,
    unsafe_allow_html=True
)