import pytest
import vector_db as PricegramRecommenderUtilities

@pytest.mark.asyncio
async def test_get_similar_items_to_product_valid():
    """
    Tests if similar items are returned for a valid item ID.
    """
    item_id = 10  # should exist in your Qdrant collection
    k = 3
    similar_items = PricegramRecommenderUtilities.get_similar_items_to_product(item_id, k)
    assert isinstance(similar_items, list)
    assert len(similar_items) <= k
    assert all(isinstance(i, str) or isinstance(i, int) for i in similar_items)

@pytest.mark.asyncio
async def test_get_similar_items_to_product_invalid():
    """
    Tests that an invalid ID returns an empty list (or no exception).
    """
    item_id = -9999  # ID unlikely to exist
    k = 5
    similar_items = PricegramRecommenderUtilities.get_similar_items_to_product(item_id, k)
    assert isinstance(similar_items, list)

@pytest.mark.asyncio
async def test_recommend_products_valid_ratings():
    """
    Tests if recommendations are returned for a user with valid ratings.
    """
    user_ratings = {10: 5, 15: 4, 20: 3}
    recommendations = PricegramRecommenderUtilities.recommend_products(user_ratings)
    assert isinstance(recommendations, list)
    assert all(isinstance(i, str) or isinstance(i, int) for i in recommendations)

@pytest.mark.asyncio
async def test_recommend_products_empty_ratings():
    """
    Tests that empty ratings return an empty list.
    """
    user_ratings = {}
    recommendations = PricegramRecommenderUtilities.recommend_products(user_ratings)
    assert isinstance(recommendations, list)
    assert len(recommendations) == 0

@pytest.mark.asyncio
async def test_recommend_products_invalid_ids():
    """
    Tests behavior when product IDs are invalid/non-existent.
    """
    user_ratings = {999999: 5, 888888: 4}
    recommendations = PricegramRecommenderUtilities.recommend_products(user_ratings)
    assert isinstance(recommendations, list)

@pytest.mark.asyncio
async def test_get_search_items_valid_query():
    """
    Tests if search returns results for a common product keyword.
    """
    query = "smartphone"
    results = PricegramRecommenderUtilities.get_search_items(query, k=5)
    assert isinstance(results, list)
    assert len(results) <= 5
    assert all(isinstance(i, str) or isinstance(i, int) for i in results)

@pytest.mark.asyncio
async def test_get_search_items_nonsense_query():
    """
    Tests that a garbage query returns an empty or small result set.
    """
    query = "asdfghjklqwerty"
    results = PricegramRecommenderUtilities.get_search_items(query, k=5)
    assert isinstance(results, list)
    assert len(results) <= 5
