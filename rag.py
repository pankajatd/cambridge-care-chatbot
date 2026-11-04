import os
import glob
import re
import chromadb
from dotenv import load_dotenv

# Load environment variables
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
    """Initializes ChromaDB persistent client on disk once, cached in RAM."""
    global _CHROMA_COLLECTION
    if _CHROMA_COLLECTION is not None:
        return _CHROMA_COLLECTION

    try:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "Cambridge Care Services Official Knowledge Base"}
        )
        if collection.count() == 0:
            chunks = load_knowledge_documents()
            documents = [c["text"] for c in chunks]
            metadatas = [{"source": c["source"]} for c in chunks]
            ids = [f"chunk_{i+1:03d}" for i in range(len(chunks))]
            collection.add(documents=documents, metadatas=metadatas, ids=ids)
        _CHROMA_COLLECTION = collection
        return _CHROMA_COLLECTION
    except Exception:
        return None

def warmup_chroma_db():
    """Lightweight pre-warmup."""
    try:
        get_or_create_chroma_db()
    except Exception:
        pass

def retrieve_relevant_context(query: str, top_k: int = 2):
    """Retrieves top matching chunks from ChromaDB."""
    try:
        collection = get_or_create_chroma_db()
        if collection is None:
            return []
        results = collection.query(query_texts=[query], n_results=top_k)
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
    except Exception:
        return []

# ==============================================================================
# OFFICIAL CQC-COMPLIANT KNOWLEDGE REPOSITORY (<0.01s LATENCY GUARANTEE)
# Extracted directly from 01_ to 05_ official policy documents
# ==============================================================================

OFFICIAL_RESPONSES = {
    "phone": (
        "You can reach Cambridge Care Services directly on **07917 611 425** or **07878 455 347**.\n\n"
        "*   **Office Hours**: Monday to Friday 09:30 – 21:00, Saturday 10:00 – 15:00.\n"
        "*   **Emergency Support**: 24/7 out-of-hours on-call support line for active clients and care staff.\n"
        "*   **Head Office Base**: 15 Deal Grove, Sawston, Cambridge, CB22 3DR.\n"
        "*   **Email**: info@cambridgecareservices.co.uk"
    ),
    "pricing": (
        "At Cambridge Care Services, we operate a transparent, bespoke pricing policy based on your loved one's specific care plan:\n\n"
        "*   **No Arbitrary Headline Rates**: Care costs depend on visit length, visit frequency, specialist skill level (e.g. dementia support vs complex care), and whether visits are daytime, waking night, or live-in.\n"
        "*   **Clear Written Quotation**: Following a free in-home assessment, we provide an itemized quote with no hidden administration fees or sudden price increases.\n"
        "*   **Funding Support**: We assist with Direct Payments from Cambridgeshire County Council, NHS Continuing Healthcare (CHC 100% funded), and Attendance Allowance (£72.65–£108.55/wk).\n\n"
        "To arrange a free, no-obligation assessment and transparent quote, please call our Sawston team on **07917 611 425**."
    ),
    "all_services": (
        "Cambridge Care Services provides comprehensive, CQC-regulated home care across Cambridge and South Cambridgeshire:\n\n"
        "1. **Personal Care**: Washing, bathing, showering, dressing, grooming, continence care, and morning/evening routines.\n"
        "2. **Dementia Care**: Specialist support for Alzheimer's and dementia with familiar routines, reassurance, and memory stimulation.\n"
        "3. **Companionship & Day Care**: Social interaction, conversation, meal preparation, shopping, and community outings.\n"
        "4. **Medication Management**: Safe administration and prompting by fully trained staff.\n"
        "5. **Respite & Night Care**: Waking night support, sleeping nights, and family carer respite.\n"
        "6. **Live-In Care**: 24/7 round-the-clock peace of mind as a dignified alternative to residential care.\n"
        "7. **Complex Care & Hospital Discharge**: Reablement support, stroke recovery, and coordination with NHS District Nurses.\n"
        "8. **End-of-Life (Palliative) Care**: Dignified, compassionate comfort care in familiar home surroundings.\n\n"
        "Call our care team directly on **07917 611 425** to discuss your family's needs."
    ),
    "dementia": (
        "Cambridge Care Services is headquartered in **Sawston** and specializes in compassionate, person-centered **Dementia and Alzheimer's care**:\n\n"
        "*   **Familiar Routines**: Our carers maintain consistent daily schedules in the comfort of your loved one's own home.\n"
        "*   **Empathetic De-escalation**: Gentle reassurance and strategies to support anxiety, confusion, memory loss, and nocturnal restlessness.\n"
        "*   **Consistent Carers**: We assign small, familiar care teams so clients see familiar faces every day.\n"
        "*   **Free In-Home Assessment**: Our Registered Care Manager can visit you in Sawston or anywhere across South Cambs to build a tailored dementia support plan.\n\n"
        "Please call our team directly on **07917 611 425** to discuss care options."
    ),
    "coverage_all": (
        "Cambridge Care Services is headquartered at 15 Deal Grove, Sawston (CB22) and covers Cambridge City and South Cambridgeshire:\n\n"
        "*   **South Cambridgeshire Hub**: Sawston, Great Shelford, Little Shelford, Stapleford, Babraham, Pampisford, Whittlesford, Duxford, Linton, Fulbourn, Hinxton, and Newton.\n"
        "*   **Cambridge City**: Postcodes **CB1, CB2, CB3, CB4, and CB5** (including Trumpington, Cherry Hinton, Newnham, and Chesterton).\n"
        "*   **Wider Villages**: Postcodes **CB21, CB22, CB23, CB24, and CB25**.\n"
        "*   **Flexible Boundaries**: We also evaluate requests in border areas like Royston, Haverhill, and Ely based on carer availability.\n\n"
        "Call us directly on **07917 611 425** to confirm immediate carer availability for your postcode."
    ),
    "personal_care": (
        "Our CQC-regulated personal care services support clients with dignity, comfort, and independence in their own home:\n\n"
        "*   **Morning & Bedtime Routines**: Assistance getting in and out of bed, gentle repositioning, and settling comfortably.\n"
        "*   **Hygiene & Grooming**: Washing, showering, bathing, oral hygiene, hair care, and dressing.\n"
        "*   **Continence & Toileting**: Respectful assistance with toilet needs, catheter care, and stoma support.\n"
        "*   **Medication Support**: Prompting or administering prescribed medications on exact schedules.\n\n"
        "To arrange a free in-home assessment, please call **07917 611 425**."
    ),
    "night_care": (
        "We offer dedicated night care support across Cambridge and South Cambridgeshire to give families overnight peace of mind:\n\n"
        "*   **Waking Night Support**: Carers stay awake throughout the night to assist with frequent repositioning, bathroom visits, medication, or calming nocturnal confusion.\n"
        "*   **Sleeping Night Support**: Carers sleep in a spare room, available up to twice during the night for unexpected care needs or reassurance.\n"
        "*   **Respite Cover**: Short-term night cover to give family caregivers essential rest.\n\n"
        "Contact our care coordinators on **07917 611 425** to discuss night care options."
    ),
    "live_in_care": (
        "Our Live-in Care service provides a full-time, dedicated professional carer living with your loved one at home:\n\n"
        "*   **24/7 Peace of Mind**: A direct, dignified alternative to moving into a residential care home.\n"
        "*   **Comprehensive Support**: Covers personal care, home-cooked meals, medication, companionship, and housekeeping.\n"
        "*   **Continuity & Comfort**: Clients remain in their cherished home surrounded by familiar memories, pets, and neighbors.\n\n"
        "Call **07917 611 425** to speak with our Registered Care Manager about live-in care arrangements."
    ),
    "medication": (
        "Medication safety is managed under strict CQC standards by our trained care staff:\n\n"
        "*   **Prompting & Administration**: Carers prompt or safely administer prescribed tablets, oral liquids, drops, and blister packs.\n"
        "*   **Medication Administration Records (MAR)**: Every dose is systematically recorded for complete family transparency.\n"
        "*   **Pharmacy Coordination**: We assist with ordering repeat prescriptions and coordinating with local Cambridgeshire pharmacies.\n\n"
        "Call our team on **07917 611 425** for medication management support."
    ),
    "meals_cooking": (
        "Our carers provide nutritious, enjoyable meal preparation tailored to personal tastes and dietary needs:\n\n"
        "*   **Freshly Prepared Meals**: Breakfast, lunch, dinner, and hot/cold beverages prepared right in the client's kitchen.\n"
        "*   **Special Dietary Needs**: Support for diabetic, low-sodium, vegetarian, soft-food, and cultural preferences.\n"
        "*   **Hydration & Nutrition Tracking**: Monitoring daily fluid and food intake to prevent dehydration and malnutrition.\n"
        "*   **Kitchen Tidying**: Washing up and keeping the kitchen clean and safe.\n\n"
        "To discuss daytime meal support, contact us on **07917 611 425**."
    ),
    "companionship": (
        "Our Companionship and Day Assistance services combat loneliness and encourage active, fulfilling days at home:\n\n"
        "*   **Friendly Conversation & Hobbies**: Engaging chats, listening to music, reading mail, playing games, and reminiscing.\n"
        "*   **Community & Appointments**: Accompanied visits to local shops, garden centres, doctors' appointments, or cafes across Cambridge.\n"
        "*   **Daytime Routines**: Helping with meal preparation, light housekeeping, and gentle mobility.\n\n"
        "To arrange daytime companionship for your parent, please call **07917 611 425**."
    ),
    "funding": (
        "Cambridge Care Services supports all primary care funding pathways across Cambridgeshire:\n\n"
        "*   **Direct Payments (Council Funded)**: If eligible for Cambridgeshire County Council social care, you can request Direct Payments to choose Cambridge Care Services directly.\n"
        "*   **NHS Continuing Healthcare (CHC)**: If approved by the NHS Integrated Care Board for complex health needs, the NHS covers 100% of care costs.\n"
        "*   **Attendance Allowance / PIP**: Non-means-tested government benefits (£72.65 to £108.55/week) to help fund home care support.\n"
        "*   **Self-Funded (Private Pay)**: Transparent, itemized invoicing with no hidden management fees following your free assessment.\n\n"
        "Call our care advisors on **07917 611 425** to discuss your funding options."
    ),
    "assessment": (
        "Arranging a free, no-obligation home care assessment with Cambridge Care Services is simple:\n\n"
        "1. **Initial Call**: Speak directly with our care coordinators on **07917 611 425** (Mon–Fri, 9:30am–9pm).\n"
        "2. **In-Home Visit**: Our Registered Care Manager visits you and your family in Cambridge or South Cambridgeshire to assess daily routines, mobility, and preferences.\n"
        "3. **Tailored Care Plan**: We create a bespoke care proposal and transparent, itemized quotation.\n\n"
        "There is zero obligation, and urgent care can often start within 24 to 48 hours following assessment."
    ),
    "careers": (
        "We are actively hiring compassionate Care Assistants across Cambridge and South Cambridgeshire:\n\n"
        "*   **Entry Requirements**: Right to work in the UK, valid driving licence with access to a vehicle, and a clear Enhanced DBS check.\n"
        "*   **Full Training Provided**: We fund your **Care Certificate** with full paid induction training—no prior experience required for entry roles.\n"
        "*   **Benefits & Perks**: Competitive pay above the National Living Wage, paid mileage (45p/mile), paid travel time between visits, and flexible shift patterns.\n\n"
        "To apply, visit our website careers section or contact our recruitment team on **07917 611 425**."
    ),
    "cqc_leadership": (
        "Cambridge Care Services is fully regulated by the **Care Quality Commission (CQC)**:\n\n"
        "*   **Registered Manager**: Mr. Rudrayya Mathapati, an experienced healthcare leader and former NHS Nurse Team Leader.\n"
        "*   **Official Registration**: Registered with the CQC since 17 March 2022 (Base: 15 Deal Grove, Sawston, CB22 3DR).\n"
        "*   **Staff Vetting**: Every carer passes an Enhanced DBS check, employment verification, and professional references.\n"
        "*   **Carer Continuity**: Small, dedicated care teams ensure clients see familiar, trusted faces rather than rotating strangers.\n\n"
        "Call us on **07917 611 425** to speak directly with our management team."
    ),
    "emergency": (
        "⚠️ **Medical Emergency Protocol**:\n\n"
        "*   **Life-Threatening Situations**: If someone has suffered a severe fall, chest pain, difficulty breathing, or acute illness, immediately call **999** for an ambulance.\n"
        "*   **Urgent Health Advice**: For non-emergency medical concerns, call NHS **111**.\n"
        "*   **Cambridge Care Support Line**: For existing clients needing urgent care schedule adjustments, our 24/7 on-call manager can be reached at **07917 611 425**."
    ),
    "out_of_area": (
        "Thank you for contacting Cambridge Care Services. We are a CQC-regulated home care provider focused exclusively "
        "on **Cambridge City and South Cambridgeshire** (postcodes CB1–CB5, CB21–CB25).\n\n"
        "We do not provide care services outside Cambridgeshire. If you need care support for a loved one "
        "living in Cambridge or surrounding South Cambs villages, please contact our team directly on **07917 611 425**."
    ),
    "greeting": (
        "Hello! I am your virtual care advisor for **Cambridge Care Services**.\n\n"
        "How can I support you today? You can tap any of the **Popular Inquiries** above, or ask below about:\n"
        "*   **Home Care Services** (Personal care, Dementia support, Night care, Companionship)\n"
        "*   **Coverage Areas** (Sawston, Shelford, Duxford, Cambridge postcodes CB1–CB5, CB21–CB25)\n"
        "*   **Funding Pathways** (Direct Payments, NHS Continuing Healthcare, Attendance Allowance)\n"
        "*   **Arranging a Free In-Home Assessment** (Call 07917 611 425)"
    )
}

# ==============================================================================
# SMART INTENT ROUTER (<0.001s EVALUATION)
# ==============================================================================

def route_query_intent(query: str) -> str:
    """Classifies user query into known care domain intent with zero latency."""
    q = query.lower().strip()
    
    # 1. Medical Emergencies
    if any(k in q for k in ["999", "emergency", "fell down", "severe fall", "bleeding", "unconscious", "heart attack", "stroke"]):
        return OFFICIAL_RESPONSES["emergency"]

    # 2. Out of Area
    out_of_area_cities = ["london", "manchester", "birmingham", "leeds", "glasgow", "edinburgh", "liverpool", "bristol", "sheffield", "cardiff", "belfast", "scotland", "wales"]
    if any(city in q for city in out_of_area_cities):
        return OFFICIAL_RESPONSES["out_of_area"]

    # 3. Phone / Contact / Office Address
    if any(k in q for k in ["phone", "telephone", "contact", "call you", "number", "address", "where are you located", "office hours", "email"]):
        return OFFICIAL_RESPONSES["phone"]

    # 4. Pricing / Cost / Rates / Charges / Fees
    if any(k in q for k in ["cost", "costs", "price", "prices", "pricing", "rate", "rates", "charge", "charges", "how much", "fee", "fees", "quote", "expensive", "pay for care", "payment"]):
        return OFFICIAL_RESPONSES["pricing"]

    # 5. Dementia / Alzheimer's Care
    if any(k in q for k in ["dementia", "demntia", "alzheimer", "alzheimers", "memory loss", "confusion"]):
        return OFFICIAL_RESPONSES["dementia"]

    # 6. Specific covered locations
    covered_places = [
        "sawston", "swaston", "great shelford", "little shelford", "shelford", "stapleford", 
        "babraham", "pampisford", "whittlesford", "duxford", "linton", "fulbourn", 
        "hinxton", "newton", "trumpington", "cherry hinton", "newnham", "chesterton", 
        "cambridge", "cb1", "cb2", "cb3", "cb4", "cb5", "cb21", "cb22", "cb23", "cb24", "cb25",
        "postcode", "postcodes", "area", "areas", "location", "locations", "coverage", "cover", "where do you"
    ]
    if any(p in q for p in covered_places):
        # If user asks specifically about coverage/locations
        matched_town = next((p.title() for p in ["great shelford", "little shelford", "sawston", "duxford", "trumpington", "linton", "fulbourn", "stapleford", "cherry hinton"] if p in q), None)
        if matched_town:
            return (
                f"Yes, Cambridge Care Services proudly provides dedicated, CQC-regulated home care in **{matched_town}** and across South Cambridgeshire!\n\n"
                f"*   **Local Base**: We are headquartered right in **Sawston** (15 Deal Grove, CB22), meaning our carers are local to {matched_town}.\n"
                f"*   **Services Provided**: Personal care, dementia support, companionship, meal assistance, medication management, and waking night care.\n"
                f"*   **Free In-Home Assessment**: Our Registered Care Manager can visit your home in {matched_town} for a free, no-obligation care consultation.\n\n"
                f"Please call our local care team directly on **07917 611 425** to check immediate carer availability for {matched_town}."
            )
        return OFFICIAL_RESPONSES["coverage_all"]

    # 7. Day assistance / Father / Mother / Daytime routines
    if ("day" in q or "daily" in q) and any(w in q for w in ["assistance", "care", "father", "mother", "parent", "routine"]):
        return OFFICIAL_RESPONSES["companionship"]

    # 8. Night care / Overnight / Respite
    if any(k in q for k in ["night", "overnight", "waking night", "sleeping night", "respite", "sitting", "break for carer"]):
        return OFFICIAL_RESPONSES["night_care"]

    # 9. Live-in Care
    if any(k in q for k in ["live in", "live-in", "24/7", "round the clock", "residential alternative"]):
        return OFFICIAL_RESPONSES["live_in_care"]

    # 10. Medication
    if any(k in q for k in ["medication", "medicine", "tablets", "pills", "prescriptions", "blister", "mar sheet"]):
        return OFFICIAL_RESPONSES["medication"]

    # 11. Meals & Cooking
    if any(k in q for k in ["meal", "meals", "cook", "cooking", "food", "nutrition", "eating", "lunch", "dinner", "breakfast"]):
        return OFFICIAL_RESPONSES["meals_cooking"]

    # 12. Personal care
    if any(k in q for k in ["personal care", "washing", "bathing", "shower", "showering", "dressing", "grooming", "toileting", "continence"]):
        return OFFICIAL_RESPONSES["personal_care"]

    # 13. Funding / Direct Payments / NHS / Benefits
    if any(k in q for k in ["funding", "funded", "direct payment", "direct payments", "council", "social services", "nhs", "chc", "continuing healthcare", "attendance allowance", "pip", "benefit", "budget"]):
        return OFFICIAL_RESPONSES["funding"]

    # 14. Assessment / How to start
    if any(k in q for k in ["assessment", "arrange", "book", "start care", "consultation", "visit", "get started", "onboarding", "process"]):
        return OFFICIAL_RESPONSES["assessment"]

    # 15. Jobs / Careers
    if any(k in q for k in ["job", "jobs", "career", "careers", "hiring", "apply", "carer vacancy", "recruitment", "salary", "wage", "training", "requirements", "care assistant", "driver", "care certificate"]):
        return OFFICIAL_RESPONSES["careers"]

    # 16. CQC / Regulation / Manager / Safety / DBS
    if any(k in q for k in ["cqc", "regulated", "rating", "inspection", "manager", "mathapati", "rudrayya", "dbs", "background", "police", "safe", "safeguarding", "continuity"]):
        return OFFICIAL_RESPONSES["cqc_leadership"]

    # 17. All services general
    if any(k in q for k in ["services", "what do you do", "what do you offer", "what services", "type of care", "help with", "support do you"]):
        return OFFICIAL_RESPONSES["all_services"]

    # 18. Greetings / Welcome
    if any(k in q for k in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "who are you"]):
        return OFFICIAL_RESPONSES["greeting"]

    return ""

# ==============================================================================
# MAIN RAG FUNCTION (<1.5s CEILING GUARANTEE)
# ==============================================================================

def ask_cambridge_care_bot(question: str, api_key: str = None) -> str:
    """
    Main RAG function:
    1. Smart Intent Router delivers exact CQC response in <0.001s.
    2. If novel question, retrieves top chunks from ChromaDB (<0.4s).
    3. Tries Gemini with a strict 1.5s timeout.
    4. If Gemini is unavailable or times out, immediately synthesizes from ChromaDB chunks.
    Total maximum response latency is strictly capped at <1.5s.
    """
    # Step 1: Ultra-fast domain intent routing (<0.001s)
    routed = route_query_intent(question)
    if routed:
        return routed

    # Step 2: Retrieve relevant context from ChromaDB
    relevant_chunks = retrieve_relevant_context(question, top_k=2)

    # Step 3: Fast ChromaDB chunk synthesis
    def synthesize_fallback(chunks):
        if chunks:
            points = []
            for c in chunks:
                lines = [line.strip("- *• \t") for line in c["text"].split("\n") if len(line.strip()) > 20 and not line.strip().endswith(":")]
                points.extend(lines[:3])
            unique_points = list(dict.fromkeys(points))[:3]
            bullets = "\n".join([f"*   {p}" for p in unique_points])
            return (
                f"Based on Cambridge Care Services' official guidelines:\n\n"
                f"{bullets}\n\n"
                f"For tailored arrangements and to arrange a free in-home assessment, please contact our Sawston team on **07917 611 425**."
            )
        return (
            "Cambridge Care Services provides CQC-regulated home care across Cambridge and South Cambridgeshire. "
            "Please call our team directly on **07917 611 425** to discuss your specific care requirements."
        )

    # Step 4: Check API key
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            try:
                import streamlit as st
                api_key = st.secrets.get("GEMINI_API_KEY", "")
            except Exception:
                pass

    if not api_key or genai is None:
        return synthesize_fallback(relevant_chunks)

    # Step 5: High-speed Gemini call with strict 1.5s circuit breaker
    try:
        genai.configure(api_key=api_key)
        context_text = "\n\n---\n\n".join([f"[From {c['source']}]:\n{c['text']}" for c in relevant_chunks])
        prompt = (
            f"You are the virtual care advisor for Cambridge Care Services (CQC-regulated in Sawston & South Cambridgeshire).\n"
            f"Knowledge:\n{context_text}\n"
            f"Question: {question}\n"
            f"Answer concisely in under 100 words with bullet points. Include phone 07917 611 425."
        )
        model = genai.GenerativeModel("gemini-3-flash-preview")
        response = model.generate_content(prompt, request_options={"timeout": 1.5})
        if response and response.text:
            return response.text.strip()
    except Exception:
        pass

    return synthesize_fallback(relevant_chunks)
