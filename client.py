import asyncio
from rich.console import Console
from rich.table import Table
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from config import GROQ_API_KEY
import httpx


console = Console()


async def main():
    client = MultiServerMCPClient(
        {
            "weather": {
                "url": "https://toolsproject.onrender.com/weather/mcp",
                "transport": "streamable_http",
            },
            "events": {
                "url": "https://toolsproject.onrender.com/events/mcp",
                "transport": "streamable_http",
            },
            "map": {
                "url": "https://toolsproject.onrender.com/maps/mcp",
                "transport": "streamable_http",
            },
        }
    )

    tools = await client.get_tools()
    table = Table(title="Available MCP Tools")
    table.add_column("Tool Name", style="cyan")
    table.add_column("Description", style="green")

    for tool in tools:
        table.add_row(tool.name, tool.description or "—")

    console.print(table)

    model = ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=GROQ_API_KEY,
        temperature=0.3,
        max_tokens=4096,
    )

    agent = create_react_agent(model=model, tools=tools)

    user_prompt = "Plan a 1-week trip to Goa with sightseeing and local events."

    console.rule("[bold blue]User Query[/bold blue]")
    console.print(f"[bold yellow]{user_prompt}[/bold yellow]\n")

    # 🧠 AI Creates Itinerary
    response = await agent.ainvoke({"messages": [{"role": "user", "content": user_prompt}]})

    itinerary_output = ""
    console.rule("[bold green]Trip Planner AI Response[/bold green]")

    for msg in response["messages"]:
        if msg.content:
            itinerary_output += msg.content + "\n"
            console.print(msg.content)

    console.rule("[bold blue]End of Response[/bold blue]")

    # ✅ Save to database through server API
    async with httpx.AsyncClient() as http:
        payload = {
            "city": "Goa",
            "start_date": "2025-02-01",
            "duration": 7,
            "prompt": user_prompt,
            "itinerary": itinerary_output.strip()
        }
        save_res = await http.post("https://toolsproject.onrender.com/save_trip", json=payload)

        console.rule("[bold green]DB Save Result[/bold green]")
        console.print(save_res.json())


if __name__ == "__main__":
    asyncio.run(main())
