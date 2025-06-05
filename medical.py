# server/medical.py

from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("medical")

OPENFDA_ENDPOINT = "https://api.fda.gov/drug/label.json"

@mcp.tool()
async def get_drug_info(drug_name: str) -> str:
    """
    Get basic drug information from the OpenFDA API.

    Args:
        drug_name: The name of the drug (e.g., ibuprofen'')
    """
    params = {"search": f"openfda.generic_name:{drug_name}", "limit": 1}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(OPENFDA_ENDPOINT, params=params, timeout=15.0)
            response.raise_for_status()
            results = response.json()["results"][0]
            brand_name = results["openfda"].get("brand_name", ["Unknown"])[0]
            purpose = results.get("purpose", ["No purpose info available"])[0]
            warnings = results.get("warnings", ["No warnings available"])[0]

            return f"""
Drug: {drug_name.capitalize()}
Brand Name: {brand_name}
Purpose: {purpose}
Warnings: {warnings}
"""
    except Exception as e:
        return f"Could not retrieve drug info for '{drug_name}'. Error: {str(e)}"
