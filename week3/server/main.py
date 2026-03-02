from mcp.server.fastmcp import FastMCP
import httpx
import os
import json # Tambahkan library json

app = FastMCP("Game-MCP-Server")

API_KEY = os.getenv("RAWG_API_KEY")
BASE_URL = "https://api.rawg.io/api"

@app.tool()
async def search_game(name: str) -> str: # Tambahkan petunjuk tipe kembalian -> str
    """Search for a game by name"""
    url = f"{BASE_URL}/games"
    params = {
        "key": API_KEY,
        "search": name,
        "page_size": 5
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)

        response.raise_for_status()
        games = response.json().get("results", [])

        if not games:
            return "Game not found."

        # Simpan hasil dalam list, lalu konversi menjadi JSON String
        result = [
            {
                "id": game["id"],
                "name": game["name"],
                "rating": game["rating"]
            }
            for game in games
        ]
        return json.dumps(result, indent=2)

    except Exception as e:
        return f"Error: {str(e)}"


@app.tool()
async def get_game_detail(game_id: int) -> str:
    """Get game details by ID"""
    url = f"{BASE_URL}/games/{game_id}"
    params = {"key": API_KEY}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)

        response.raise_for_status()
        game = response.json()

        # Simpan hasil dalam dict, lalu konversi menjadi JSON String
        result = {
            "name": game.get("name"),
            "released": game.get("released"),
            "rating": game.get("rating")
        }
        return json.dumps(result, indent=2)

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run()