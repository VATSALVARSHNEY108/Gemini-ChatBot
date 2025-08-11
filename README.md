#🔥 Vatsal AI Chatbot 🔥
A conversational AI chatbot powered by Google Gemini API and LangChain, built with Streamlit.
It supports conversational memory, model selection, temperature control, and easy API key configuration.

🚀 Features
💬 Conversational Memory – remembers your chat history during the session.

🎛️ Configurable Models – choose from gemini-1.5-flash, gemini-1.5-pro, and gemini-pro.

🌡️ Temperature Control – adjust creativity and randomness of responses.

🧹 Clear History – reset conversation anytime.

🔑 Easy API Key Input – no need to hardcode your key, enter it via the sidebar.

⚡ Free to use – uses Google’s free Gemini API.

📦 Installation
Clone this repository

bash
Copy
Edit
git clone https://github.com/yourusername/vatsal-ai-chatbot.git
cd vatsal-ai-chatbot
Create a virtual environment (optional but recommended)

bash
Copy
Edit
python -m venv .venv
source .venv/bin/activate    # Mac/Linux
.venv\Scripts\activate       # Windows
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
🔑 Get Your Gemini API Key
Visit Google AI Studio

Sign in with your Google account.

Create a new API key.

▶️ Run the App
bash
Copy
Edit
streamlit run app.py
⚙️ How to Use
Enter your Gemini API key in the sidebar.

Select your model (gemini-1.5-flash recommended for speed).

Adjust temperature (creativity level).

Start chatting!

🛠️ Tech Stack
Python

Streamlit – UI framework

LangChain – conversation handling

Google Gemini API – AI model

ConversationBufferMemory – session-based memory

📂 Project Structure
bash
Copy
Edit
📦 vatsal-ai-chatbot
 ┣ 📜 app.py                # Main Streamlit application
 ┣ 📜 requirements.txt      # Python dependencies
 ┣ 📜 README.md             # Documentation
 ┗ 📂 .venv                  # Virtual environment (optional)
💡 Tips
gemini-1.5-flash – fastest & most cost-effective

gemini-1.5-pro – better for reasoning tasks

gemini-pro – standard balanced model

Temperature 0.0 → more deterministic, 1.0 → more creative
