import pandas as pd
import asyncio
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
# from langchain.memory import ConversationBufferMemory

#imports from other files
from .chat_model import chat_model
from .tools import rag_tool, tavily_tool

# Define the system prompt
system_prompt = """
You are an expert in E-commerce, electronics, and digital products.
For any queries related to electronic, digital, or technical products
(e.g., mobiles, laptops, watches, earbuds, etc.),
always call the "products_retriever" tool to retrieve relevant information.

If the question is unrelated to products or E-commerce platforms,
use the "tavily_search_results_json" tool for general knowledge informations.
Only call "tavily_search_results_json" when absolutely necessary.

In case of any query, atleast answer something informative.
"""
# You also have a Tavily Tool which you can call for general_info when the question
# is not related to E-commerce platforms/products or both.
# Create the agent prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
tools = [rag_tool, tavily_tool]

#creating the memory
# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def create_agent():
  agent = create_tool_calling_agent(chat_model, tools, prompt)
  agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
  return agent_executor

agent = create_agent()

# def get_session_history(session_id: str):
#     return SQLChatMessageHistory(session_id, "sqlite+aiosqlite:///memory.db",async_mode=True)

# Wrap with history management
# runnable_with_history = RunnableWithMessageHistory(
#     runnable = agent,
#     get_session_history=get_session_history,  # History retrieval function
#     input_messages_key="input",  # Key for user input
#     history_messages_key="history"  # Key for chat history
# )

events = []
async def stream_agent_events(user_input):
    # Initialize list for events
    stream = agent.astream_events(
    {
        "input": user_input
        # "chat_history": chat_history
    },
    version="v1",
)

    async for event in stream:
        if event["event"] == "on_chat_model_end":
            # Never triggers in python<=3.10!
            print(event)

    # Asynchronously iterate over agent events
    # Remove callbacks argument from astream_events call
    # agent is already initialized with a callback manager, avoid setting it again

#     async for event in agent.astream_events(
#     {
#         "input": {"write 100 lines essay on forests."}
#     },
#     version="v1",
# ):
    # chat_history = memory.buffer_as_messages
    # print("History",chat_history)
#     async for event in agent.astream_events(
#     {
#         "input": user_input
#         # "chat_history": chat_history
#     },
#     version="v1",
# ):
        # Process the event based on its type
        kind = event["event"]
        # if kind == "on_chain_start":
        #     if event.get("name") == "Agent":
        #         print(
        #             f"Starting agent: {event['name']} with input: {event['data'].get('input')}"
        #         )
        # elif kind == "on_chain_end":
        #     if event.get("name") == "Agent":
        #         print("-------------------------------\n\n")
            # print(f"Done agent with output: {event['data'].get('output')}")
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                #This print statement goes through web socket send message
                yield content
        # elif kind == "on_tool_start":
        #     print("--")
            # print(f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}")
        # elif kind == "on_tool_end":
        #     print(f"Done tool: {event['name']}")
            # print(f"Tool output was: {event['data'].get('output')}")
            # print("--")
        elif kind == "on_retriever_end":
            # print(f"Done retriever: {event['name']}")
            ids = [doc.metadata["id"] for doc in event["data"]['output'].get("documents")]
            # print(f"Retriever output was: {event['data']['output'].get('documents')}")
            # print("--")
            events.append(ids)

    yield events

import asyncio

async def main():
    # First user input
    user_input1 = "My name is bob. remember it."
    print("Processing first input...")
    result1 = await stream_agent_events(user_input1)  # Await the first call
    print("\nFirst result:", result1)

    # Second user input
    user_input2 = "what's my name? kindly answer me"
    print("\nProcessing second input...")
    result2 = await stream_agent_events(user_input2)  # Await the second call
    print("\nSecond result:", result2)

print("Chatbot ready.")
# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
