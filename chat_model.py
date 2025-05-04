
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
# Load environment variables from .env file
load_dotenv()

# Fetch the API key from the environment
groq_api_key = os.getenv("GROQ_API_KEY")

chat_model_name="llama-3.1-8b-instant"
chat_model = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name=chat_model_name)