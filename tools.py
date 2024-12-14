from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools.retriever import create_retriever_tool

from vector_db import qdrant
#Making qdrant retriever
retriever = qdrant.as_retriever()

rag_tool = create_retriever_tool(
    retriever,
    "products_retriever",
    """Helps in answering queries about Ecommerce platforms, products on Ecommerce vendors especially
    laptops, mobiles, earbuds and watches.Retrieves products most similar to the features of the product in user's prompt.
    """,
)

tavily_tool = TavilySearchResults(max_results=5)
