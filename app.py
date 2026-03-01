import os

import streamlit as st
from dotenv import load_dotenv

from src.crew import TripCrew

load_dotenv()

st.set_page_config(
    page_title="AI Trip Planner",
    page_icon="assets/favicon.png" if os.path.exists("assets/favicon.png") else None,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.5px;
        margin-bottom: 0;
    }
    .main-subtitle {
        font-size: 1.15rem;
        color: #64748b;
        margin-top: 0.25rem;
        margin-bottom: 2rem;
    }
    .agent-step {
        background: #f1f5f9;
        border-left: 4px solid #3b82f6;
        padding: 0.75rem 1rem;
        border-radius: 0 6px 6px 0;
        margin: 0.3rem 0;
        font-family: monospace;
        font-size: 0.82rem;
        color: #334155;
        white-space: pre-wrap;
        word-break: break-word;
    }
    .result-section {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.5rem 2rem;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #0f172a;
        color: #ffffff;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background-color: #1e293b;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "trip_result" not in st.session_state:
    st.session_state.trip_result = None
if "agent_log" not in st.session_state:
    st.session_state.agent_log = []
if "planning" not in st.session_state:
    st.session_state.planning = False


with st.sidebar:
    st.header("Configuration")
    st.caption("Enter your API keys or set them in a .env file.")

    openai_key = st.text_input(
        "OpenAI API Key",
        value=os.environ.get("OPENAI_API_KEY", ""),
        type="password",
        help="Get your key at platform.openai.com/api-keys",
    )
    serper_key = st.text_input(
        "Serper API Key",
        value=os.environ.get("SERPER_API_KEY", ""),
        type="password",
        help="Free tier available at serper.dev",
    )
    model_choice = st.selectbox(
        "OpenAI Model",
        options=["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        help="gpt-4o-mini gives the best cost-to-quality ratio for trip planning",
    )

    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
    if serper_key:
        os.environ["SERPER_API_KEY"] = serper_key
    os.environ["OPENAI_MODEL"] = model_choice

    st.divider()
    st.markdown("**How it works**")
    st.markdown(
        "Three AI agents collaborate in sequence:\n\n"
        "**1. City Selector** picks the best destination from your options\n\n"
        "**2. Local Expert** builds a detailed insider city guide\n\n"
        "**3. Travel Concierge** assembles your full day-by-day itinerary"
    )

    st.divider()
    st.caption("Powered by [CrewAI](https://crewai.com) and [OpenAI](https://openai.com)")


st.markdown('<h1 class="main-title">AI Trip Planner</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="main-subtitle">Three autonomous AI agents research destinations, curate local guides, and build your personalized itinerary.</p>',
    unsafe_allow_html=True,
)

col_left, col_right = st.columns(2, gap="large")

with col_left:
    origin = st.text_input(
        "Traveling from",
        placeholder="e.g. New York",
    )
    date_range = st.text_input(
        "Travel dates",
        placeholder="e.g. September 5 to September 20, 2025",
    )
    budget = st.selectbox(
        "Budget level",
        options=["Budget", "Mid-range", "Luxury"],
        index=1,
        help="Shapes hotel, restaurant, and activity recommendations",
    )

with col_right:
    destinations = st.text_input(
        "Destination options",
        placeholder="e.g. Tokyo, Bangkok, Bali",
        help="Separate multiple cities with commas",
    )
    interests = st.text_area(
        "Interests and hobbies",
        placeholder="e.g. street food, temples, photography, hiking, nightlife",
        height=104,
    )
    travelers = st.number_input(
        "Number of travelers",
        min_value=1,
        max_value=20,
        value=1,
        step=1,
    )

st.markdown("")


def get_validation_errors() -> list[str]:
    errors = []
    if not origin.strip():
        errors.append("Enter your departure city.")
    if not destinations.strip():
        errors.append("Enter at least one destination.")
    if not date_range.strip():
        errors.append("Enter your travel dates.")
    if not interests.strip():
        errors.append("Describe your interests so agents can personalize your plan.")
    if not os.environ.get("OPENAI_API_KEY"):
        errors.append("Add your OpenAI API key in the sidebar.")
    if not os.environ.get("SERPER_API_KEY"):
        errors.append("Add your Serper API key in the sidebar.")
    return errors


if st.button("Plan My Trip", type="primary"):
    errors = get_validation_errors()
    if errors:
        for msg in errors:
            st.error(msg)
    else:
        st.session_state.trip_result = None
        st.session_state.agent_log = []

        collected_logs: list[str] = []

        def capture_step(output: object) -> None:
            text = str(output)
            if text.strip():
                collected_logs.append(text)
                st.session_state.agent_log = collected_logs[:]

        with st.spinner("Your AI travel crew is researching and planning. This takes a few minutes..."):
            try:
                crew = TripCrew(
                    origin=origin.strip(),
                    destinations=destinations.strip(),
                    date_range=date_range.strip(),
                    interests=interests.strip(),
                    budget=budget,
                    travelers=int(travelers),
                )
                result = crew.run(step_callback=capture_step)
                st.session_state.trip_result = result
                st.success("Your itinerary is ready.")
            except Exception as exc:
                st.error(f"Planning failed: {exc}")


if st.session_state.trip_result:
    st.divider()

    if st.session_state.agent_log:
        with st.expander("Agent Activity Log", expanded=False):
            for entry in st.session_state.agent_log:
                st.markdown(
                    f'<div class="agent-step">{entry[:600]}</div>',
                    unsafe_allow_html=True,
                )

    st.subheader("Your Personalized Itinerary")
    st.markdown(
        '<div class="result-section">',
        unsafe_allow_html=True,
    )
    st.markdown(st.session_state.trip_result)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")
    dl_col, _ = st.columns([1, 4])
    with dl_col:
        st.download_button(
            label="Download Itinerary",
            data=st.session_state.trip_result,
            file_name="trip_itinerary.md",
            mime="text/markdown",
        )
