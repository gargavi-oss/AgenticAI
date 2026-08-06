from fastmcp import FastMCP
mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(loc: str)->str:
    """Get the weather of the location"""
    return "It is always rainny in California"


if __name__=="__main__":
    mcp.run(transport="streamable-http")