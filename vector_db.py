from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

qdrant_url = os.getenv("QDRANT_URI")
qdrant_api_key = os.getenv("API_KEY_QDRANT")


qdrant_collection_name = "prodcuts"
embeddings_model_name = "all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name=qdrant_collection_name,
    api_key=qdrant_api_key,
    url=qdrant_url,
)