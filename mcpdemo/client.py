from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq


from dotenv import load_dotenv
load_dotenv()

import asyncio

import os  
os.environ["GROQ_API_KEY"]= os.getenv("GROQ_API_KEY")

async def main():
    client= MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["mcpdemo/mathserver.py"],
                "transport": "stdio"
            },
            "weather":{
                "url":"http://127.0.0.1:8000/mcp",
                "transport": "streamable_http"
            }
        }
    )
    tools = await client.get_tools()
    print([tool.name for tool in tools])
    model = ChatGroq(model="llama-3.1-8b-instant",temperature=0)
    agent = create_agent(model = model,tools = tools)
    math_response = await agent.ainvoke({
        "messages":[{"role":"user","content":"What is (3+5)x8 ?"}]
    })
    print("Math response:",math_response['messages'][-1].content)
    weather_response = await agent.ainvoke({
            "messages":[{"role":"user","content":"What is weather in india?"}]
    })
    print("weather response:",weather_response['messages'][-1].content)


asyncio.run(main())
