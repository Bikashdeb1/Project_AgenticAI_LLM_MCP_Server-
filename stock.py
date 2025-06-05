from mcp.server.fastmcp import FastMCP
from random import uniform

mcp = FastMCP("stock")

@mcp.tool()
def get_stock_price(symbol: str) -> str:
    """Return a fake stock price for the given symbol."""
    price = round(uniform(100, 500), 2)
    return f"The current stock price of {symbol.upper()} is ${price}"
