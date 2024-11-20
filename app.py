import streamlit as st
from phi.tools.tavily import TavilyTools
from assistant import get_research_assistant 

import os
from dotenv import load_dotenv
load_dotenv()  # Loads the .env file


# Fetch the API key from the environment variable
api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    raise ValueError("API key not found in environment variables")

st.set_page_config(
    page_title="Research Assistant",
    page_icon=":book:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .report-title {
        font-size: 24px;
        font-weight: bold;
        color: #FF4B4B;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        font-size: 16px;
        border-radius: 10px;
    }
    .stButton>button:hover {
        background-color: #FF6347;
        color: white;
    }
    .sidebar .stButton>button {
        background-color: #0073e6;
        color: white;
        font-size: 14px;
        border-radius: 5px;
    }
    .sidebar .stButton>button:hover {
        background-color: #005bb5;
    }
    .stSidebar>div {
        padding: 10px;
        background-color: #f1f3f4;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title(":books: Research Assistant")

def main() -> None:
    llm_model = st.sidebar.selectbox(
        "Select Model", options=["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"]
    )
    if "llm_model" not in st.session_state:
        st.session_state["llm_model"] = llm_model
    elif st.session_state["llm_model"] != llm_model:
        st.session_state["llm_model"] = llm_model
        st.rerun()

    input_topic = st.text_input(
        "🔬 Enter a topic",
        value="Superfast Llama 3 inference on Groq Cloud",
        key="topic_input"
    )
    
    generate_report = st.button("Generate Report")
    if generate_report:
        st.session_state["topic"] = input_topic

    # Sidebar trending topics
    st.sidebar.markdown("## 📈 Trending Topics")
    if st.sidebar.button("Superfast Llama 3 inference on Groq Cloud"):
        st.session_state["topic"] = "Llama 3 on Groq Cloud"

    if st.sidebar.button("Latest cyber tech news."):
        st.session_state["topic"] = "Latest cyber tech news"

    if st.sidebar.button("Indian central budget 2024"):
        st.session_state["topic"] = "Indian central budget 2024"

    if st.sidebar.button("Nikola Tesla 369 theory"):
        st.session_state["topic"] = "Nikola Tesla 369 theory"

    if "topic" in st.session_state:
        report_topic = st.session_state["topic"]
        research_assistant = get_research_assistant(model=llm_model)
        tavily_search_results = None

        with st.status("🔍 Searching Web", expanded=True) as status:
            with st.container():
                tavily_container = st.empty()
                tavily_search_results = TavilyTools().web_search_using_tavily(report_topic)
                if tavily_search_results:
                    tavily_container.markdown(tavily_search_results)
            status.update(label="✅ Web Search Complete", state="complete", expanded=False)

        if not tavily_search_results:
            st.write("⚠️ Sorry, report generation failed. Please try again.")
            return

        with st.spinner("⏳ Generating Report..."):
            final_report = ""
            final_report_container = st.empty()
            for delta in research_assistant.run(tavily_search_results):
                final_report += delta  # type: ignore
                final_report_container.markdown(final_report, unsafe_allow_html=True)

    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Restart"):
        st.rerun()

main()