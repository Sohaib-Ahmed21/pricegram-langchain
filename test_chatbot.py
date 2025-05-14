# test_app.py

import pytest
import asyncio
from chatbot import create_agent, stream_agent_events

@pytest.mark.asyncio
async def test_agent_basic_ecommerce_query():
    user_input = "Show me the latest smartwatches under $200."
    stream = stream_agent_events(user_input)
    output = []
    async for chunk in stream:
        output.append(chunk)
    assert any("smartwatch" in str(c).lower() or "$" in str(c) for c in output)

@pytest.mark.asyncio
async def test_agent_general_query_triggers_tavily():
    user_input = "Who is the current president of the United States?"
    stream = stream_agent_events(user_input)
    output = []
    async for chunk in stream:
        output.append(chunk)
    assert any("president" in str(c).lower() for c in output)

@pytest.mark.asyncio
async def test_agent_product_related_triggers_retriever():
    user_input = "Tell me about budget earbuds."
    stream = stream_agent_events(user_input)
    result = []
    async for chunk in stream:
        result.append(chunk)
    assert isinstance(result, list)
    assert any("earbuds" in str(r).lower() for r in result)

@pytest.mark.asyncio
async def test_agent_handles_empty_input():
    user_input = ""
    stream = stream_agent_events(user_input)
    result = []
    async for chunk in stream:
        result.append(chunk)
    assert any("informative" in str(r).lower() or "please provide" in str(r).lower() for r in result)

@pytest.mark.asyncio
async def test_agent_history_context_response():
    history = ["User: My name is Alice."]
    user_input = "What’s my name?"
    stream = stream_agent_events(user_input, history)
    result = []
    async for chunk in stream:
        result.append(chunk)
    assert any("alice" in str(r).lower() for r in result)
