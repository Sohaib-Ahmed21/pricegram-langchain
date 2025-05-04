from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
import numpy as np

# Load environment variables from .env file
load_dotenv()

qdrant_url = os.getenv("QDRANT_URI")
qdrant_api_key = os.getenv("API_KEY_QDRANT")



qdrant_collection_name = "products"
embeddings_model_name = "all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name=qdrant_collection_name,
    api_key=qdrant_api_key,
    url=qdrant_url,
)
print(qdrant)
print(qdrant.similarity_search("iphone 15"))
print("Qdrant collection setup successful.")

from qdrant_client.http import models

def get_vector_by_id(client, collection_name, item_id):
        # Fetch the document using a filter on metadata ID
        response = client.scroll(
            collection_name=collection_name,
            scroll_filter=models.Filter(
                must=[models.FieldCondition(
                    key="metadata.id",
                    match=models.MatchValue(value=item_id)
                )]
            ),
            with_vectors=True ,
            limit=1
        )
        # Extract vector from the response
        if response and response[0]:
            return response[0][0].vector # Return the stored vector

        return None  # Return None if no vector found

def get_similar_items_to_product(client, item_id, k):
    # k : how much similar we want i.e. number of similar products
    vector = get_vector_by_id(client, "products", item_id)
    results = qdrant.similarity_search_by_vector(embedding=vector, k=k)
    rzlts=[]
    for result in results:
        rzlts.append(result.metadata["id"])
    return rzlts

def recommend_products(client, user_ratings, collection_name="products"):
    """
    Recommend products based on user-rated items using a weighted similarity approach.

    :param client: Qdrant client
    :param user_ratings: Dictionary where keys are product IDs and values are user ratings (1-5)
    :param collection_name: Name of the Qdrant collection
    :param k: Number of recommendations to return
    :return: List of recommended product IDs
    """

    # Step 1: Retrieve vectors of rated products
    weighted_vectors = []
    total_weight = 0

    for product_id, rating in user_ratings.items():
        vector = get_vector_by_id(client, collection_name, product_id)
        if vector is not None:
            weighted_vectors.append(np.array(vector) * rating)  # Weight vector by rating
            total_weight += rating

    if not weighted_vectors:  
        return []  # Return empty if no valid vectors found

    # Step 2: Compute weighted average preference vector
    user_preference_vector = np.sum(weighted_vectors, axis=0) / total_weight

    user_preference_vector = user_preference_vector.tolist() if isinstance(user_preference_vector, np.ndarray) else list(user_preference_vector)

    # Step 3: Search for similar items using the computed vector
    results = qdrant.similarity_search_by_vector(embedding=user_preference_vector,k=1500)
    rzlts=[]
    for result in results:
        rzlts.append(result.metadata["id"])
    
    return rzlts

# Classes for export

class PricegramRecommenderUtilities:
    @staticmethod
    def get_similar_items_to_product(item_id: int, k: int):
        """
        Get `k` similar items to a product of id `item_id`.
        
        This function returns items that can be suggested to a user 
        when they browse a particular product.
        """
        return get_similar_items_to_product(qdrant.client, item_id, k)
    
    @staticmethod
    def recommend_products(user_ratings: dict[int, int]):
        """
        Recommend items to user based on their ratings of the products.
        
        The function takes in a dictionary of id to rating mapping and 
        returns all products that the user might like based on these 
        ratings.
        """
        return recommend_products(qdrant.client, user_ratings)
    
    @staticmethod
    def get_search_items(query, k=50):
        """
        Search for products, returns ids of products to fetch.
        """
        results = qdrant.similarity_search(query=query,k=k)
        rzlts=[]
        for result in results:
            rzlts.append(result.metadata["id"])
        
        return rzlts

# Example usage:
user_ratings = {10: 5, 15: 3, 20: 4}  # User has rated products 10, 15, and 20
recommendations = recommend_products(qdrant.client, user_ratings)
print("Recommended Products:", recommendations[:5])