# Trip Planner Crew

Trip Planner Crew is a Python tool that assists users in planning their trips by employing AI agents and natural language processing techniques.

## Overview

This project comprises several Python modules:

- **crewai**: This module contains the `Crew` class, which manages the trip planning crew.
- **trip_agents**: Here, you can find agents for city selection, local expertise, and travel concierge services.
- **trip_tasks**: Defines tasks for identifying, gathering information, and planning the trip.
- **langchain**: Includes the `llms` module for interacting with language models. Specifically, it utilizes the `Ollama` language model for natural language processing.

## Usage

To utilize Trip Planner Crew:

1. Install the necessary dependencies:

   ```
   pip install crewai
   ```

2. Execute the `trip_crew.py` script:

   ```
   python trip_crew.py
   ```

3. Follow the prompts to input your trip details:
   - Origin location
   - Cities of interest
   - Date range
   - Interests and hobbies

4. The tool will generate a trip plan based on your inputs and display it.

## Example

```python
from trip_crew import TripCrew

location = "New York"
cities = "London, Paris, Rome"
date_range = "June 1 - June 15"
interests = "History, Food, Culture"

trip_crew = TripCrew(location, cities, date_range, interests)
result = trip_crew.run()

print("\n\n########################")
print("## Here is your Trip Plan")
print("########################\n")
print(result)
```

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.
