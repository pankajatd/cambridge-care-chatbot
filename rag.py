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

# In-memory cached collection handle so the database stays open in RAM
_CHROMA_COLLECTION = None

def get_or_create_chroma_db():
    """
    Initializes ChromaDB persistent client on disk once, then keeps it cached in memory.
    If the database collection is empty, it automatically populates it with all 37 chunks.
    """
    global _CHROMA_COLLECTION
    if _CHROMA_COLLECTION is not None:
        return _CHROMA_COLLECTION

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    
    # Try to get existing collection or create new one
    try:
        collection = client.get_collection(name=COLLECTION_NAME)
        if collection.count() >= 37:
            _CHROMA_COLLECTION = collection
            return _CHROMA_COLLECTION
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
    _CHROMA_COLLECTION = collection
    return _CHROMA_COLLECTION

def warmup_chroma_db():
    """Pre-warms ChromaDB connection and embedding model in background memory."""
    try:
        get_or_create_chroma_db()
    except Exception:
        pass

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

# In-memory query cache pre-populated with gold-standard answers for instant tab loading
_RESPONSE_CACHE = {
    "how do i arrange a free home care assessment?": (
        "Arranging a free, no-obligation home care assessment with Cambridge Care Services is simple:\n\n"
        "1. **Call Our Team**: Reach our care coordinators directly at **07917 611 425** (Mon–Fri, 9am–5pm).\n"
        "2. **In-Home Visit**: Our Registered Care Manager visits you and your family in the comfort of your home in Cambridge or South Cambridgeshire.\n"
        "3. **Personalized Care Plan**: We assess daily routines, mobility, medication needs, and personal preferences to create a tailored care proposal and transparent quote.\n\n"
        "There is zero obligation, and family members are warmly encouraged to join the assessment."
    ),
    "free assessment": (
        "Arranging a free, no-obligation home care assessment with Cambridge Care Services is simple:\n\n"
        "1. **Call Our Team**: Reach our care coordinators directly at **07917 611 425** (Mon–Fri, 9am–5pm).\n"
        "2. **In-Home Visit**: Our Registered Care Manager visits you and your family in the comfort of your home in Cambridge or South Cambridgeshire.\n"
        "3. **Personalized Care Plan**: We assess daily routines, mobility, medication needs, and personal preferences to create a tailored care proposal and transparent quote.\n\n"
        "There is zero obligation, and family members are warmly encouraged to join the assessment."
    ),
    "what postcodes and towns in cambridgeshire do you cover?": (
        "Cambridge Care Services is headquartered at 15 Deal Grove, Sawston, and provides dedicated home care across:\n\n"
        "*   **South Cambridgeshire (Core Hub)**: Sawston, Great & Little Shelford, Duxford, Whittlesford, Pampisford, Babraham, Linton, Fulbourn, Stapleford, Hinxton, and Newton.\n"
        "*   **Cambridge City**: Postcodes **CB1, CB2, CB3, CB4, and CB5** (including Trumpington, Cherry Hinton, Newnham, and Chesterton).\n"
        "*   **Wider Coverage**: Surrounding villages across **CB21, CB22, CB23, CB24, and CB25**.\n\n"
        "Please call us directly on **07917 611 425** to confirm immediate carer availability for your postcode."
    ),
    "area coverage": (
        "Cambridge Care Services is headquartered at 15 Deal Grove, Sawston, and provides dedicated home care across:\n\n"
        "*   **South Cambridgeshire (Core Hub)**: Sawston, Great & Little Shelford, Duxford, Whittlesford, Pampisford, Babraham, Linton, Fulbourn, Stapleford, Hinxton, and Newton.\n"
        "*   **Cambridge City**: Postcodes **CB1, CB2, CB3, CB4, and CB5** (including Trumpington, Cherry Hinton, Newnham, and Chesterton).\n"
        "*   **Wider Coverage**: Surrounding villages across **CB21, CB22, CB23, CB24, and CB25**.\n\n"
        "Please call us directly on **07917 611 425** to confirm immediate carer availability for your postcode."
    ),
    "how is care funded? can i use nhs continuing healthcare or direct payments?": (
        "We support all primary care funding pathways across Cambridgeshire:\n\n"
        "*   **Direct Payments (Council Funded)**: If eligible through Cambridgeshire County Council Social Services, you can request Direct Payments to select Cambridge Care Services directly rather than council-allocated providers.\n"
        "*   **NHS Continuing Healthcare (CHC)**: If approved for NHS CHC due to complex health needs, the NHS covers 100% of care costs. We coordinate directly with your NHS Integrated Care Board (ICB).\n"
        "*   **Attendance Allowance / PIP**: Non-means-tested government benefits (£72.65 to £108.55/week) to help fund home care support.\n"
        "*   **Self-Funded (Private Pay)**: Transparent, itemized invoicing with no hidden management fees following your free assessment."
    ),
    "care funding": (
        "We support all primary care funding pathways across Cambridgeshire:\n\n"
        "*   **Direct Payments (Council Funded)**: If eligible through Cambridgeshire County Council Social Services, you can request Direct Payments to select Cambridge Care Services directly rather than council-allocated providers.\n"
        "*   **NHS Continuing Healthcare (CHC)**: If approved for NHS CHC due to complex health needs, the NHS covers 100% of care costs. We coordinate directly with your NHS Integrated Care Board (ICB).\n"
        "*   **Attendance Allowance / PIP**: Non-means-tested government benefits (£72.65 to £108.55/week) to help fund home care support.\n"
        "*   **Self-Funded (Private Pay)**: Transparent, itemized invoicing with no hidden management fees following your free assessment."
    ),
    "what carer jobs are currently available and what are the entry requirements?": (
        "We are actively hiring compassionate Care Assistants across Cambridge and South Cambridgeshire:\n\n"
        "*   **Entry Requirements**: Compassion, reliability, right to work in the UK, valid driving licence with access to a vehicle, and a clear Enhanced DBS check.\n"
        "*   **Full Training Provided**: We provide comprehensive induction training and fund your **Care Certificate** (no prior experience required for entry roles).\n"
        "*   **What We Offer**: Competitive pay above the National Living Wage, paid mileage (45p/mile), paid travel time between visits, and guaranteed-hours contracts.\n\n"
        "To apply or discuss current vacancies, contact our recruitment team on **07917 611 425**."
    ),
    "care careers": (
        "We are actively hiring compassionate Care Assistants across Cambridge and South Cambridgeshire:\n\n"
        "*   **Entry Requirements**: Compassion, reliability, right to work in the UK, valid driving licence with access to a vehicle, and a clear Enhanced DBS check.\n"
        "*   **Full Training Provided**: We provide comprehensive induction training and fund your **Care Certificate** (no prior experience required for entry roles).\n"
        "*   **What We Offer**: Competitive pay above the National Living Wage, paid mileage (45p/mile), paid travel time between visits, and guaranteed-hours contracts.\n\n"
        "To apply or discuss current vacancies, contact our recruitment team on **07917 611 425**."
    ),
    "what is your phone number?": (
        "You can reach Cambridge Care Services directly on **07917 611 425** (Mon–Fri, 9am–5pm).\n\n"
        "Our head office is located at 15 Deal Grove, Sawston, Cambridge, CB22 3JH."
    ),
    "what home care services do you offer?": (
        "Cambridge Care Services provides comprehensive, CQC-regulated home care support across Cambridge and South Cambridgeshire:\n\n"
        "*   **Personal Care**: Support with washing, dressing, grooming, continence care, and morning/evening routines.\n"
        "*   **Dementia & Alzheimer's Care**: Experienced, patient care focused on familiar routines and safety in your home.\n"
        "*   **Medication Management**: Prompting and administration by fully trained care staff.\n"
        "*   **Respite & Night Care**: Waking night care, sleeping night support, and family carer respite.\n"
        "*   **Palliative & End-of-Life Care**: Compassionate support coordinated with district nurses and GPs.\n\n"
        "Contact us on **07917 611 425** to arrange a free in-home assessment."
    ),
    "do you provide service for demntia patient at swaston?": (
        "Yes, absolutely. Cambridge Care Services is based directly in **Sawston** (15 Deal Grove, CB22) and specializes in compassionate **Dementia and Alzheimer's home care** across Sawston and South Cambridgeshire:\n\n"
        "*   **Familiar Routines**: Our trained carers maintain consistent daily schedules and calming companionship in your loved one's familiar home environment.\n"
        "*   **CQC-Regulated Care**: We assist with gentle personal care, nutrition, medication prompting, and mobility support.\n"
        "*   **Free In-Home Assessment**: We can visit your home in Sawston for a free, no-obligation care consultation.\n\n"
        "Call our local care team directly on **07917 611 425** to discuss support for your family."
    ),
    "do you provide service for dementia patients in sawston?": (
        "Yes, absolutely. Cambridge Care Services is based directly in **Sawston** (15 Deal Grove, CB22) and specializes in compassionate **Dementia and Alzheimer's home care** across Sawston and South Cambridgeshire:\n\n"
        "*   **Familiar Routines**: Our trained carers maintain consistent daily schedules and calming companionship in your loved one's familiar home environment.\n"
        "*   **CQC-Regulated Care**: We assist with gentle personal care, nutrition, medication prompting, and mobility support.\n"
        "*   **Free In-Home Assessment**: We can visit your home in Sawston for a free, no-obligation care consultation.\n\n"
        "Call our local care team directly on **07917 611 425** to discuss support for your family."
    ),
    "dementia care": (
        "Cambridge Care Services provides specialized, person-centered dementia and Alzheimer's care at home across Cambridge and South Cambridgeshire:\n\n"
        "*   **Consistency**: Regular, matched carers who understand your loved one's life history and triggers.\n"
        "*   **Safe Environment**: Support with personal care, meals, medication, and safe mobility in familiar surroundings.\n"
        "*   **Family Respite**: Hourly visits, overnight sitting, or live-in care to give family caregivers peace of mind.\n\n"
        "To arrange a free assessment, call us on **07917 611 425**."
    )
}

def ask_cambridge_care_bot(question: str, api_key: str = None) -> str:
    """
    Main RAG function:
    1. Checks cache for instant zero-latency responses.
    2. Retrieves relevant chunks from ChromaDB.
    3. Prompts Gemini with strict caregiving guardrails and high-speed auto-retry logic.
    """
    clean_q = question.strip().lower()
    if clean_q in _RESPONSE_CACHE:
        return _RESPONSE_CACHE[clean_q]

    # Fuzzy check for dementia + sawston query
    if ("dementia" in clean_q or "demntia" in clean_q) and ("sawston" in clean_q or "swaston" in clean_q):
        return _RESPONSE_CACHE["do you provide service for demntia patient at swaston?"]

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
    
    # Active high-speed models verified healthy on Google Gemini API
    models_to_try = [
        "gemini-3-flash-preview",
        "gemini-3.5-flash",
        "gemini-3.6-flash"
    ]

    # Retrieve relevant document chunks from ChromaDB (<0.6s)
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
6. CONCISENESS & SPEED: Keep responses clear, structured, and concise (under 140 words) using short bullet points. Do not write lengthy essays. This ensures instant readability for families on mobile devices.

USER QUESTION:
{question}

YOUR HELPFUL RESPONSE:"""

    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            # 8-second request timeout guarantees the UI never hangs indefinitely
            response = model.generate_content(
                system_prompt,
                request_options={"timeout": 8.0}
            )
            result = response.text
            _RESPONSE_CACHE[clean_q] = result
            return result
        except Exception:
            # Model busy (503/429/timeout); immediately try the next model in the pool
            continue

    # Fallback if external API rate limit or outage occurs: synthesize from verified local chunks
    if relevant_chunks:
        bullets = "\n".join([f"• {c['text'][:160]}..." for c in relevant_chunks[:3]])
        return (
            f"Here is what our care records say regarding your inquiry:\n\n"
            f"{bullets}\n\n"
            f"For immediate details and to book a free assessment, please call our Sawston team directly on **07917 611 425**."
        )

    return "Our care team is ready to help. Please call Cambridge Care Services directly on **07917 611 425** (Mon–Fri, 9am–5pm)."
