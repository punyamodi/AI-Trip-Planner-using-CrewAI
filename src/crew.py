from typing import Callable, Optional

from crewai import Crew, Process

from src.agents import TripAgents
from src.tasks import TripTasks


class TripCrew:
    def __init__(
        self,
        origin: str,
        destinations: str,
        date_range: str,
        interests: str,
        budget: str = "Mid-range",
        travelers: int = 1,
    ) -> None:
        self.origin = origin
        self.destinations = destinations
        self.date_range = date_range
        self.interests = interests
        self.budget = budget
        self.travelers = travelers

    def run(self, step_callback: Optional[Callable] = None) -> str:
        agents = TripAgents()
        tasks = TripTasks()

        city_agent = agents.city_selection_agent()
        local_agent = agents.local_expert_agent()
        concierge_agent = agents.travel_concierge_agent()

        identify_task = tasks.identify_city_task(
            city_agent,
            self.origin,
            self.destinations,
            self.interests,
            self.date_range,
            self.budget,
            self.travelers,
        )
        gather_task = tasks.gather_city_info_task(
            local_agent,
            self.origin,
            self.interests,
            self.date_range,
            self.budget,
            self.travelers,
        )
        plan_task = tasks.create_itinerary_task(
            concierge_agent,
            self.origin,
            self.interests,
            self.date_range,
            self.budget,
            self.travelers,
        )

        crew_kwargs = {
            "agents": [city_agent, local_agent, concierge_agent],
            "tasks": [identify_task, gather_task, plan_task],
            "process": Process.sequential,
            "verbose": True,
        }

        if step_callback is not None:
            crew_kwargs["step_callback"] = step_callback

        crew = Crew(**crew_kwargs)
        result = crew.kickoff()
        return str(result)
