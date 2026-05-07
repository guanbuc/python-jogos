# -*- encoding: utf-8 -*-

import asyncio
from copilot import CopilotClient
from copilot.tools import define_tool

@define_tool("get_weather")
async def get_weather(city: str) -> dict:
    """Get weather for a city"""
    return {"city": city, "temp": "72°F"}

async def main():
    client = CopilotClient()
    await client.start()

    session = await client.create_session({
        "model": "gpt-4o",
        "tools": [get_weather]
    })
    print("Sessão iniciada com sucesso!")

if __name__ == "__main__":
    asyncio.run(main())
