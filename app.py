import streamlit as st
import os
import shutil
import time
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# --- 1. CONFIG & STYLING ---
st.set_page_config(
    page_title="AI PDF Mind",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS for Glassmorphism and modern feel
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at top right, #1a1a2e, #16213e);
        color: #e94560 !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(22, 33, 62, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(233, 69, 96, 0.2);
    }

    /* Chat Bubble Styling */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(5px);
        border-radius: 15px !important;
        border: 1px solid rgba(233, 69, 96, 0.1);
        padding: 15px !important;
        margin-bottom: 10px !important;
    }

    /* Assistant Message Specific */
    div[data-testid="chatAvatarIcon-assistant"] {
        background-color: #e94560 !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #e94560, #0f3460);
        color: white;
        border: none;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(233, 69, 96, 0.4);
    }

    /* Header Styling */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 700 !important;
        background: -webkit-linear-gradient(#e94560, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Hide Streamlit components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# API Keys
# API Keys - Use environment variables for security
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.sidebar.error("⚠️ GROQ_API_KEY not found! Please set it in your environment.")


# --- 2. CORE LOGIC ---
@st.cache_resource
def initialize_settings():
    # Fast LLM via Groq
    Settings.llm = Groq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)
    
    # Efficient Local Embeddings
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    
    Settings.chunk_size = 512
    Settings.chunk_overlap = 50

initialize_settings()

def clear_chat():
    st.session_state.messages = []
    st.rerun()

def reset_index():
    if "query_engine" in st.session_state:
        del st.session_state.query_engine
    if "index_data" in st.session_state:
        del st.session_state.index_data
    st.rerun()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
    st.title("Settings")
    st.markdown("---")
    
    
    if st.button("🗑️ Clear Chat History"):
        clear_chat()
        
    if st.button("🔄 Reset Document Index"):
        reset_index()

    st.markdown("---")
    st.markdown("")
    st.write(f"")
    st.write(f"")
    
    st.caption("")

# --- 4. MAIN INTERFACE ---
st.title("🧠 AI PDF Mind")
st.markdown("### Talk to your documents with lightning speed.")

# Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# File Uploader
uploaded_file = st.file_uploader("Upload your PDF to begin...", type="pdf")

if uploaded_file:
    # Use session state to persist the index for the current file
    if "query_engine" not in st.session_state:
        with st.status("⚡ Initializing Brain...", expanded=True) as status:
            st.write("Creating temporary workspace...")
            temp_dir = "data_input"
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
            
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.write("Reading document structure...")
            documents = SimpleDirectoryReader(input_dir=temp_dir).load_data()
            
            st.write("Generating vector embeddings (CPU-accelerated)...")
            index = VectorStoreIndex.from_documents(documents)
            
            st.write("Optimizing query engine...")
            st.session_state.query_engine = index.as_query_engine(streaming=True)
            
            # Clean up
            shutil.rmtree(temp_dir)
            status.update(label="✅ Mind Fully Synchronized!", state="complete", expanded=False)
            st.toast("Document Indexed Successfully!", icon="🚀")

    # Chat Display
    st.divider()
    chat_container = st.container()
    
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Ask a question about " + uploaded_file.name):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = st.session_state.query_engine.query(prompt)
                full_response = st.write_stream(response.response_gen)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error communicating with Groq: {e}")
                st.info("Try resetting the index if the error persists.")

else:
    # Welcome Message when no file is uploaded
    st.markdown("""
    ---
    #### How to get started:
    1. 📁 **Upload** a PDF document using the box above.
    2. ⏳ **Wait** a few seconds for the 'Mind Sync' to complete.
    3. 💬 **Chat** with your document naturally!
    

    """)

