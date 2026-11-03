import os
import glob
import chromadb
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    import google.generativeai as genai
except ImportError:
    genai = None

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "cambridge_care_knowledge"

def load_knowledge_documents():
    """Reads the 5 numbered source knowledge documents (01_ to 05_) and splits them into sections."""
    doc_paths = sorted(glob.glob(os.path.join(BASE_DIR, "0*.txt")))
    chunks = []
    
    for path in doc_paths:
        filename = os.path.basename(path)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            sections = content.split("\n\n")
            for sec in sections:
                cleaned = sec.strip()
                if len(cleaned) > 40:
                    chunks.append({
                        "source": filename,
                        "text": cleaned
                    })
    return chunks

def get_or_create_chroma_db():
    """
    Initializes ChromaDB persistent client on disk.
    If the database collection is empty, it automatically populates it with all 37 chunks.
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    
    # Try to get existing collection or create new one
    try:
        collection = client.get_collection(name=COLLECTION_NAME)
        if collection.count() >= 37:
            return collection
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Cambridge Care Services Official Knowledge Base"}
    )
    
    # Populate collection if empty
    if collection.count() == 0:
        chunks = load_knowledge_documents()
        documents = [c["text"] for c in chunks]
        metadatas = [{"source": c["source"]} for c in chunks]
        ids = [f"chunk_{i+1:03d}" for i in range(len(chunks))]
        
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    return collection

def retrieve_relevant_context(query: str, top_k: int = 4):
    """
    Queries ChromaDB Vector Database using mathematical vector search.
    Returns the top matching chunks directly from ChromaDB.
    """
    collection = get_or_create_chroma_db()
    
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    matched_chunks = []
    if results and "documents" in results and results["documents"]:
        docs = results["documents"][0]
        metas = results["metadatas"][0] if "metadatas" in results else [{}] * len(docs)
        for doc, meta in zip(docs, metas):
            matched_chunks.append({
                "source": meta.get("source", "Unknown"),
                "text": doc
            })
            
    return matched_chunks

# In-memory query cache to serve identical or preset questions instantly
_RESPONSE_CACHE = {}

def ask_cambridge_care_bot(question: str, api_key: str = None) -> str:
    """
    Main RAG function:
    1. Checks cache for instant zero-latency responses.
    2. Retrieves relevant chunks from ChromaDB.
    3. Prompts Gemini with strict caregiving guardrails and auto-retry logic.
    """
    clean_q = question.strip().lower()
    if clean_q in _RESPONSE_CACHE:
        return _RESPONSE_CACHE[clean_q]

    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            try:
                import streamlit as st
                api_key = st.secrets.get("GEMINI_API_KEY", "")
            except Exception:
                pass

    if not api_key:
        return "Please provide a valid Gemini API key in your .env file to start chatting."

    if genai is None:
        return "Error: google-generativeai package is not installed in the active Python environment."

    # Configure the Gemini API
    genai.configure(api_key=api_key)
    
    # Pool of high-speed models to try with automatic fallback across free quota tiers
    models_to_try = ["gemini-flash-lite-latest", "gemini-2.5-flash-lite", "gemini-3-flash-preview"]

    # Retrieve relevant document chunks from ChromaDB
    relevant_chunks = retrieve_relevant_context(question, top_k=4)
    
    context_text = "\n\n---\n\n".join(
        [f"[From {c['source']}]:\n{c['text']}" for c in relevant_chunks]
    )

    # System instruction with healthcare guardrails
    system_prompt = f"""You are the official, friendly, and compassionate AI assistant for Cambridge Care Services, a CQC-regulated home care provider in Cambridge and South Cambridgeshire.

OFFICIAL KNOWLEDGE BASE CONTEXT (RETRIEVED FROM CHROMADB):
{context_text}

STRICT OPERATING GUIDELINES:
1. ONLY answer based on the facts provided in the knowledge base above. Do NOT make up services, policies, or coverage areas.
2. MEDICAL SAFETY GUARDRAIL: We provide non-clinical home care. You must NEVER give medical advice, alter medication schedules, or make clinical diagnoses.
3. EMERGENCY PROTOCOL: If someone asks about a life-threatening emergency, severe fall, or acute medical issue, immediately instruct them to dial 999 (or 111 for urgent NHS health advice).
4. LEAD GENERATION: When a family inquires about starting care or costs, warmly invite them to book a "Free, no-obligation Home Assessment" or offer to take their details so our team can call them. Mention our phone number: 07917 611 425.
5. TONE: Warm, respectful, empathetic, reassuring, and professional.

USER QUESTION:
{question}

YOUR HELPFUL RESPONSE:"""

    import time
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(system_prompt)
            result = response.text
            _RESPONSE_CACHE[clean_q] = result
            return result
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "quota" in err_msg.lower():
                # Model hit its daily or burst limit; try the next model in the pool
                continue
            else:
                return f"Error contacting AI service: {err_msg}"

    return "The free Google Gemini API rate limit was momentarily reached. Please wait a few seconds and send your question again."
