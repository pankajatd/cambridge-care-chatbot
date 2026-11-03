import os
import base64
import threading
import streamlit as st

# Set professional page title and favicon (MUST BE FIRST STREAMLIT COMMAND)
st.set_page_config(
    page_title="Cambridge Care Services Assistant",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Nurse Uniform Palette (Slate Tunic Grey & Rose-Pink Piping from official hero photo)
st.markdown(f"""
<style>
    /* Global Body & Background - Fast native typography, zero blocking network roundtrips */
    html, body, .stApp {{
        background: #F8F9FA;
        background: linear-gradient(180deg, #FAFBFC 0%, #F1F4F7 100%);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        color: #242A2E;
        overflow-x: hidden !important;
    }}

    /* Completely hide Streamlit branding, footer, watermarks, and Community Cloud badges */
    footer,
    footer:after,
    .stFooter,
    div[data-testid="stFooter"],
    #MainMenu,
    header[data-testid="stHeader"] .stDeployButton,
    div[data-testid="stDecoration"],
    div[data-testid="stStatusWidget"],
    div[data-testid="stToolbarActions"],
    [data-testid="manage-app-button"],
    #manage-app-button,
    [class*="viewerBadge"],
    div[class*="viewerBadge"],
    a[class*="viewerBadge"],
    .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_,
    .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK,
    div[class*="ProfileBadge"],
    .stDeployButton {{
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }}

    /* Streamlit top header cleanup */
    header[data-testid="stHeader"] {{
        background: transparent !important;
        height: 2.2rem !important;
    }}

    /* Main Container: Generous Full Laptop Layout by Default */
    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 860px !important;
    }}

    /* ---------------- NURSE UNIFORM HEADER CARD (SLEEK NAVBAR) ---------------- */
    .header-card {{
        background: #3A4046;
        background: linear-gradient(145deg, #3A4046 0%, #282D32 100%);
        border: 2px solid #F66A71 !important;
        border-radius: 18px;
        padding: 15px 22px;
        margin-bottom: 14px;
        box-shadow: 0 10px 28px rgba(246, 106, 113, 0.18), 0 4px 14px rgba(40, 45, 50, 0.4);
        position: relative;
    }}

    .header-top {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 0;
    }}

    .brand-group {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .brand-logo-container {{
        width: 46px;
        height: 46px;
        background: #FFFFFF;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        border: 1.5px solid rgba(246, 106, 113, 0.4);
        padding: 3px;
        flex-shrink: 0;
    }}

    .brand-logo-img {{
        width: 100%;
        height: 100%;
        object-fit: contain;
    }}

    .brand-name {{
        font-size: 20px;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: -0.3px;
        line-height: 1.2;
    }}

    /* Single Unified Capsule Tab under Brand Name */
    .single-capsule-tab {{
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 11px;
        font-weight: 500;
        color: #E2E8F0;
        display: inline-flex;
        align-items: center;
        gap: 7px;
        margin-top: 5px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.12);
        transition: all 0.2s ease;
    }}

    .single-capsule-tab:hover {{
        background: rgba(246, 106, 113, 0.15);
        border-color: #F66A71;
        color: #FFFFFF;
    }}

    .capsule-divider {{
        color: rgba(255, 255, 255, 0.35);
        font-size: 10px;
    }}

    .sleek-dot {{
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: #F66A71;
        box-shadow: 0 0 6px #F66A71;
        display: inline-block;
        flex-shrink: 0;
    }}

    /* Phone Button */
    a.phone-button,
    a.phone-button *,
    a.phone-button:hover,
    a.phone-button:visited,
    a.phone-button:active,
    a.phone-button:focus,
    div[data-testid="stMarkdownContainer"] a.phone-button,
    div[data-testid="stMarkdownContainer"] a.phone-button * {{
        text-decoration: none !important;
        text-decoration-line: none !important;
        border-bottom: none !important;
        outline: none !important;
        color: #FFFFFF !important;
    }}

    .phone-button {{
        display: inline-flex !important;
        align-items: center !important;
        gap: 8px !important;
        background: linear-gradient(135deg, #F66A71 0%, #C43F4A 100%) !important;
        color: #FFFFFF !important;
        padding: 8px 16px !important;
        border-radius: 50px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 14px rgba(246, 106, 113, 0.45) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        cursor: pointer;
        transition: all 0.2s ease !important;
    }}

    .phone-button:hover {{
        transform: translateY(-1px) scale(1.02);
        box-shadow: 0 6px 18px rgba(246, 106, 113, 0.6) !important;
    }}

    .phone-svg-icon {{
        width: 13px;
        height: 13px;
        fill: #FFFFFF;
        display: inline-block;
        vertical-align: middle;
    }}

    /* ---------------- POPULAR INQUIRY PILLS: LAPTOP DEFAULT (FULL SIZED & ELEGANT) ---------------- */
    .suggestions-label {{
        font-size: 11px;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
        margin-top: 2px;
    }}

    /* Row Container: NEVER WRAPS, ALWAYS 1 SINGLE HORIZONTAL LINE */
    div[data-testid="stHorizontalBlock"],
    [data-testid="stHorizontalBlock"],
    .stHorizontalBlock {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: stretch !important;
        gap: 8px !important;
        margin-bottom: 12px !important;
        width: 100% !important;
    }}

    /* Laptop: 4 columns evenly across width */
    div[data-testid="stHorizontalBlock"] > div,
    [data-testid="stHorizontalBlock"] > div,
    .stHorizontalBlock > div,
    div[data-testid="column"],
    [data-testid="column"] {{
        width: calc(25% - 6px) !important;
        min-width: 0 !important;
        max-width: calc(25% - 6px) !important;
        flex: 1 1 calc(25% - 6px) !important;
        padding: 0 !important;
        margin: 0 !important;
    }}

    div.stButton {{
        width: 100% !important;
        height: 100% !important;
        display: flex !important;
    }}

    div.stButton > button {{
        background-color: #FFFFFF !important;
        color: #334155 !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 14px !important;
        padding: 6px 10px !important;
        min-height: 38px !important;
        height: 100% !important;
        width: 100% !important;
        max-width: 100% !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        line-height: 1.2 !important;
        letter-spacing: 0 !important;
        white-space: normal !important;
        word-break: normal !important;
        text-align: center !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
    }}

    div.stButton > button:hover {{
        background-color: #F66A71 !important;
        color: #FFFFFF !important;
        border-color: #F66A71 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 8px rgba(246, 106, 113, 0.28) !important;
    }}

    /* Mobile Responsive Adaptation (< 640px) */
    @media (max-width: 640px) {{
        .block-container {{
            padding-top: 1rem !important;
            padding-left: 8px !important;
            padding-right: 8px !important;
            padding-bottom: 0.5rem !important;
        }}

        .header-card {{
            padding: 10px 12px !important;
            border-radius: 14px !important;
            margin-bottom: 8px !important;
        }}

        .brand-name {{
            font-size: 16px !important;
        }}

        .single-capsule-tab {{
            font-size: 9px !important;
            padding: 2px 7px !important;
            flex-wrap: wrap !important;
            gap: 4px !important;
        }}

        .phone-button {{
            padding: 6px 12px !important;
            font-size: 11px !important;
        }}

        /* On mobile, tighten column gaps and scale button font to fit 4 in a row */
        div[data-testid="stHorizontalBlock"],
        [data-testid="stHorizontalBlock"],
        .stHorizontalBlock {{
            gap: 4px !important;
            margin-bottom: 8px !important;
        }}

        div[data-testid="stHorizontalBlock"] > div,
        [data-testid="stHorizontalBlock"] > div,
        .stHorizontalBlock > div,
        div[data-testid="column"],
        [data-testid="column"] {{
            width: calc(25% - 3px) !important;
            min-width: 0 !important;
            max-width: calc(25% - 3px) !important;
            flex: 1 1 calc(25% - 3px) !important;
        }}

        div.stButton > button {{
            font-size: clamp(8px, 2.2vw, 10px) !important;
            padding: 3px 2px !important;
            min-height: 30px !important;
            border-radius: 10px !important;
        }}
    }}

    /* ---------------- UNIFORM BOX SIZES & COMPACT TAB DESCRIPTION ---------------- */
    div[data-testid="stExpander"] {{
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        margin-bottom: 7px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
        overflow: hidden !important;
        width: 100% !important;
        max-width: 100% !important;
        transition: all 0.2s ease !important;
    }}

    div[data-testid="stExpander"]:hover {{
        border-color: #CBD5E0 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03) !important;
    }}

    div[data-testid="stExpander"] summary {{
        font-size: 11.5px !important;
        font-weight: 600 !important;
        color: #4A5568 !important;
        padding: 6px 12px !important;
        background: #F8FAFC !important;
        min-height: unset !important;
        line-height: 1.35 !important;
    }}

    div[data-testid="stExpander"] summary:hover {{
        color: #F66A71 !important;
        background: #F1F5F9 !important;
    }}

    div[data-testid="stExpander"] summary svg {{
        width: 13px !important;
        height: 13px !important;
        color: #F66A71 !important;
    }}

    /* Description text displayed when tab is clicked / expanded */
    div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {{
        padding: 10px 14px !important;
        background: #FAFBFC !important;
        border-top: 1px solid #EDF2F7 !important;
    }}

    div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] p,
    div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] li,
    div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] div[data-testid="stMarkdownContainer"] {{
        font-size: 11.5px !important;
        line-height: 1.5 !important;
        color: #4A5568 !important;
    }}

    /* ---------------- CHAT MESSAGES ---------------- */
    div[data-testid="stChatMessage"] {{
        padding: 0 !important;
        background: transparent !important;
        margin-bottom: 14px !important;
        gap: 10px !important;
        width: 100% !important;
    }}

    div[data-testid="stChatMessageAvatarAssistant"] {{
        background: linear-gradient(135deg, #F66A71 0%, #C43F4A 100%) !important;
        color: #FFFFFF !important;
        border-radius: 50% !important;
        box-shadow: 0 4px 10px rgba(246, 106, 113, 0.3) !important;
        border: 2px solid #FFFFFF !important;
        width: 36px !important;
        height: 36px !important;
    }}

    div[data-testid="stChatMessageAvatarUser"] {{
        background: #3A4046 !important;
        color: #FFFFFF !important;
        border-radius: 50% !important;
        box-shadow: 0 4px 10px rgba(58, 64, 70, 0.25) !important;
        border: 2px solid #FFFFFF !important;
        width: 36px !important;
        height: 36px !important;
    }}

    /* Assistant Card */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) div[data-testid="stMarkdownContainer"] {{
        background: #FFFFFF;
        border: 1px solid #E5E9EC;
        border-radius: 4px 16px 16px 16px;
        padding: 13px 18px;
        box-shadow: 0 3px 14px rgba(0, 0, 0, 0.03), 0 1px 3px rgba(0, 0, 0, 0.02);
        color: #2D3748;
        font-size: 12.5px !important;
        line-height: 1.55 !important;
        width: 100% !important;
    }}

    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) div[data-testid="stMarkdownContainer"] p {{
        color: #2D3748;
        font-size: 12.5px !important;
        margin-bottom: 6px !important;
    }}

    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) div[data-testid="stMarkdownContainer"] li {{
        font-size: 12px !important;
        margin-bottom: 3px !important;
        line-height: 1.45 !important;
    }}

    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) div[data-testid="stMarkdownContainer"] p:last-child {{
        margin-bottom: 0 !important;
    }}

    /* User Message Bubble */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {{
        flex-direction: row-reverse !important;
    }}

    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) div[data-testid="stMarkdownContainer"] {{
        background: linear-gradient(135deg, #F66A71 0%, #C43F4A 100%);
        border-radius: 16px 4px 16px 16px;
        padding: 8px 16px;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(246, 106, 113, 0.25);
        font-size: 12.5px !important;
        width: 100% !important;
    }}

    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) div[data-testid="stMarkdownContainer"] p {{
        color: #FFFFFF !important;
        font-size: 12.5px !important;
        line-height: 1.4;
        margin: 0;
    }}

    /* ---------------- HIGHLIGHTED QUERY INPUT BOX - NO SCROLLBAR ---------------- */
    div[data-testid="stBottom"] {{
        background: transparent !important;
        padding-bottom: 12px !important;
    }}

    div[data-testid="stBottom"] > div {{
        max-width: 740px !important;
        margin: 0 auto !important;
        padding: 0 !important;
    }}

    div[data-testid="stChatInput"],
    .stChatInput,
    div[data-testid="stChatInput"] > div {{
        border: 2.5px solid #F66A71 !important;
        border-radius: 22px !important;
        box-shadow: 0 6px 26px rgba(246, 106, 113, 0.38), 0 2px 8px rgba(0, 0, 0, 0.06) !important;
        background: #FFFFFF !important;
        min-height: 52px !important;
        transition: all 0.25s ease !important;
    }}

    div[data-testid="stChatInput"]:focus-within,
    div[data-testid="stChatInput"] > div:focus-within {{
        border-color: #E8505B !important;
        box-shadow: 0 8px 32px rgba(246, 106, 113, 0.55), 0 3px 10px rgba(0, 0, 0, 0.1) !important;
    }}

    div[data-testid="stChatInput"] textarea,
    div[data-testid="stChatInput"] textarea:focus,
    div[data-testid="stChatInput"] textarea:hover {{
        font-size: 13.5px !important;
        font-weight: 500 !important;
        color: #1A202C !important;
        min-height: 44px !important;
        height: auto !important;
        line-height: 1.35 !important;
        padding: 10px 12px 8px 14px !important;
        overflow: hidden !important;
        overflow-y: hidden !important;
        overflow-x: hidden !important;
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
        resize: none !important;
        box-sizing: border-box !important;
    }}

    div[data-testid="stChatInput"] textarea::-webkit-scrollbar {{
        display: none !important;
        width: 0 !important;
        height: 0 !important;
    }}

    div[data-testid="stChatInput"] button {{
        background: linear-gradient(135deg, #F66A71 0%, #C43F4A 100%) !important;
        border-radius: 50% !important;
        color: #FFFFFF !important;
        box-shadow: 0 2px 8px rgba(246, 106, 113, 0.45) !important;
        border: none !important;
        width: 36px !important;
        height: 36px !important;
    }}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-card">
    <div class="header-top">
        <div class="brand-group">
            <div class="brand-logo-container">
                <img class="brand-logo-img" src="https://www.cambridgecareservices.co.uk/images/logo-mark.png" alt="Cambridge Care Services Logo" />
            </div>
            <div>
                <div class="brand-name">Cambridge Care Services</div>
                <div class="single-capsule-tab">
                    <span class="sleek-dot"></span>
                    <span>CQC Regulated Provider</span>
                    <span class="capsule-divider">•</span>
                    <span>📍 Sawston (CB22) & South Cambridgeshire</span>
                </div>
            </div>
        </div>
        <a class="phone-button" href="tel:07917611425">
            <svg class="phone-svg-icon" viewBox="0 0 24 24">
                <path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
            </svg>
            <span>07917 611 425</span>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize conversation history organized by inquiries (question + answer exchanges)
if "inquiries" not in st.session_state:
    st.session_state.inquiries = []

# Quick Action Chips for Fast Pre-set Queries (Exact Laptop Layout)
st.markdown('<div class="suggestions-label">Popular Inquiries</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4, gap="small")

preset_query = None
with col1:
    if st.button("📋 Free Assessment", use_container_width=True):
        preset_query = "How do I arrange a free home care assessment?"
with col2:
    if st.button("📍 Area Coverage", use_container_width=True):
        preset_query = "What postcodes and towns in Cambridgeshire do you cover?"
with col3:
    if st.button("💷 Care Funding", use_container_width=True):
        preset_query = "How is care funded? Can I use NHS Continuing Healthcare or Direct Payments?"
with col4:
    if st.button("💼 Care Careers", use_container_width=True):
        preset_query = "What carer jobs are currently available and what are the entry requirements?"

# Display Initial Welcome Greeting if no inquiries yet
if not st.session_state.inquiries:
    with st.chat_message("assistant"):
        st.write("Hello! I am your virtual care advisor for **Cambridge Care Services**.\n\nHow can I support you today? You can ask about our **home care services**, **postcodes covered across Cambridge & South Cambs**, **funding pathways (NHS / Direct Payments)**, or **booking a free in-home care assessment**.")

# Render Inquiries:
# 1. Previous inquiries are collapsed in a uniform 100% width card
# 2. Latest inquiry is expanded in full view with matching uniform width
total_inquiries = len(st.session_state.inquiries)

for idx, inq in enumerate(st.session_state.inquiries):
    is_latest = (idx == total_inquiries - 1)
    
    if not is_latest:
        # COLLAPSED TAB - 100% UNIFORM WIDTH MATCHING ACTIVE BOX
        with st.expander(f"Previous Inquiry: {inq['question']}", expanded=False):
            with st.chat_message("user"):
                st.write(inq["question"])
            with st.chat_message("assistant"):
                st.write(inq["answer"])
    else:
        # LATEST INQUIRY - 100% UNIFORM WIDTH
        with st.chat_message("user"):
            st.write(inq["question"])
        with st.chat_message("assistant"):
            st.write(inq["answer"])

# Handle user query (either typed in input box or clicked from quick chips)
user_input = st.chat_input("Ask about care services, locations, funding...")
active_query = preset_query or user_input

# Non-blocking background warm-up: prepares database in RAM without delaying page display
def _background_warmup():
    try:
        from rag import warmup_chroma_db
        warmup_chroma_db()
    except Exception:
        pass

if "warmed" not in st.session_state:
    st.session_state.warmed = True
    threading.Thread(target=_background_warmup, daemon=True).start()

if active_query:
    from rag import ask_cambridge_care_bot
    # 1. Immediately show user message
    with st.chat_message("user"):
        st.write(active_query)

    # 2. Query ChromaDB and Gemini via RAG
    with st.chat_message("assistant"):
        with st.spinner("Consulting care guidelines..."):
            response = ask_cambridge_care_bot(active_query)
            st.write(response)
            
    # 3. Save new inquiry exchange into session history
    st.session_state.inquiries.append({
        "question": active_query,
        "answer": response
    })
