import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Attempt Logfire instrumentation if available
try:
    import logfire
    logfire_token = os.getenv("LOGFIRE_TOKEN")
    if logfire_token:
        logfire.configure(token=logfire_token)
        logfire.instrument_requests()
except Exception as e:
    print(f"Logfire Init Error in UI: {e}")

# Page Configuration
st.set_page_config(
    page_title="Enterprise Agentic RAG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #4F46E5, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #6B7280;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .status-badge {
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .source-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown('<div class="main-header">⚡ Enterprise Agentic RAG System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">LangGraph State Orchestration • Qdrant Vector Search • Groq & Gemini Powered</div>', unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_url = st.text_input("FastAPI Backend URL", value="http://127.0.0.1:8000")
    thread_id = st.text_input("Session / Thread ID", value="user_session_1")

    # Backend Health Check
    st.subheader("🔌 Connection Status")
    try:
        health_resp = requests.get(f"{api_url}/", timeout=3)
        if health_resp.status_code == 200:
            st.success("Backend Connected (Online)")
        else:
            st.warning(f"Backend returned status code: {health_resp.status_code}")
    except Exception:
        st.error("Backend Offline (Ensure FastAPI is running)")

    st.markdown("---")
    
    # Workflow Graph Preview
    st.subheader("🗺️ Architecture Graph")
    if st.button("View Agent Workflow Graph"):
        try:
            graph_resp = requests.get(f"{api_url}/graph", timeout=5)
            if graph_resp.status_code == 200 and "image" in graph_resp.headers.get("content-type", ""):
                st.image(graph_resp.content, caption="LangGraph Workflow Pipeline", use_container_width=True)
            else:
                st.info("Graph endpoint did not return an image.")
        except Exception as err:
            st.error(f"Could not load graph: {err}")

    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Initialize Chat State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display Thought Process if present
        if message.get("thought_process"):
            with st.expander("🧠 Agent Thought Process & Plan", expanded=False):
                for step in message["thought_process"]:
                    st.write(f"- {step}")
                    
        # Display Sources if present
        if message.get("sources"):
            with st.expander("📚 Retrieved Context Sources", expanded=False):
                for i, doc in enumerate(message["sources"]):
                    st.markdown(f"**Source {i+1}:**")
                    if isinstance(doc, dict):
                        st.json(doc)
                    else:
                        st.write(str(doc))

# User Query Input
user_query = st.chat_input("Ask a question about the indexed enterprise documents...")

if user_query:
    # Append User Message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Process via FastAPI Backend
    with st.chat_message("assistant"):
        with st.spinner("Agent is reasoning, retrieving context, and generating response..."):
            try:
                response = requests.post(
                    f"{api_url}/query",
                    json={"q": user_query, "thread_id": thread_id},
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer returned.")
                    plan = data.get("thought_process", [])
                    sources = data.get("sources", [])
                    
                    st.markdown(answer)
                    
                    if plan:
                        with st.expander("🧠 Agent Thought Process & Plan", expanded=False):
                            for step in plan:
                                st.write(f"- {step}")
                                
                    if sources:
                        with st.expander("📚 Retrieved Context Sources", expanded=False):
                            for i, doc in enumerate(sources):
                                st.markdown(f"**Source {i+1}:**")
                                if isinstance(doc, dict):
                                    st.json(doc)
                                else:
                                    st.write(str(doc))
                                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "thought_process": plan,
                        "sources": sources
                    })
                else:
                    error_msg = f"Backend error ({response.status_code}): {response.text}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    
            except Exception as e:
                error_msg = f"Failed to connect to FastAPI backend at `{api_url}`: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
