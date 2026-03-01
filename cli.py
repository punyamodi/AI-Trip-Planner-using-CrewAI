import sys
from textwrap import dedent

from dotenv import load_dotenv

from src.crew import TripCrew

load_dotenv()

BUDGET_OPTIONS = ["Budget", "Mid-range", "Luxury"]


def prompt(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value if value else default


def main() -> None:
    print("AI Trip Planner")
    print("=" * 50)
    print()

    origin = prompt("Traveling from")
    if not origin:
        print("Departure city is required.")
        sys.exit(1)

    destinations = prompt("Destination options (comma-separated)")
    if not destinations:
        print("At least one destination is required.")
        sys.exit(1)

    date_range = prompt("Travel dates (e.g. June 1 to June 15, 2025)")
    if not date_range:
        print("Travel dates are required.")
        sys.exit(1)

    interests = prompt("Your interests and hobbies (e.g. food, history, hiking)")
    if not interests:
        print("Please describe your interests.")
        sys.exit(1)

    budget_input = prompt("Budget level (Budget / Mid-range / Luxury)", "Mid-range")
    budget = budget_input if budget_input in BUDGET_OPTIONS else "Mid-range"

    travelers_input = prompt("Number of travelers", "1")
    try:
        travelers = max(1, int(travelers_input))
    except ValueError:
        travelers = 1

    print()
    print(
        dedent(
            f"""\
        Planning your trip with the following details:
          From:        {origin}
          To:          {destinations}
          Dates:       {date_range}
          Interests:   {interests}
          Budget:      {budget}
          Travelers:   {travelers}
        """
        )
    )
    print("This may take a few minutes...\n")

    crew = TripCrew(
        origin=origin,
        destinations=destinations,
        date_range=date_range,
        interests=interests,
        budget=budget,
        travelers=travelers,
    )

    result = crew.run()

    print()
    print("=" * 50)
    print("YOUR TRIP ITINERARY")
    print("=" * 50)
    print()
    print(result)

    output_file = "trip_itinerary.md"
    with open(output_file, "w", encoding="utf-8") as fh:
        fh.write(result)
    print(f"\nItinerary saved to {output_file}")


if __name__ == "__main__":
    main()
