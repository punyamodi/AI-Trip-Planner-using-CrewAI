import os

from crewai import Agent
from langchain_openai import ChatOpenAI

from src.tools.calculator import CalculatorTool
from src.tools.search import SearchTool


def build_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        temperature=0.7,
    )


class TripAgents:
    def __init__(self) -> None:
        self.llm = build_llm()
        self.search = SearchTool()
        self.calculator = CalculatorTool()

    def city_selection_agent(self) -> Agent:
        return Agent(
            role="City Selection Expert",
            goal="Identify and recommend the single best destination from the provided options based on weather, upcoming events, flight costs, and traveler preferences",
            backstory=(
                "A veteran travel analyst with fifteen years of experience comparing global destinations. "
                "You specialize in matching travelers to cities by evaluating seasonal weather, local cultural events, "
                "flight affordability, and overall fit with each traveler's interests and budget."
            ),
            tools=[self.search],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
        )

    def local_expert_agent(self) -> Agent:
        return Agent(
            role="Local Expert",
            goal="Compile a rich, authentic insider guide to the selected city covering attractions, culture, cuisine, neighborhoods, and practical logistics",
            backstory=(
                "A well-traveled local guide who has spent years living in and exploring cities across every continent. "
                "You know the places that never appear in standard guidebooks and can craft recommendations that perfectly "
                "match each traveler's unique interests and travel style."
            ),
            tools=[self.search],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
        )

    def travel_concierge_agent(self) -> Agent:
        return Agent(
            role="Travel Concierge",
            goal="Create a complete, personalized travel itinerary with day-by-day plans, hotel and restaurant picks, a packing list, and a detailed budget breakdown",
            backstory=(
                "An elite travel concierge with decades of experience crafting seamless trips for all budgets. "
                "You excel at turning destination research into actionable, day-by-day itineraries that balance "
                "exploration, relaxation, and value, always recommending specific real places rather than vague suggestions."
            ),
            tools=[self.search, self.calculator],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
        )
