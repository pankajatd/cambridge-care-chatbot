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
        padding-bottom: 7rem !important;
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
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        flex-wrap: nowrap !important;
        gap: 10px !important;
        margin-bottom: 0 !important;
        width: 100% !important;
    }}

    .brand-group {{
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        min-width: 0 !important;
        flex: 1 1 auto !important;
    }}

    .brand-info {{
        min-width: 0 !important;
        overflow: hidden !important;
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
        flex-shrink: 0 !important;
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
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
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
        flex-shrink: 0 !important;
        white-space: nowrap !important;
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

    /* Dedicated Popular Inquiry Tab Info Card (Option 1) */
    .tab-info-card {{
        background: #FFFFFF !important;
        border: 2px solid #F66A71 !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        margin-top: 4px !important;
        margin-bottom: 18px !important;
        box-shadow: 0 4px 16px rgba(246, 106, 113, 0.15), 0 1px 3px rgba(0, 0, 0, 0.04) !important;
        animation: fadeIn 0.25s ease-in-out !important;
    }}
    .tab-info-header {{
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        margin-bottom: 8px !important;
        padding-bottom: 6px !important;
        border-bottom: 1.5px solid #F1F5F9 !important;
    }}
    .tab-info-title {{
        font-size: 13.5px !important;
        font-weight: 700 !important;
        color: #1E293B !important;
    }}
    .tab-info-body {{
        font-size: 12.5px !important;
        line-height: 1.55 !important;
        color: #334155 !important;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(-4px); }}
        to {{ opacity: 1; transform: translateY(0); }}
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
            padding-bottom: 6.5rem !important;
        }}

        .header-card {{
            padding: 8px 10px !important;
            border-radius: 14px !important;
            margin-bottom: 8px !important;
        }}

        .header-top {{
            flex-wrap: nowrap !important;
            gap: 6px !important;
        }}

        .brand-group {{
            gap: 7px !important;
            min-width: 0 !important;
            flex: 1 1 auto !important;
        }}

        .brand-logo-container {{
            width: 34px !important;
            height: 34px !important;
            border-radius: 9px !important;
            padding: 2px !important;
            flex-shrink: 0 !important;
        }}

        .brand-name {{
            font-size: clamp(12.5px, 3.5vw, 15px) !important;
            line-height: 1.15 !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }}

        .single-capsule-tab {{
            font-size: 8px !important;
            padding: 2px 5px !important;
            margin-top: 2px !important;
            gap: 3px !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            max-width: 100% !important;
        }}

        .phone-button {{
            padding: 5px 8px !important;
            font-size: clamp(9.5px, 2.7vw, 11px) !important;
            gap: 4px !important;
            flex-shrink: 0 !important;
            white-space: nowrap !important;
            align-self: center !important;
        }}

        .phone-svg-icon {{
            width: 10px !important;
            height: 10px !important;
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

        /* Mobile adaptation for Popular Inquiry Tab Info Card */
        .tab-info-card {{
            padding: 10px 12px !important;
            border-radius: 12px !important;
            margin-bottom: 12px !important;
        }}
        .tab-info-title {{
            font-size: 12px !important;
        }}
        .tab-info-body {{
            font-size: 11.5px !important;
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
    div[data-testid="stBottom"],
    .stBottom {{
        background: #F8F9FA !important;
        background: linear-gradient(180deg, rgba(248, 249, 250, 0.95) 0%, #F1F4F7 100%) !important;
        backdrop-filter: blur(10px) !important;
        padding-top: 10px !important;
        padding-bottom: 14px !important;
        border-top: 1px solid rgba(226, 232, 240, 0.8) !important;
    }}

    div[data-testid="stBottom"] > div {{
        max-width: 740px !important;
        margin: 0 auto !important;
        padding: 0 !important;
    }}

    div[data-testid="stChatInput"] {{
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
    }}

    div[data-testid="stChatInput"] > div {{
        border: 2px solid #F66A71 !important;
        border-radius: 30px !important;
        box-shadow: 0 4px 20px rgba(246, 106, 113, 0.35) !important;
        background: #FFFFFF !important;
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        padding: 4px 10px 4px 18px !important;
        min-height: 52px !important;
        box-sizing: border-box !important;
        transition: all 0.25s ease !important;
    }}

    div[data-testid="stChatInput"]:focus-within > div {{
        border-color: #E8505B !important;
        box-shadow: 0 6px 28px rgba(246, 106, 113, 0.5) !important;
    }}

    /* Remove inner Baseweb red focus borders so entire capsule is one unified pill */
    div[data-testid="stChatInput"] [data-baseweb="textarea"],
    div[data-testid="stChatInput"] [data-baseweb="base-input"],
    div[data-testid="stChatInput"] [data-baseweb="textarea"]:focus-within,
    div[data-testid="stChatInput"] [data-baseweb="base-input"]:focus-within {{
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        background: transparent !important;
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }}

    div[data-testid="stChatInput"] textarea,
    div[data-testid="stChatInput"] textarea:focus,
    div[data-testid="stChatInput"] textarea:hover {{
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        background: transparent !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        color: #1A202C !important;
        min-height: 40px !important;
        height: auto !important;
        line-height: 1.4 !important;
        padding: 8px 6px 8px 0 !important;
        overflow: hidden !important;
        overflow-y: hidden !important;
        overflow-x: hidden !important;
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
        resize: none !important;
        box-sizing: border-box !important;
        align-self: center !important;
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
        width: 34px !important;
        height: 34px !important;
        min-width: 34px !important;
        min-height: 34px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        align-self: center !important;
        margin: auto 0 !important;
        flex-shrink: 0 !important;
        cursor: pointer !important;
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
            <div class="brand-info">
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

# Gold-Standard Content for Popular Inquiries (Option 1: Instant, Dedicated Panel)
TAB_CONTENT = {
    "free_assessment": {
        "title": "📋 Free, No-Obligation Home Care Assessment",
        "text": (
            "Arranging a free home care assessment with Cambridge Care Services is simple:\n\n"
            "1. **Call Our Team**: Reach our care coordinators directly on **07917 611 425** (Mon–Fri, 9am–5pm).\n"
            "2. **In-Home Visit**: Our Registered Care Manager visits you and your family in the comfort of your home in Cambridge or South Cambridgeshire.\n"
            "3. **Personalized Care Plan**: We assess daily routines, mobility, medication needs, and personal preferences to create a tailored care proposal and transparent quote.\n\n"
            "There is zero obligation, and family members are warmly encouraged to join the assessment."
        )
    },
    "area_coverage": {
        "title": "📍 Areas & Postcodes Covered across Cambridgeshire",
        "text": (
            "Cambridge Care Services is headquartered at 15 Deal Grove, Sawston, and provides dedicated home care across:\n\n"
            "*   **South Cambridgeshire (Core Hub)**: Sawston, Great & Little Shelford, Duxford, Whittlesford, Pampisford, Babraham, Linton, Fulbourn, Stapleford, Hinxton, and Newton.\n"
            "*   **Cambridge City**: Postcodes **CB1, CB2, CB3, CB4, and CB5** (including Trumpington, Cherry Hinton, Newnham, and Chesterton).\n"
            "*   **Wider Coverage**: Surrounding villages across **CB21, CB22, CB23, CB24, and CB25**.\n\n"
            "Please call us directly on **07917 611 425** to confirm immediate carer availability for your postcode."
        )
    },
    "care_funding": {
        "title": "💷 Care Funding Pathways & Support",
        "text": (
            "We support all primary care funding pathways across Cambridgeshire:\n\n"
            "*   **Direct Payments (Council Funded)**: If eligible through Cambridgeshire County Council Social Services, you can request Direct Payments to select Cambridge Care Services directly rather than council-allocated providers.\n"
            "*   **NHS Continuing Healthcare (CHC)**: If approved for NHS CHC due to complex health needs, the NHS covers 100% of care costs. We coordinate directly with your NHS Integrated Care Board (ICB).\n"
            "*   **Attendance Allowance / PIP**: Non-means-tested government benefits (£72.65 to £108.55/week) to help fund home care support.\n"
            "*   **Self-Funded (Private Pay)**: Transparent, itemized invoicing with no hidden management fees following your free assessment."
        )
    },
    "care_careers": {
        "title": "💼 Care Assistant Careers & Entry Requirements",
        "text": (
            "We are actively hiring compassionate Care Assistants across Cambridge and South Cambridgeshire:\n\n"
            "*   **Entry Requirements**: Compassion, reliability, right to work in the UK, valid driving licence with access to a vehicle, and a clear Enhanced DBS check.\n"
            "*   **Full Training Provided**: We provide comprehensive induction training and fund your **Care Certificate** (no prior experience required for entry roles).\n"
            "*   **What We Offer**: Competitive pay above the National Living Wage, paid mileage (45p/mile), paid travel time between visits, and guaranteed-hours contracts.\n\n"
            "To apply or discuss current vacancies, contact our recruitment team on **07917 611 425**."
        )
    }
}

# State management: Popular tab viewer and User Chat are completely isolated
if "active_tab" not in st.session_state:
    st.session_state.active_tab = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Quick Action Chips for Fast Pre-set Queries (Option 1: Overwrites cleanly on click, tap again to close)
st.markdown('<div class="suggestions-label">Popular Inquiries</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4, gap="small")

with col1:
    if st.button("📋 Free Assessment", use_container_width=True):
        st.session_state.active_tab = None if st.session_state.active_tab == "free_assessment" else "free_assessment"
with col2:
    if st.button("📍 Area Coverage", use_container_width=True):
        st.session_state.active_tab = None if st.session_state.active_tab == "area_coverage" else "area_coverage"
with col3:
    if st.button("💷 Care Funding", use_container_width=True):
        st.session_state.active_tab = None if st.session_state.active_tab == "care_funding" else "care_funding"
with col4:
    if st.button("💼 Care Careers", use_container_width=True):
        st.session_state.active_tab = None if st.session_state.active_tab == "care_careers" else "care_careers"

# Dedicated Option 1 Tab Information Card (instant 0ms display; switches topic cleanly)
if st.session_state.active_tab and st.session_state.active_tab in TAB_CONTENT:
    tab_data = TAB_CONTENT[st.session_state.active_tab]
    st.markdown(f"""
    <div class="tab-info-card">
        <div class="tab-info-header">
            <span class="tab-info-title">{tab_data['title']}</span>
            <span style="font-size: 11px; color: #94A3B8; font-weight: 500;">Tap pill to close</span>
        </div>
        <div class="tab-info-body">
    """, unsafe_allow_html=True)
    st.markdown(tab_data["text"])
    st.markdown("</div></div>", unsafe_allow_html=True)

# High-performance care bot loader
@st.cache_resource(show_spinner=False)
def get_care_bot():
    from rag import ask_cambridge_care_bot
    return ask_cambridge_care_bot

# ----------------- USER CHAT CONVERSATION (METHOD B) -----------------
user_input = st.chat_input("Ask about care services, locations, funding...")

has_history = len(st.session_state.chat_history) > 0

# Case 1: Fresh visit — show welcome greeting
if not has_history and not user_input:
    with st.chat_message("assistant"):
        st.write("Hello! I am your virtual care advisor for **Cambridge Care Services**.\n\nHow can I support you today? You can tap any of the **Popular Inquiries** above, or ask below about **home care services**, **postcodes covered across Cambridge & South Cambs**, **funding pathways (NHS / Direct Payments)**, or **booking a free in-home assessment**.")

# Case 2: User just submitted a question
elif user_input:
    # All prior history folds into the expander immediately
    if has_history:
        past_count = len(st.session_state.chat_history)
        with st.expander(f"📂 View Previous Questions ({past_count})", expanded=False):
            for past in st.session_state.chat_history:
                with st.chat_message("user"):
                    st.write(past["question"])
                with st.chat_message("assistant"):
                    st.write(past["answer"])

    # Render current question in full view
    with st.chat_message("user"):
        st.write(user_input)
    with st.chat_message("assistant"):
        bot = get_care_bot()
        response = bot(user_input)
        st.write(response)

    # Save to history without st.rerun() to prevent connection blips or lost state
    st.session_state.chat_history.append({
        "question": user_input,
        "answer": response
    })

# Case 3: Page re-render or tab click — show folded past + latest in full view
else:
    total_chat = len(st.session_state.chat_history)
    if total_chat > 1:
        past_count = total_chat - 1
        with st.expander(f"📂 View Previous Questions ({past_count})", expanded=False):
            for past in st.session_state.chat_history[:-1]:
                with st.chat_message("user"):
                    st.write(past["question"])
                with st.chat_message("assistant"):
                    st.write(past["answer"])

    if total_chat >= 1:
        latest = st.session_state.chat_history[-1]
        with st.chat_message("user"):
            st.write(latest["question"])
        with st.chat_message("assistant"):
            st.write(latest["answer"])
