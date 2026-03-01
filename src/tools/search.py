import json
import os
from typing import Type

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class SearchInput(BaseModel):
    query: str = Field(description="The search query to look up on the internet")


class SearchTool(BaseTool):
    name: str = "Search Internet"
    description: str = (
        "Searches the internet for up-to-date information about travel destinations, "
        "weather forecasts, flight costs, local events, hotels, and restaurants."
    )
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query, "num": 5})
        headers = {
            "X-API-KEY": os.environ.get("SERPER_API_KEY", ""),
            "content-type": "application/json",
        }

        try:
            response = requests.post(url, headers=headers, data=payload, timeout=15)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            return f"Search request failed: {exc}"

        if "organic" not in data:
            return "No results found. Verify your Serper API key is valid."

        output = []
        for item in data["organic"][:5]:
            title = item.get("title", "")
            link = item.get("link", "")
            snippet = item.get("snippet", "")
            output.append(f"Title: {title}\nURL: {link}\nSummary: {snippet}\n---")

        return "\n".join(output)
