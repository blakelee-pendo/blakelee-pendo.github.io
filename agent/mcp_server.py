"""A tiny MCP server exposing a few toy tools over stdio."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("demo-tools")

FAKE_WEATHER = {
    "raleigh": "72°F and sunny",
    "london": "55°F and drizzling",
    "tokyo": "68°F and clear",
}


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@mcp.tool()
def get_weather(city: str) -> str:
    """Get the (canned) current weather for a city."""
    return FAKE_WEATHER.get(city.lower(), f"No weather data for {city}")


@mcp.tool()
def echo(text: str) -> str:
    """Echo the input text back."""
    return text


if __name__ == "__main__":
    mcp.run(transport="stdio")
