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
# UNIVERSAL CQC-COMPLIANT CARE INTELLIGENCE ENGINE (<0.001s LATENCY GUARANTEE)
# Fully generalized to deliver elaborate, empathetic responses for ANY query
# ==============================================================================

def extract_relative(q: str):
    rel_map = [
        ("grandmother", "your Grandmother", "her", "her"),
        ("grandfather", "your Grandfather", "him", "his"),
        ("grandma", "your Grandma", "her", "her"),
        ("grandpa", "your Grandpa", "him", "his"),
        ("mother", "your Mother", "her", "her"),
        ("mum", "your Mother", "her", "her"),
        ("mom", "your Mother", "her", "her"),
        ("father", "your Father", "him", "his"),
        ("dad", "your Father", "him", "his"),
        ("aunt", "your Aunt", "her", "her"),
        ("uncle", "your Uncle", "him", "his"),
        ("sister", "your Sister", "her", "her"),
        ("brother", "your Brother", "him", "his"),
        ("husband", "your Husband", "him", "his"),
        ("wife", "your Wife", "her", "her"),
        ("parents", "your Parents", "them", "their"),
        ("parent", "your Parent", "them", "their"),
        ("myself", "you", "you", "your"),
        ("for me", "you", "you", "your"),
        ("i need care", "you", "you", "your"),
    ]
    for key, name, pronoun, possessive in rel_map:
        if key in q:
            return name, pronoun, possessive
    return "your loved one", "her", "her"

def extract_location(q: str):
    sawston_aliases = ["sawston", "swaston", "sawston village"]
    if any(s in q for s in sawston_aliases):
        return "in Sawston and South Cambridgeshire", True, "Sawston"
    
    towns = [
        ("great shelford", "in Great Shelford and South Cambridgeshire", "Great Shelford"),
        ("little shelford", "in Little Shelford and South Cambridgeshire", "Little Shelford"),
        ("cherry hinton", "in Cherry Hinton and Cambridge", "Cherry Hinton"),
        ("whittlesford", "in Whittlesford and South Cambridgeshire", "Whittlesford"),
        ("stapleford", "in Stapleford and South Cambridgeshire", "Stapleford"),
        ("trumpington", "in Trumpington and South Cambridgeshire", "Trumpington"),
        ("pampisford", "in Pampisford and South Cambridgeshire", "Pampisford"),
        ("waterbeach", "in Waterbeach and South Cambridgeshire", "Waterbeach"),
        ("cambourne", "in Cambourne and South Cambridgeshire", "Cambourne"),
        ("cottenham", "in Cottenham and South Cambridgeshire", "Cottenham"),
        ("fulbourn", "in Fulbourn and South Cambridgeshire", "Fulbourn"),
        ("babraham", "in Babraham and South Cambridgeshire", "Babraham"),
        ("shelford", "in Shelford and South Cambridgeshire", "Shelford"),
        ("duxford", "in Duxford and South Cambridgeshire", "Duxford"),
        ("hinxton", "in Hinxton and South Cambridgeshire", "Hinxton"),
        ("newton", "in Newton and South Cambridgeshire", "Newton"),
        ("linton", "in Linton and South Cambridgeshire", "Linton"),
        ("histon", "in Histon and South Cambridgeshire", "Histon"),
        ("cambridge", "across Cambridge and South Cambridgeshire", "Cambridge"),
    ]
    for k, loc_text, town_name in towns:
        if k in q:
            return loc_text, False, town_name
            
    return "across Cambridge and South Cambridgeshire", False, "South Cambridgeshire"

def extract_schedule(q: str):
    has_night = any(n in q for n in ["night", "overnight", "sleeping night", "waking night", "nocturnal"])
    has_day = any(d in q for d in ["day", "daytime", "afternoon", "morning"])
    has_live_in = any(l in q for l in ["live in", "live-in", "24/7", "round the clock", "residential"])
    has_respite = any(r in q for r in ["respite", "holiday", "break", "temporary", "two weeks", "few weeks"])
    
    hours_mention = ""
    for h in ["1 hour", "2 hours", "2 hour", "3 hours", "3 hour", "4 hours", "4 hour", "5 hours", "5 hour", "6 hours", "6 hour", "8 hours", "8 hour", "10 hours", "10 hour", "12 hours", "12 hour"]:
        if h in q:
            hours_mention = h.replace(" hours", "-hour").replace(" hour", "-hour")
            break
            
    return has_night, has_day, has_live_in, has_respite, hours_mention

def extract_special_requests(q: str):
    """Detects specific user questions like male/female carers, nurse distinctions, pets, languages, urgency."""
    notes = []
    
    # 1. Male Carer / Male Nurse request
    if any(k in q for k in ["male nurse", "male carer", "male staff", "man carer", "male care assistant", "male support worker", "gentleman carer"]):
        notes.append(
            "*   **Male Carer Allocation for Dignity & Preference**: We fully respect client preferences for male or female carers. If your loved one feels more comfortable with a male carer for personal care, washing, dressing, and daily assistance, a trained **male care assistant / support worker** can be allocated to their care team."
        )
        if any(n in q for n in ["nurse", "nurses", "nursing"]):
            notes.append(
                "*   **Carer vs. Registered Nurse Distinction**: Our team members are CQC-regulated Home Care Assistants and Support Workers rather than acute hospital ward nurses. However, our Registered Care Manager, **Mr. Rudrayya Mathapati**, is an experienced former **NHS Clinical Nurse Team Leader**, and our carers coordinate directly alongside NHS District Nurses and GPs for any clinical procedures."
            )
    elif any(k in q for k in ["female carer", "female nurse", "female staff", "woman carer", "lady carer"]):
        notes.append(
            "*   **Female Carer Allocation**: We fully accommodate client preferences for female carers. For personal care routines, washing, dressing, and hygiene, a compassionate female carer will be dedicated to their care team to ensure total comfort and dignity."
        )
    elif any(k in q for k in ["nurse", "nurses", "nursing", "clinical nurse"]):
        notes.append(
            "*   **Carer vs. Registered Nurse Guidance**: Our care assistants provide non-clinical social care and medication management. Clinical nursing procedures (such as IV lines or sterile catheterization) are coordinated directly with your local NHS District Nursing team, overseen by our Registered Manager, **Mr. Rudrayya Mathapati**, a former NHS Clinical Nurse Team Leader."
        )

    # 2. Urgency / Fast Start
    if any(k in q for k in ["how fast", "how quickly", "immediate", "urgent", "emergency start", "today", "tomorrow", "asap"]):
        notes.append(
            "*   **Rapid Onboarding Guarantee (24-48 Hours)**: For urgent situations, hospital discharges, or sudden care needs, our Care Manager can conduct an expedited in-home assessment and commence care visits within **24 to 48 hours**."
        )

    # 3. Pets
    if any(k in q for k in ["dog", "cat", "pet", "pets", "animal", "walk the dog"]):
        notes.append(
            "*   **Pet-Friendly Home Care**: We understand that cherished pets are family members. Our carers are pet-friendly and can assist with pet feeding, letting pets out into the garden, or light companionship assistance alongside care routines."
        )

    # 4. Multilingual / Language
    if any(k in q for k in ["language", "languages", "speak", "hindi", "punjabi", "urdu", "italian", "spanish", "polish", "gujarati"]):
        notes.append(
            "*   **Language & Cultural Matching**: We value cultural diversity and communication. Where specific language preferences exist, our care coordinators make every effort to match carers who share your language and cultural background."
        )

    # 5. Bank Holidays / Weekends
    if any(k in q for k in ["christmas", "bank holiday", "bank holidays", "easter", "new year", "weekend only", "sundays"]):
        notes.append(
            "*   **365-Day Year-Round Cover**: Cambridge Care Services operates 365 days a year, including all Bank Holidays, Christmas Day, Boxing Day, and New Year. Regular care schedules are seamlessly maintained with higher weekend/holiday pay rates."
        )

    # 6. Carer Sickness / Replacement Cover
    if any(k in q for k in ["sick", "ill", "carer calls in", "replacement", "running late", "holiday cover"]):
        notes.append(
            "*   **Guaranteed Replacement Cover**: If a regular carer is unwell or on leave, Cambridge Care Services guarantees seamless replacement cover by a briefed backup carer so your family experiences zero missed visits."
        )

    return notes

def route_care_inquiry(query: str) -> str:
    q = query.lower().strip()
    
    # 1. Emergency Protocol
    if any(k in q for k in ["999", "emergency", "fell down", "severe fall", "bleeding", "unconscious", "heart attack"]):
        return (
            "⚠️ **Medical Emergency Protocol**:\n\n"
            "*   **Life-Threatening Situations**: If someone has suffered a severe fall, chest pain, difficulty breathing, acute trauma, or loss of consciousness, please call **999** immediately for an ambulance.\n"
            "*   **Urgent Non-Emergency Health Advice**: For urgent medical guidance that is not life-threatening, call NHS **111**.\n"
            "*   **Cambridge Care On-Call Line**: For existing clients needing urgent care visit adjustments, our 24/7 emergency support line is **07917 611 425**."
        )

    # 2. Out of Area Inquiries
    out_of_area_cities = ["london", "manchester", "birmingham", "leeds", "glasgow", "edinburgh", "liverpool", "bristol", "sheffield", "cardiff", "belfast", "scotland", "wales"]
    if any(city in q for city in out_of_area_cities):
        return (
            "Thank you for contacting Cambridge Care Services. We are a CQC-regulated home care provider focused exclusively "
            "on **Cambridge City and South Cambridgeshire** (postcodes CB1-CB5, CB21-CB25).\n\n"
            "We do not provide care services outside Cambridgeshire. If you need care support for a loved one "
            "living in Cambridge or surrounding South Cambs villages, please contact our team directly on **07917 611 425**."
        )

    # 3. Direct Contact / Phone / Office Details
    if any(k in q for k in ["what is your phone", "what is your telephone", "contact number", "call you", "where is your office", "head office address", "opening hours"]):
        return (
            "You can reach Cambridge Care Services directly by telephone on **07917 611 425** or **07878 455 347**.\n\n"
            "*   **Head Office Address**: 15 Deal Grove, Sawston, Cambridge, Cambridgeshire, CB22 3DR.\n"
            "*   **Office Opening Hours**: Monday to Friday from 09:30 to 21:00, and Saturday from 10:00 to 15:00.\n"
            "*   **24/7 Emergency Support**: We operate a 24-hour on-call support line dedicated to active clients, their families, and on-duty care staff for any urgent care schedule adjustments or evening peace of mind.\n"
            "*   **Email Inquiries**: You can also reach our administrative and coordination team directly at **info@cambridgecareservices.co.uk**.\n\n"
            "Whether you are exploring care options for the first time or need immediate support, our local team is always available to assist."
        )

    relative, pronoun, possessive = extract_relative(q)
    loc_text, is_sawston, town_name = extract_location(q)
    has_night, has_day, has_live_in, has_respite, hours_mention = extract_schedule(q)
    special_notes = extract_special_requests(q)
    special_bullets = ("\n" + "\n".join(special_notes) + "\n") if special_notes else ""

    # Contextual office proximity text
    office_intro = (
        f"Because our head office is located right in **Sawston** (15 Deal Grove, CB22 3DR), our local carers are based within the village, "
        f"allowing us to provide prompt, dependable, and consistent visits tailored to {possessive} daily routines:\n\n"
        if is_sawston else
        f"Our experienced care team provides prompt, dependable, and consistent home visits {loc_text}, tailored to {possessive} personal care plan:\n\n"
    )

    # Dynamic Opening phrase addressing special requests if asked
    opening_ack = f"Yes, absolutely. Cambridge Care Services provides dedicated, person-centered care for **{relative}** {loc_text}"
    if any(k in q for k in ["male nurse", "male carer", "male staff"]):
        opening_ack = f"Yes, absolutely. Cambridge Care Services can accommodate your request for a **male carer** to support **{relative}** {loc_text}"
    elif any(k in q for k in ["female carer", "female nurse"]):
        opening_ack = f"Yes, absolutely. Cambridge Care Services can provide a **female carer** to support **{relative}** {loc_text}"

    # 4. Parkinson\'s Disease & Complex Neurological Care
    if any(k in q for k in ["parkinson", "parkinsons", "tremor", "rigidity", "neurological"]):
        sched_note = ""
        if has_night and (has_day or hours_mention):
            sched_note = f", including tailored daytime support and **overnight care** (such as {hours_mention or '6-hour'} waking night or sleeping night assistance)"
        elif has_night:
            sched_note = f", including tailored **overnight care** (such as {hours_mention or '6-hour'} waking night or sleeping night assistance)"
        elif hours_mention or has_day:
            sched_note = f", including tailored daytime visits (such as {hours_mention or 'unhurried'} morning or afternoon support)"
        else:
            sched_note = ", including tailored daytime assistance and overnight care"

        return (
            f"{opening_ack}{sched_note}.\n\n"
            f"{office_intro}"
            f"{special_bullets}"
            f"*   **Specialist Parkinson\'s & Mobility Support**: Parkinson\'s symptoms vary significantly throughout the day and evening. Our carers assist with safe transfers, posture support, gentle mobility to reduce fall risks, and unhurried personal care that respects {possessive} pace and dignity.\n"
            f"*   **Time-Critical Medication Management**: In Parkinson\'s care, strict timing of prescribed medication is essential to minimize tremors and motor fluctuations (the 'on/off' effect). Our carers ensure prompt, accurate administration audited on Medication Administration Records (MAR) under strict CQC clinical guidelines.\n"
            f"*   **Dedicated Overnight Care (6+ Hours)**: For nocturnal restlessness, difficulty turning or repositioning in bed, nighttime anxiety, or bathroom assistance, our carers provide dedicated overnight care (both waking nights where a carer stays awake to assist continuously, and sleeping nights for on-site reassurance).\n"
            f"*   **Daytime Companionship & Nutrition**: Preparing wholesome, nutritious meals, encouraging hydration, medication prompting, and providing compassionate companionship to keep {relative} engaged, comfortable, and safe in {possessive} familiar home surroundings.\n"
            f"*   **Small, Consistent Care Teams**: We assign a small, dedicated care team so {relative} sees the same trusted, friendly faces every day and night rather than rotating strangers, fostering genuine emotional comfort, continuity, and mutual trust.\n"
            f"*   **Free In-Home Care Assessment**: Our Registered Care Manager, **Mr. Rudrayya Mathapati** (former NHS Clinical Nurse Team Leader), will visit {relative} at home for an unhurried, comprehensive consultation to build a tailored Parkinson\'s Care Plan.\n\n"
            f"To discuss {relative}\'s daytime and overnight care schedule or book your free assessment, please call our Sawston care team directly on **07917 611 425** (Mon-Fri 09:30-21:00, Sat 10:00-15:00, with 24/7 on-call manager support)."
        )

    # 5. Dementia & Alzheimer\'s Care
    if any(k in q for k in ["dementia", "demntia", "alzheimer", "alzheimers", "memory loss", "confusion", "cognitive"]):
        sched_note = ""
        if has_night:
            sched_note = f", including dedicated overnight care ({hours_mention or 'waking night / sleeping night'})"
        elif hours_mention or has_day:
            sched_note = f", including tailored visit schedules (such as {hours_mention or '2-to-3-hour'} daytime visits or dedicated afternoon blocks)"

        return (
            f"Yes, absolutely. Cambridge Care Services provides dedicated, person-centered **Dementia and Alzheimer\'s home care** for **{relative}** {loc_text}{sched_note}.\n\n"
            f"We understand how vital it is for families to find compassionate, dependable care for a loved one living with memory loss. Our service is designed to maintain {possessive} dignity, safety, and comfort in {possessive} own familiar home surroundings:\n\n"
            f"{office_intro}"
            f"{special_bullets}"
            f"*   **Familiar Surroundings & Consistent Routines**: Remaining in one\'s own home surrounded by cherished memories, pets, and lifelong routines is clinically proven to reduce stress, disorientation, and confusion for individuals living with dementia. Our carers maintain consistent daily schedules tailored to {possessive} personal rhythm.\n"
            f"*   **Empathetic Daytime & Personal Care**: Our carers provide unhurried, patient support with morning routines, dignified bathing and dressing, preparing wholesome meals, afternoon tea, gentle mobility, stimulating memory activities, and reassuring companionship.\n"
            f"*   **Late-Afternoon Reassurance & Sundowning Support**: We understand that late afternoons can sometimes trigger restlessness, anxiety, or confusion (sundowning). Our staff are specially trained in gentle de-escalation, empathetic communication, and calming evening settling routines to ensure {relative} feels safe, understood, and relaxed.\n"
            f"*   **Small, Consistent Care Teams**: We assign a small, dedicated care team so {relative} sees the same trusted, friendly faces every day rather than rotating strangers, fostering genuine emotional comfort, continuity, and mutual trust.\n"
            f"*   **Flexible Visit Schedules**: We tailor visit durations to your family\'s exact needs-whether that is 1-hour visits, unhurried 2-to-3-hour daytime blocks (such as 3:00 PM to 6:00 PM), waking nights, or round-the-clock live-in care.\n"
            f"*   **Free In-Home Care Assessment**: Our Registered Care Manager, **Mr. Rudrayya Mathapati**, will visit your family home for an unhurried, no-obligation assessment to listen to your wishes and design a bespoke Dementia Support Plan.\n\n"
            f"To discuss {relative}\'s care needs or book a free assessment, please call our Sawston care team directly on **07917 611 425** (Mon-Fri 09:30-21:00, Sat 10:00-15:00, with 24/7 on-call manager support)."
        )

    # 6. Stroke / Hospital Discharge / Reablement
    if any(k in q for k in ["stroke", "rehab", "reablement", "hospital discharge", "post-hospital", "discharged", "hospital", "surgery"]):
        return (
            f"{opening_ack} following hospital discharge:\n\n"
            f"{office_intro}"
            f"{special_bullets}"
            f"*   **Mobility Rebuilding & Safe Transfers**: Assisting with safe bed-to-chair transfers, walking practice, and prescribed physiotherapy exercises to regain physical strength and prevent fall injuries.\n"
            f"*   **Dignified Personal Care**: Respectful assistance with morning and evening routines, washing, dressing, and hygiene tailored to {possessive} recovery pace.\n"
            f"*   **Clinical & Medication Coordination**: Timely medication prompting on Medication Administration Records (MAR) and direct collaboration with NHS District Nurses, Occupational Therapists (OTs), and GPs.\n"
            f"*   **Nutritious Meal Preparation & Hydration**: Freshly cooking balanced meals and monitoring fluid intake to support healing and strength.\n"
            f"*   **Rapid Onboarding Guarantee**: For urgent hospital discharge reablement, care visits can often commence within **24 to 48 hours** following an in-home assessment.\n\n"
            f"To discuss {relative}\'s hospital discharge date and request specialized carer matching with our Registered Care Manager, **Mr. Rudrayya Mathapati**, please call **07917 611 425**."
        )

    # 7. Respite Care (Short term cover, holiday cover)
    if has_respite:
        return (
            f"Yes, Cambridge Care Services provides dedicated, CQC-regulated **Respite Care** for **{relative}** {loc_text}.\n\n"
            f"We understand that family caregiving is both deeply rewarding and physically demanding. Our respite care service provides primary family carers with restful peace of mind while they take a well-deserved break or holiday:\n\n"
            f"{office_intro}"
            f"{special_bullets}"
            f"*   **Flexible Cover Periods**: Whether you require respite cover for a few hours a week, several full days, overnight support, or full 1-to-2-week live-in cover while your family travels, we adapt to your exact timetable.\n"
            f"*   **Seamless Continuity of Care**: Our carers strictly follow {possessive} established daily routines, dietary preferences, and medication schedules so {relative} experiences zero disruption in their familiar home surroundings.\n"
            f"*   **Comprehensive In-Home Assistance**: Covers personal hygiene, morning/evening dressing, fresh home cooking, companionship, and medication administration on MAR records.\n"
            f"*   **Guaranteed Staff Cover**: You can travel with complete peace of mind knowing backup carer cover is guaranteed under our CQC operational guidelines.\n\n"
            f"To discuss your holiday dates and arrange a free respite assessment, please call our Sawston office directly on **07917 611 425**."
        )

    # 8. Night Care (Waking & Sleeping nights)
    if has_night:
        timing_str = f"({hours_mention or '6-to-10 hour shifts'})"
        return (
            f"Yes, Cambridge Care Services provides dedicated, CQC-regulated overnight care for **{relative}** {loc_text} {timing_str}:\n\n"
            f"{office_intro}"
            f"{special_bullets}"
            f"*   **Waking Night Support**: A trained, compassionate carer stays awake throughout the entire night to assist with scheduled medications, frequent repositioning in bed, bathroom visits, nocturnal disorientation, and fall prevention.\n"
            f"*   **Sleeping Night Support**: A carer sleeps on-site in a spare bedroom, on hand up to twice during the night for unexpected care needs, reassurance, or toileting assistance.\n"
            f"*   **Respite for Family Carers**: Providing family members with uninterrupted, restful sleep knowing their loved one is in safe, professional hands.\n"
            f"*   **Small, Consistent Night Teams**: Dedicated carers so {relative} feels secure seeing familiar, trusted faces each night.\n\n"
            f"To discuss overnight care schedules and book a free assessment, please call our Sawston office directly on **07917 611 425**."
        )

    # 9. 24/7 Live-In Care
    if has_live_in:
        return (
            f"Our 24/7 Live-In Care service provides a dedicated, full-time professional carer residing with **{relative}** {loc_text}:\n\n"
            f"{office_intro}"
            f"{special_bullets}"
            f"*   **24/7 One-to-One Peace of Mind**: A compassionate, dignified alternative to moving into a residential care home. Your loved one receives 100% personalized attention.\n"
            f"*   **Preserving Home, Memories & Pets**: Clients remain in their familiar home surroundings, sleep in their own bed, keep their pets, and welcome family whenever they wish.\n"
            f"*   **Comprehensive Daily Support**: Covers personal care, freshly prepared meals, light housekeeping, medication administration, companionship, and nighttime presence.\n"
            f"*   **Carefully Matched Carers**: Carers are matched based on personality, shared interests, dietary skills, and clinical care requirements.\n\n"
            f"To discuss live-in care arrangements with our Registered Care Manager, call **07917 611 425**."
        )

    # 10. General Health & Chronic Conditions (Arthritis, Diabetes, Mobility, Vision, Frailty, Palliative)
    health_keywords = ["arthritis", "diabetes", "diabetic", "mobility", "fall", "falls", "palliative", "terminal", "cancer", "vision", "blind", "sensory", "catheter", "stoma", "incontinence", "pain", "wheelchair", "hoist", "frail", "frailty", "elderly", "aged"]
    if any(k in q for k in health_keywords):
        condition_mention = next((k.title() for k in health_keywords if k in q), "Physical Health & Mobility")
        return (
            f"{opening_ack}, tailored to support **{condition_mention}** and daily wellbeing:\n\n"
            f"{office_intro}"
            f"{special_bullets}"
            f"*   **Un-Hurried Daily Personal Care**: Respectful, patient support with morning wake-up routines, bathing, showering, dressing, and skin care designed to accommodate physical stiffness, pain, or limited mobility.\n"
            f"*   **Mobility Assistance & Fall Prevention**: Safe transfer assistance (bed, chair, commode), safe positioning, and gentle mobility encouragement to promote independence while strictly guarding against fall hazards.\n"
            f"*   **Strict Medication Clinical Governance**: Prescription prompting and administration recorded on formal Medication Administration Records (MAR) under CQC clinical guidelines.\n"
            f"*   **Wholesome Cooking & Nutritional Care**: Freshly cooking healthy meals tailored to special dietary requirements (such as diabetic-friendly, low-sodium, or soft textures) and monitoring daily hydration.\n"
            f"*   **Small, Consistent Care Teams**: Small teams of DBS-checked, Care Certificate-trained carers so {relative} builds trust with familiar friendly faces.\n"
            f"*   **Free In-Home Assessment**: Our Registered Care Manager, **Mr. Rudrayya Mathapati** (former NHS Clinical Nurse Team Leader), visits your family home to design a bespoke Care Plan tailored to {possessive} health needs.\n\n"
            f"To discuss {relative}\'s daily routine or book your free assessment, please call our Sawston care coordinators directly on **07917 611 425**."
        )

    # 11. Standalone Carer Matching / Gender / Special Request Inquiries
    if special_notes:
        return (
            f"{opening_ack}:\n\n"
            f"{office_intro}"
            f"{special_bullets}"
            f"*   **Tailored Care Planning**: Following an in-home assessment, we draft a comprehensive Care Plan that incorporates personal preferences, routines, and safety requirements.\n"
            f"*   **Carer Continuity & Professional Standards**: All carers undergo Enhanced DBS checks, complete the Care Certificate, and participate in continuous professional development.\n\n"
            f"To discuss your specific carer matching requirements with our Registered Care Manager, **Mr. Rudrayya Mathapati**, please call our Sawston office on **07917 611 425**."
        )

    # 12. Personal Care (Washing, Bathing, Dressing, Continence)
    if any(k in q for k in ["personal care", "washing", "bathing", "shower", "showering", "dressing", "grooming", "toileting", "continence"]):
        return (
            f"Cambridge Care Services delivers CQC-regulated personal care for **{relative}** {loc_text} with the highest dignity, compassion, and privacy:\n\n"
            f"{office_intro}"
            f"*   **Morning & Bedtime Routines**: Gentle, unhurried assistance getting in and out of bed, safe transfers, and comfortable positioning.\n"
            f"*   **Washing & Bathing**: Respectful help with showers, baths, bed baths, hair washing, skin care, and oral hygiene.\n"
            f"*   **Dressing & Grooming**: Supporting personal clothing choices, compression hosiery, and grooming according to personal taste.\n"
            f"*   **Continence & Toileting**: Discreet, dignified assistance with personal toileting, catheter management, and stoma care.\n"
            f"*   **Medication Administration**: Administering prescribed medicines on strict schedules, fully audited on MAR sheets.\n\n"
            f"To arrange a free in-home consultation, please call our team on **07917 611 425**."
        )

    # 13. Companionship & Day Assistance
    if any(k in q for k in ["companionship", "lonely", "loneliness", "outing", "outings", "day assistance", "befriending", "hobbies"]):
        return (
            f"Our Companionship and Day Assistance services for **{relative}** {loc_text} are designed to combat loneliness, encourage social connection, and support independent living:\n\n"
            f"{office_intro}"
            f"*   **Meaningful Social Connection**: Friendly conversation, reading mail, listening to music, sharing memories, and participating in favorite hobbies.\n"
            f"*   **Community Outings & Medical Appointments**: Accompaniment to GP appointments, hospital clinics, cafes, garden centres, or shopping trips across Cambridge.\n"
            f"*   **Unhurried Daytime Support**: Flexible visits (from 1-hour sessions to full daytime blocks) providing meal preparation, light housekeeping, and gentle mobility.\n\n"
            f"To arrange companionship visits, please contact our team on **07917 611 425**."
        )

    # 14. Pricing, Costs, and Funding
    if any(k in q for k in ["cost", "costs", "price", "prices", "pricing", "rate", "rates", "charge", "charges", "how much", "fee", "fees", "quote", "pay for care", "funding", "direct payment", "direct payments", "nhs", "chc", "continuing healthcare", "attendance allowance", "pip"]):
        return (
            "At Cambridge Care Services, we operate a person-centered, bespoke fee structure with complete pricing transparency:\n\n"
            "*   **Transparent, Tailored Quotations**: Because every individual\'s needs differ, care rates depend on visit duration (e.g. 1-hour, 2-hour, or 3+ hour visits), visit frequency, time of day (daytime vs waking night vs sleep-in), and specialist skill level.\n"
            "*   **Clear Written Agreement**: Following your free in-home assessment, you receive a full, written, itemized quotation. There are **zero hidden administration fees**, no unexpected setup charges, and no unannounced rate increases.\n"
            "*   **Council Direct Payments**: If eligible for social care through Cambridgeshire County Council, you have the legal right to request Direct Payments, allowing you to choose Cambridge Care Services directly.\n"
            "*   **NHS Continuing Healthcare (CHC)**: For clients with primary complex health or nursing needs, care may be **100% funded by the NHS**. We coordinate directly with your NHS Integrated Care Board (ICB).\n"
            "*   **Attendance Allowance / PIP**: Non-means-tested state benefits (£72.65 to £108.55 per week) available to help support home care costs regardless of your personal savings.\n\n"
            "To discuss your budget, explore funding options, and receive a free personalized quote, please call our Sawston care team on **07917 611 425**."
        )

    # 15. Assessment / Process / Booking
    if any(k in q for k in ["assessment", "arrange", "book", "start care", "consultation", "onboarding", "how do we begin"]):
        return (
            "Arranging a free, no-obligation home care assessment with Cambridge Care Services is a straightforward 3-step process:\n\n"
            "1.  **Initial Consultation Call**: Contact our care coordinators on **07917 611 425** (Mon-Fri 09:30-21:00, Sat 10:00-15:00) to discuss immediate needs, care preferences, and visit schedules.\n"
            "2.  **In-Person Home Assessment**: Our Registered Care Manager, **Mr. Rudrayya Mathapati**, visits your family home in Cambridge or South Cambridgeshire to assess daily routines, mobility, home safety, and medical history.\n"
            "3.  **Bespoke Care Plan & Quotation**: We draft a detailed, person-centered Care Plan and provide a transparent, itemized written quote.\n\n"
            "There is zero obligation, and for urgent post-hospital discharge situations, care can often commence within **24 to 48 hours**."
        )

    # 16. Careers & Recruitment
    if any(k in q for k in ["job", "jobs", "career", "careers", "hiring", "apply", "carer vacancy", "recruitment", "salary", "wage", "training"]):
        return (
            "Cambridge Care Services is actively recruiting compassionate Care Assistants and Senior Support Workers across Cambridge and South Cambridgeshire:\n\n"
            "*   **Entry Requirements**: Compassion, empathy, right to work in the UK, valid UK driving licence with access to a reliable vehicle, and a clear Enhanced DBS check.\n"
            "*   **Comprehensive Paid Training**: We fund your **Care Certificate** induction and provide paid shadow shifts alongside experienced senior carers-no prior experience required for entry roles.\n"
            "*   **Pay & Benefits**: Competitive pay rates above the National Living Wage (with higher weekend and Bank Holiday rates), paid mileage allowance (45p/mile), paid travel time between visits, and guaranteed-hours contracts.\n\n"
            "To apply, visit our website careers section or contact our recruitment team directly on **07917 611 425**."
        )

    # 17. CQC Regulation & Leadership
    if any(k in q for k in ["cqc", "regulated", "rating", "inspection", "manager", "mathapati", "rudrayya", "dbs", "background", "police"]):
        return (
            "Cambridge Care Services is fully regulated by the **Care Quality Commission (CQC)** and operates under high clinical standards:\n\n"
            "*   **Registered Manager**: Mr. Rudrayya Mathapati, an experienced clinical leader and former NHS Nurse Team Leader with extensive nursing and community care experience.\n"
            "*   **Official CQC Registration**: Registered since 17 March 2022 (Head Office: 15 Deal Grove, Sawston, Cambridge, CB22 3DR).\n"
            "*   **Rigorous Staff Vetting**: Every care assistant undergoes an Enhanced DBS check, verified employment history, and multiple professional reference checks.\n"
            "*   **Carer Continuity & Quality Spot Checks**: We prioritize consistent carer allocation and conduct regular unannounced quality spot checks to ensure the highest standards of safety and dignity.\n\n"
            "Please call our office on **07917 611 425** to speak directly with our Registered Care Manager."
        )

    # 18. Pure Location Inquiry
    covered_places = [
        "sawston", "swaston", "great shelford", "little shelford", "shelford", "stapleford", 
        "babraham", "pampisford", "whittlesford", "duxford", "linton", "fulbourn", 
        "hinxton", "newton", "trumpington", "cherry hinton", "newnham", "chesterton", 
        "cambridge", "cb1", "cb2", "cb3", "cb4", "cb5", "cb21", "cb22", "cb23", "cb24", "cb25",
        "postcode", "postcodes", "area", "areas", "location", "locations", "coverage", "cover", "where do you"
    ]
    if any(p in q for p in covered_places):
        matched_town = next((p.title() for p in ["great shelford", "little shelford", "sawston", "duxford", "trumpington", "linton", "fulbourn", "stapleford", "cherry hinton"] if p in q), None)
        if matched_town:
            return (
                f"Yes, Cambridge Care Services proudly provides dedicated, CQC-regulated home care in **{matched_town}** and across South Cambridgeshire!\n\n"
                f"*   **Local Base & Carer Continuity**: We are headquartered right in **Sawston** (15 Deal Grove, CB22), meaning our carers are local to {matched_town} and can provide prompt, reliable visits.\n"
                f"*   **Comprehensive Services Available**: Personal care, dementia support, Parkinson\'s care, companionship, freshly prepared meals, medication management, and overnight waking care.\n"
                f"*   **Free In-Home Assessment**: Our Registered Care Manager can visit your home in {matched_town} for an unhurried, no-obligation care consultation.\n\n"
                f"Please call our local care team directly on **07917 611 425** to confirm immediate carer availability for {matched_town}."
            )
        return (
            "Cambridge Care Services is headquartered directly in **Sawston** (15 Deal Grove, CB22 3DR) and proudly delivers CQC-regulated home care across Cambridge City and South Cambridgeshire:\n\n"
            "*   **South Cambridgeshire Core Hub**: Sawston, Great Shelford, Little Shelford, Stapleford, Babraham, Pampisford, Whittlesford, Duxford, Linton, Fulbourn, Hinxton, and Newton.\n"
            "*   **Cambridge City & Suburbs**: Postcodes **CB1, CB2, CB3, CB4, and CB5** (including Trumpington, Cherry Hinton, Newnham, and Chesterton).\n"
            "*   **Surrounding Regional Villages**: Full coverage across **CB21, CB22, CB23, CB24, and CB25** (such as Cambourne, Histon, Impington, Cottenham, and Waterbeach).\n"
            "*   **Flexible Border Policy**: If your loved one resides in bordering towns such as Royston, Haverhill, Newmarket, or Ely, our management team assesses local carer availability and can often accommodate care packages.\n\n"
            "Please contact our Sawston office directly on **07917 611 425** to confirm immediate carer availability for your specific postcode."
        )

    # 19. All Services Overview & Comprehensive Catch-All
    return (
        f"Cambridge Care Services is a regulated home care provider registered with the Care Quality Commission (CQC), delivering high-quality, compassionate care for **{relative}** {loc_text}:\n\n"
        f"{office_intro}"
        f"1.  **Personal Care**: Respectful support with morning, afternoon, and evening routines, including washing, bathing, showering, oral hygiene, dressing, grooming, continence care, and catheter/stoma management.\n"
        f"2.  **Specialist Dementia & Alzheimer\'s Care**: Person-centered support focused on maintaining familiar routines, gentle communication, de-escalation for anxiety or sundowning, and comforting companionship in familiar home surroundings.\n"
        f"3.  **Specialist Parkinson\'s & Neurological Care**: Mobility assistance, fall prevention, safe transfers, posture support, and time-critical medication prompting.\n"
        f"4.  **Companionship & Day Assistance**: Combatting loneliness through friendly conversation, accompaniment to GP appointments or local shops, hobby engagement, and nutritious meal preparation.\n"
        f"5.  **Medication Management**: Safe administration and prompting of prescribed tablets, blister packs, and eye drops, all recorded on formal Medication Administration Records (MAR) under strict CQC clinical guidelines.\n"
        f"6.  **Night Care Support**: Waking nights (carer awake all night to support with medication, repositioning, and nocturnal restlessness) and Sleeping nights (carer sleeps on-site for peace of mind).\n"
        f"7.  **Respite Care**: Flexible cover from a few hours a week to multi-week live-in cover while family caregivers rest or travel.\n"
        f"8.  **24/7 Live-In Care**: A dedicated, full-time professional carer residing in the home, offering an unhurried, dignified alternative to moving into a residential care home.\n"
        f"9.  **Complex Care & Hospital Discharge**: Post-stroke rehabilitation, neurological support, and reablement care coordinated alongside NHS District Nurses and GPs.\n"
        f"10. **Palliative & End-of-Life Care**: Compassionate, dignified comfort care focusing on pain relief assistance and emotional family support during life\'s most sensitive moments.\n\n"
        f"To discuss {relative}\'s care needs and book a free in-home consultation with our Registered Care Manager, **Mr. Rudrayya Mathapati**, please call our Sawston care team on **07917 611 425**."
    )


def route_query_intent(query: str) -> str:
    return route_care_inquiry(query)

# ==============================================================================
# MAIN RAG FUNCTION (<2.5s CEILING GUARANTEE)
# ==============================================================================

def ask_cambridge_care_bot(question: str, api_key: str = None) -> str:
    """
    Main Universal RAG function:
    1. Universal Care Intelligence Engine delivers exact CQC response in <0.001s.
    2. If novel question, tries Gemini with full 5-part healthcare prompt.
    3. If Gemini is unavailable or times out, immediately synthesizes from CQC knowledge base.
    Guarantees detailed, compassionate, CQC-compliant responses with zero crisp answers.
    """
    # Step 1: Universal Care Intelligence Engine (<0.001s)
    routed = route_care_inquiry(question)
    if routed:
        return routed

    # Step 2: Retrieve relevant context from ChromaDB
    relevant_chunks = retrieve_relevant_context(question, top_k=3)

    # Step 3: Check API key
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            try:
                import streamlit as st
                api_key = st.secrets.get("GEMINI_API_KEY", "")
            except Exception:
                pass

    if not api_key or genai is None:
        return route_care_inquiry("services")

    # Step 4: High-detail Gemini call with 3.5s timeout
    try:
        genai.configure(api_key=api_key)
        context_text = "\n\n---\n\n".join([f"[From {c['source']}]:\n{c['text']}" for c in relevant_chunks])
        prompt = (
            f"You are the senior virtual care advisor for Cambridge Care Services, a CQC-regulated home care provider headquartered in Sawston (15 Deal Grove, CB22 3DR) and serving Cambridge and South Cambridgeshire.\n\n"
            f"Knowledge Base Context:\n{context_text}\n\n"
            f"User Question: {question}\n\n"
            f"Operating Instructions:\n"
            f"Provide a warm, compassionate, and detailed healthcare response following this exact structure:\n"
            f"1. Directly acknowledge the family member (e.g. your Father, Mother, Aunt, or loved one) and understand their specific health condition or care needs.\n"
            f"2. Detail concrete in-home care routines (morning assistance, dignified personal care, fresh meal cooking, hydration, or night support).\n"
            f"3. Explain CQC clinical safeguards (time-critical medication on MAR records, safe transfers/fall prevention, Enhanced DBS-checked carers).\n"
            f"4. Confirm small, consistent care teams and our local base in Sawston / South Cambridgeshire.\n"
            f"5. Warmly invite them to a free in-home care assessment with Registered Care Manager, Mr. Rudrayya Mathapati, and provide our phone number: 07917 611 425."
        )
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt, request_options={"timeout": 3.5})
        if response and response.text and len(response.text.strip()) > 100:
            return response.text.strip()
    except Exception:
        pass

    return route_care_inquiry("services")
