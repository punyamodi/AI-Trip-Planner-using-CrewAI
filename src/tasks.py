from crewai import Agent, Task


class TripTasks:
    def identify_city_task(
        self,
        agent: Agent,
        origin: str,
        destinations: str,
        interests: str,
        date_range: str,
        budget: str,
        travelers: int,
    ) -> Task:
        return Task(
            description=(
                f"Analyze each of the following destination options and recommend the single best city for this trip: {destinations}.\n\n"
                f"Evaluate each destination on:\n"
                f"1. Weather conditions and climate during {date_range}\n"
                f"2. Cultural events, festivals, or seasonal highlights during the visit\n"
                f"3. Estimated round-trip flight costs from {origin}\n"
                f"4. Overall affordability suitable for a {budget} budget with {travelers} traveler(s)\n"
                f"5. Alignment with the traveler's interests: {interests}\n\n"
                f"Search for current data on each destination before finalizing your recommendation. "
                f"Compare all options before making a decision."
            ),
            expected_output=(
                "A detailed destination selection report containing:\n"
                "- The recommended city with a clear, well-reasoned justification\n"
                "- Weather forecast summary for the specified travel period\n"
                "- Estimated round-trip flight cost from the origin city\n"
                "- Key events or festivals happening during the visit\n"
                "- A brief comparison of why the chosen city beats the other options\n"
                "- Why this destination best matches the traveler's interests and budget"
            ),
            agent=agent,
        )

    def gather_city_info_task(
        self,
        agent: Agent,
        origin: str,
        interests: str,
        date_range: str,
        budget: str,
        travelers: int,
    ) -> Task:
        return Task(
            description=(
                f"Using the destination selected in the previous task, compile a comprehensive local guide.\n\n"
                f"Cover each of the following areas thoroughly:\n"
                f"1. Top attractions and must-see landmarks with practical visitor tips\n"
                f"2. Hidden gems and local favorites that typical tourists miss\n"
                f"3. Best neighborhoods for exploring, dining, and staying\n"
                f"4. Local cuisine highlights and specific restaurant recommendations across price ranges\n"
                f"5. Cultural customs, local etiquette, and behavior to be aware of\n"
                f"6. Getting around the city: transportation options and estimated costs\n"
                f"7. Safety considerations and areas to approach with caution\n"
                f"8. Weather-specific advice for {date_range}\n\n"
                f"Traveler interests: {interests}\n"
                f"Budget level: {budget}\n"
                f"Number of travelers: {travelers}\n"
                f"Traveling from: {origin}"
            ),
            expected_output=(
                "A comprehensive city guide including:\n"
                "- Curated attraction list with descriptions, opening hours where available, and visitor tips\n"
                "- Neighborhood guide with character descriptions and highlights\n"
                "- Restaurant and food recommendations spanning budget to mid-range to upscale\n"
                "- Cultural do's and don'ts with context\n"
                "- Transportation guide with estimated costs\n"
                "- Practical tips tailored to the specific travel dates, group size, and traveler interests"
            ),
            agent=agent,
        )

    def create_itinerary_task(
        self,
        agent: Agent,
        origin: str,
        interests: str,
        date_range: str,
        budget: str,
        travelers: int,
    ) -> Task:
        return Task(
            description=(
                f"Using the destination analysis and city guide from the previous tasks, create a complete day-by-day travel itinerary.\n\n"
                f"The itinerary must include all of the following:\n"
                f"1. A structured daily schedule with morning, afternoon, and evening activities and specific locations\n"
                f"2. Specific hotel recommendations with estimated nightly rates suited to a {budget} budget\n"
                f"3. Restaurant recommendations for breakfast, lunch, and dinner each day with estimated costs\n"
                f"4. Clear transport instructions between locations including estimated time and cost\n"
                f"5. A weather-appropriate packing checklist for {date_range}\n"
                f"6. A detailed budget breakdown for {travelers} traveler(s) covering flights, accommodation, meals, transport, and activities\n"
                f"7. Practical daily tips: best time to arrive at popular spots, booking advice, local phrases\n\n"
                f"Travel dates: {date_range}\n"
                f"Traveling from: {origin}\n"
                f"Interests: {interests}\n"
                f"Budget level: {budget}\n"
                f"Number of travelers: {travelers}\n\n"
                f"Format the entire output as clean, well-structured Markdown."
            ),
            expected_output=(
                "A complete Markdown travel itinerary containing:\n"
                "- Day-by-day schedule with specific times, named locations, and brief descriptions\n"
                "- Hotel options with estimated prices per night and booking tips\n"
                "- Named restaurant recommendations for each meal with estimated cost per person\n"
                "- A packing checklist tailored to the destination, season, and activities\n"
                "- A budget table in USD showing per-person and total estimated costs\n"
                "- Practical tips and local insights woven into each day's plan"
            ),
            agent=agent,
        )
