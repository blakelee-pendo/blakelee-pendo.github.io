"""A fake chat model that plays the part of an LLM without calling any API.

On the first turn it picks a tool based on simple keyword matching and emits a
tool call. Once a tool result comes back, it returns a final answer built from
that result.
"""

import re
import uuid
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult


class FakeToolCallingChatModel(BaseChatModel):
    @property
    def _llm_type(self) -> str:
        return "fake-tool-calling"

    def bind_tools(self, tools: Any, **kwargs: Any) -> "FakeToolCallingChatModel":
        return self

    def _generate(self, messages: list[BaseMessage], stop=None, run_manager=None, **kwargs) -> ChatResult:
        last = messages[-1]
        if isinstance(last, ToolMessage):
            reply = AIMessage(content=f"The answer is: {last.text}")
        else:
            question = next(m for m in reversed(messages) if isinstance(m, HumanMessage)).content
            reply = self._pick_tool_call(question)
        return ChatResult(generations=[ChatGeneration(message=reply)])

    def _pick_tool_call(self, question: str) -> AIMessage:
        numbers = re.findall(r"-?\d+(?:\.\d+)?", question)
        if "weather" in question.lower():
            city = question.rstrip("?.!").split()[-1]
            name, args = "get_weather", {"city": city}
        elif len(numbers) >= 2:
            name, args = "add", {"a": float(numbers[0]), "b": float(numbers[1])}
        else:
            name, args = "echo", {"text": question}
        return AIMessage(
            content="",
            tool_calls=[{"name": name, "args": args, "id": f"call_{uuid.uuid4().hex[:8]}", "type": "tool_call"}],
        )
