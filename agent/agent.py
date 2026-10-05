"""LangChain agent that loads its tools from the local MCP server and uses a fake LLM."""

import asyncio
import sys
from pathlib import Path

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from fake_llm import FakeToolCallingChatModel

SERVER = Path(__file__).parent / "mcp_server.py"

DEFAULT_QUESTIONS = [
    "What is 2 plus 40?",
    "What's the weather in Raleigh?",
    "Say hello",
]


async def main(questions: list[str]) -> None:
    client = MultiServerMCPClient(
        {"demo-tools": {"command": sys.executable, "args": [str(SERVER)], "transport": "stdio"}}
    )
    tools = await client.get_tools()
    print("Loaded MCP tools:", [t.name for t in tools])

    agent = create_agent(FakeToolCallingChatModel(), tools)
    for question in questions:
        result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
        print(f"\nQ: {question}")
        for msg in result["messages"][1:]:
            if getattr(msg, "tool_calls", None):
                for call in msg.tool_calls:
                    print(f"  -> tool call: {call['name']}({call['args']})")
            elif msg.type == "tool":
                print(f"  <- tool result: {msg.text}")
            else:
                print(f"A: {msg.content}")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:] or DEFAULT_QUESTIONS))
