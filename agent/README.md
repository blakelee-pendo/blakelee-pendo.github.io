# Fake LangChain agent + MCP server

A minimal LangChain agent that loads its tools from a local MCP server. The LLM
is faked (`fake_llm.py`), so no API key is needed.

- `mcp_server.py` — MCP server (stdio) with `add`, `get_weather` (canned), and `echo` tools
- `fake_llm.py` — fake chat model that emits a tool call, then answers from the tool result
- `agent.py` — connects to the MCP server via `langchain-mcp-adapters` and runs the agent

## Run

```bash
cd agent
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python agent.py                         # runs the default questions
.venv/bin/python agent.py "What is 3 plus 4?"     # or ask your own
```
