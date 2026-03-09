import streamlit as st
import requests
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Mini RAG Search",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stAlert {
        padding: 1rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_url' not in st.session_state:
    # st.session_state.api_url = "http://localhost:8000"
    st.session_state.api_url = "https://rag-api-5j63.onrender.com"
if 'chunks_count' not in st.session_state:
    st.session_state.chunks_count = 0
if 'query_history' not in st.session_state:
    st.session_state.query_history = []


def check_api_health(url):
    """Check if the API is running"""
    try:
        response = requests.get(f"{url}/health", timeout=3)
        return response.status_code == 200
    except:
        return False


def ingest_document(url, file):
    """Upload and ingest a document"""
    try:
        files = {"file": (file.name, file.getvalue(), "text/plain")}
        response = requests.post(f"{url}/ingest", files=files, timeout=60)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}: {response.text}"}
    except requests.exceptions.ConnectionError:
        return {"error": f"Cannot connect to {url}. Make sure FastAPI is running."}
    except Exception as e:
        return {"error": str(e)}


def query_document(url, question, top_k=3):
    """Query the document with extended timeout for Mistral"""
    try:
        payload = {
            "question": question,
            "top_k": top_k
        }

        # Increase timeout to 5 minutes for Mistral
        response = requests.post(
            f"{url}/query",
            json=payload,
            timeout=300  # 5 minutes timeout
        )

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}: {response.text}"}

    except requests.exceptions.Timeout:
        return {
            "error": "⚠️ The request timed out. Mistral is taking too long to respond. Please try again with a simpler question."}
    except requests.exceptions.ConnectionError:
        return {"error": f"Cannot connect to {url}. Make sure FastAPI is running."}
    except Exception as e:
        return {"error": str(e)}


# Main app
st.markdown("<h1 class='main-header'>🔍 Mini RAG Search System</h1>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")

    api_url = st.text_input(
        "FastAPI URL",
        value=st.session_state.api_url,
        help="Enter the URL where your FastAPI backend is running"
    )
    st.session_state.api_url = api_url

    # Check connection
    with st.spinner("Checking connection..."):
        api_status = check_api_health(api_url)

    if api_status:
        st.success("✅ Connected to FastAPI backend")

        # Document Ingestion
        st.markdown("---")
        st.header("📄 Document Ingestion")

        uploaded_file = st.file_uploader(
            "Upload a text file",
            type=['txt'],
            help="Upload a .txt file to ingest"
        )

        if uploaded_file is not None:
            if st.button("📤 Ingest Document", type="primary", use_container_width=True):
                with st.spinner("Ingesting document..."):
                    result = ingest_document(api_url, uploaded_file)

                    if "error" in result:
                        st.error(f"❌ {result['error']}")
                    else:
                        st.success(f"✅ Document ingested successfully!")
                        st.info(f"📊 Created {result['chunks']} chunks")
                        st.session_state.chunks_count = result['chunks']

        # Settings
        st.markdown("---")
        st.header("⚙️ Query Settings")

        # Add warning about Mistral speed
        st.warning("⚠️ Mistral model takes 2-3 minutes to respond")

        top_k = st.slider(
            "Number of chunks (top_k)",
            min_value=1,
            max_value=10,
            value=3
        )

        # Stats
        if st.session_state.chunks_count > 0:
            st.metric("Total Chunks in DB", st.session_state.chunks_count)

        # Query History
        st.markdown("---")
        st.header("📋 Query History")
        if st.session_state.query_history:
            for item in reversed(st.session_state.query_history[-5:]):
                st.markdown(f"**Q:** {item['question'][:50]}...")
        else:
            st.info("No queries yet")

    else:
        st.error("❌ Cannot connect to FastAPI backend")
        st.info(f"Make sure FastAPI is running at:\n{api_url}")
        st.stop()

# Main content area
st.header("💬 Ask Questions")

# Query input
question = st.text_input(
    "Enter your question:",
    placeholder="e.g., What is the main topic discussed in the document?",
    key="query_input"
)

# Create columns for better layout
col1, col2 = st.columns([1, 5])

with col1:
    query_button = st.button("🚀 Ask Question", type="primary", use_container_width=True)

# Handle query
if query_button and question:
    if st.session_state.chunks_count == 0:
        st.warning("⚠️ No documents have been ingested yet. Please upload a document first.")
    else:
        # Show warning about wait time
        st.warning("⏳ Mistral is thinking... This will take 2-3 minutes. Please wait.")

        # Create a progress bar to show activity
        progress_bar = st.progress(0)
        status_text = st.empty()

        start_time = time.time()

        # Update progress every 30 seconds to show it's working
        for i in range(6):
            time.sleep(30)  # Wait 30 seconds
            elapsed = time.time() - start_time
            progress = min(int((elapsed / 180) * 100), 100)  # 180 seconds = 3 minutes
            progress_bar.progress(progress)
            status_text.text(f"⏱️ Elapsed time: {int(elapsed)} seconds... Still working on it...")

            # Check if we have a result (this is a hack - in reality we need async)
            if i == 5:  # After 3 minutes, make the actual request
                status_text.text("✅ Almost done...")

        # Make the actual query
        result = query_document(api_url, question, top_k)

        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()

        if "error" in result:
            st.error(f"❌ {result['error']}")
        else:
            # Add to history
            st.session_state.query_history.append({
                "question": question,
                "answer": result['answer'][:50] + "...",
                "time": datetime.now().strftime("%H:%M:%S")
            })

            # Display answer
            st.markdown("### 📝 Answer:")
            st.markdown(f"> {result['answer']}")

            # Display sources
            with st.expander("🔍 View Source Chunks", expanded=False):
                for i, source in enumerate(result['sources'], 1):
                    st.text_area(
                        label=f"Chunk {i}",
                        value=source,
                        height=150,
                        key=f"source_{i}_{int(time.time())}"
                    )

elif query_button and not question:
    st.warning("⚠️ Please enter a question")

# Footer with instructions
with st.expander("📖 Quick Start Guide"):
    st.markdown("""
    1. **Start FastAPI backend** (in a terminal):
       ```bash
       uvicorn main:app --reload --port 8000""")