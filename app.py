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
        padding: 8px 14px 8px 0 !important;
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
        transform: translateX(-14px) !important;
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
            "1. **Call Our Team**: Reach our care coordinators directly on **07917 611 425** (Mon-Fri, 9am-5pm).\n"
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

# ==============================================================================
# OFFICIAL CQC-COMPLIANT ELABORATE KNOWLEDGE REPOSITORY (<0.001s LATENCY GUARANTEE)
# Embedded directly in app.py for instant execution and zero container cache delay
# ==============================================================================

OFFICIAL_RESPONSES = {
    "phone": (
        "You can reach Cambridge Care Services directly by telephone on **07917 611 425** or **07878 455 347**.\n\n"
        "*   **Head Office Address**: 15 Deal Grove, Sawston, Cambridge, Cambridgeshire, CB22 3DR.\n"
        "*   **Office Opening Hours**: Monday to Friday from 09:30 to 21:00, and Saturday from 10:00 to 15:00.\n"
        "*   **24/7 Emergency Support**: We operate a 24-hour on-call support line dedicated to active clients, their families, and on-duty care staff for any urgent care schedule adjustments or evening peace of mind.\n"
        "*   **Email Inquiries**: You can also reach our administrative and coordination team directly at **info@cambridgecareservices.co.uk**.\n\n"
        "Whether you are exploring care options for the first time or need immediate support, our local team is always available to assist."
    ),
    "pricing": (
        "At Cambridge Care Services, we are committed to complete pricing transparency and operate a person-centered, bespoke fee structure tailored to your loved one's exact care requirements:\n\n"
        "*   **Transparent, Tailored Quotations**: Because every individual's needs differ, we do not publish arbitrary headline figures. Care rates depend on visit duration (e.g. 1-hour, 2-hour, or 3+ hour visits), visit frequency, time of day (daytime vs waking night vs sleep-in), and specialist skill level (e.g. complex clinical care vs companionship).\n"
        "*   **Clear Written Agreement**: Following your free in-home assessment, you receive a full, written, itemized quotation. There are **zero hidden administration fees**, no unexpected setup charges, and no unannounced rate increases.\n"
        "*   **Council Direct Payments**: If you are eligible for social care funding through Cambridgeshire County Council, you have the legal right to request Direct Payments. This allows you to choose Cambridge Care Services directly rather than council-allocated providers.\n"
        "*   **NHS Continuing Healthcare (CHC)**: For clients with primary complex health or nursing needs, care may be **100% funded by the NHS**. We coordinate directly with your NHS Integrated Care Board (ICB).\n"
        "*   **Attendance Allowance / PIP**: Non-means-tested state benefits (£72.65 to £108.55 per week) available to help support home care costs regardless of your personal savings.\n\n"
        "To discuss your budget, explore funding options, and receive a free personalized quote, please call our Sawston care team on **07917 611 425**."
    ),
    "all_services": (
        "Cambridge Care Services is a regulated home care provider registered with the Care Quality Commission (CQC), delivering high-quality, compassionate care across Cambridge and South Cambridgeshire:\n\n"
        "1.  **Personal Care**: Respectful support with morning, afternoon, and evening routines, including washing, bathing, showering, oral hygiene, dressing, grooming, continence care, and catheter/stoma management.\n"
        "2.  **Specialist Dementia & Alzheimer's Care**: Person-centered support focused on maintaining familiar routines, gentle communication, de-escalation for anxiety or sundowning, and comforting companionship in familiar home surroundings.\n"
        "3.  **Companionship & Day Assistance**: Combatting loneliness through friendly conversation, accompaniment to GP appointments or local shops, hobby engagement, and nutritious meal preparation.\n"
        "4.  **Medication Management**: Safe administration and prompting of prescribed tablets, blister packs, and eye drops, all recorded on formal Medication Administration Records (MAR) under strict CQC clinical guidelines.\n"
        "5.  **Night Care Support**: Waking nights (carer awake all night to support with medication, repositioning, and nocturnal restlessness) and Sleeping nights (carer sleeps on-site for peace of mind).\n"
        "6.  **24/7 Live-In Care**: A dedicated, full-time professional carer residing in the home, offering an unhurried, dignified alternative to moving into a residential care home.\n"
        "7.  **Complex Care & Hospital Discharge**: Post-stroke rehabilitation, neurological support, and reablement care coordinated alongside NHS District Nurses and GPs.\n"
        "8.  **Palliative & End-of-Life Care**: Compassionate, dignified comfort care focusing on pain relief assistance and emotional family support during life's most sensitive moments.\n\n"
        "To discuss how we can tailor a care plan for your family, please call our team on **07917 611 425**."
    ),
    "dementia": (
        "Cambridge Care Services specializes in compassionate, person-centered **Dementia and Alzheimer's home care** across Sawston, Cambridge City, and South Cambridgeshire:\n\n"
        "*   **Familiar Surroundings & Established Routines**: Remaining in one's own home surrounded by cherished memories, pets, and lifelong routines is proven to reduce stress and disorientation for individuals living with memory loss.\n"
        "*   **Unhurried Daytime Support**: Our carers provide patient assistance with morning routines, nutritious meal preparation, afternoon tea, medication prompting, stimulating memory activities, and gentle mobility.\n"
        "*   **Gentle De-escalation & Emotional Reassurance**: We understand that late afternoons can sometimes trigger restlessness or anxiety (sundowning). Our staff are trained in empathetic communication and calming strategies to ensure your loved one feels safe and understood.\n"
        "*   **Small, Consistent Care Teams**: We assign consistent carers so your loved one sees familiar, friendly faces every day rather than rotating strangers, fostering genuine trust and emotional security.\n"
        "*   **Free In-Home Assessment**: Our Registered Care Manager visits your family home to complete an in-depth care consultation and craft a bespoke Dementia Support Plan.\n\n"
        "Please call our Sawston care coordinators directly on **07917 611 425** to discuss daytime support or book your free assessment."
    ),
    "coverage_all": (
        "Cambridge Care Services is headquartered directly in **Sawston** (15 Deal Grove, CB22 3DR) and proudly delivers CQC-regulated home care across Cambridge City and South Cambridgeshire:\n\n"
        "*   **South Cambridgeshire Core Hub**: Sawston, Great Shelford, Little Shelford, Stapleford, Babraham, Pampisford, Whittlesford, Duxford, Linton, Fulbourn, Hinxton, and Newton.\n"
        "*   **Cambridge City & Suburbs**: Postcodes **CB1, CB2, CB3, CB4, and CB5** (including Trumpington, Cherry Hinton, Newnham, and Chesterton).\n"
        "*   **Surrounding Regional Villages**: Full coverage across **CB21, CB22, CB23, CB24, and CB25** (such as Cambourne, Histon, Impington, Cottenham, and Waterbeach).\n"
        "*   **Flexible Border Policy**: If your loved one resides in bordering towns such as Royston, Haverhill, Newmarket, or Ely, our management team assesses local carer availability and can often accommodate care packages.\n\n"
        "Please contact our Sawston office directly on **07917 611 425** to confirm immediate carer availability for your specific postcode."
    ),
    "personal_care": (
        "Our CQC-regulated personal care services are delivered with the utmost dignity, compassion, and respect for personal privacy:\n\n"
        "*   **Morning & Bedtime Routines**: Gentle assistance getting out of bed, settling into bed, safe transfer support, and ensuring comfortable positioning.\n"
        "*   **Washing & Bathing**: Respectful, unhurried help with showering, bathing, bed baths, hair washing, skin care, and oral hygiene.\n"
        "*   **Dressing & Grooming**: Supporting clients in choosing their preferred clothes, putting on compression hosiery, and grooming according to personal taste.\n"
        "*   **Continence & Toilet Support**: Discreet, dignified assistance with personal toileting, catheter management, and stoma care support.\n"
        "*   **Medication Administration**: Prompting or administering prescribed medicines on strict schedules, fully audited on Medication Administration Records (MAR).\n\n"
        "To arrange a free in-home consultation, please call our care team on **07917 611 425**."
    ),
    "night_care": (
        "We provide dedicated overnight care across Cambridge and South Cambridgeshire to give clients round-the-clock safety and family carers restful peace of mind:\n\n"
        "*   **Waking Night Support**: A trained carer stays awake throughout the entire night to assist with scheduled medications, frequent repositioning, bathroom assistance, and calming nocturnal disorientation or falls prevention.\n"
        "*   **Sleeping Night Support**: A carer sleeps in a spare room at the client's home, on hand up to twice during the night for unexpected care needs, reassurance, or toileting support.\n"
        "*   **Respite Cover**: Short-term night cover whether you need support for a few nights, during recovery from an illness, or while primary family carers take a well-deserved break.\n\n"
        "To discuss night care rotas and book an assessment, call our team on **07917 611 425**."
    ),
    "live_in_care": (
        "Our Live-In Care service provides a dedicated, full-time professional carer residing with your loved one in their own home:\n\n"
        "*   **24/7 One-to-One Peace of Mind**: A compassionate, dignified alternative to moving into a residential care home. Your loved one receives 100% personalized attention.\n"
        "*   **Preserving Home, Memories & Pets**: Clients remain in the comfort of their familiar surroundings, sleep in their own bed, keep their cherished pets, and welcome family whenever they wish.\n"
        "*   **Comprehensive Daily Support**: Covers personal care, freshly prepared meals, light housekeeping, medication administration, companionship, and night-time presence.\n"
        "*   **Carefully Matched Carers**: Carers are matched based on personality, shared interests, dietary skills, and clinical care requirements.\n\n"
        "To discuss live-in care arrangements with our Registered Care Manager, call **07917 611 425**."
    ),
    "medication": (
        "Medication management is delivered under rigorous Care Quality Commission (CQC) safety standards:\n\n"
        "*   **Prompting & Administration**: Our care assistants prompt or safely administer prescribed oral tablets, liquids, topical creams, eye drops, and blister packs.\n"
        "*   **MAR Sheet Auditing**: Every single dose is recorded and verified on Medication Administration Records (MAR) to ensure 100% compliance and zero missed doses.\n"
        "*   **Pharmacy & Prescription Coordination**: We liaise directly with your local Cambridgeshire GP surgeries and pharmacies to help coordinate repeat prescription deliveries.\n\n"
        "For medication support inquiries, please call our office on **07917 611 425**."
    ),
    "meals_cooking": (
        "Nutritious, enjoyable meals are a core part of maintaining strength, health, and happiness at home:\n\n"
        "*   **Freshly Cooked Meals**: Our carers prepare wholesome breakfasts, hot lunches, and evening suppers right in your kitchen, tailored strictly to personal preferences.\n"
        "*   **Special Dietary Requirements**: We cater for diabetic diets, low-sodium meals, vegetarian/vegan preferences, soft-food consistencies, and cultural or religious dietary requirements.\n"
        "*   **Hydration & Intake Monitoring**: Carers encourage fluid intake and monitor nutrition to prevent dehydration, urinary tract infections (UTIs), and unplanned weight loss.\n"
        "*   **Kitchen Care**: Carers wash dishes, wipe down surfaces, and maintain food safety standards.\n\n"
        "To discuss meal and daytime support, contact our team on **07917 611 425**."
    ),
    "companionship": (
        "Our Companionship and Day Assistance services are designed to prevent loneliness, encourage social connection, and support independent living:\n\n"
        "*   **Warm, Meaningful Companionship**: Engaging conversation, listening to music, reading mail, sharing memories, and participating in favorite hobbies.\n"
        "*   **Community Outings & Appointments**: Accompanying clients to local GP appointments, hospital clinics, cafes, garden centres, or shopping trips across Cambridge.\n"
        "*   **Daytime Assistance**: Unhurried visits (from 1 hour to full daytime blocks) helping with light housekeeping, meal preparation, and gentle mobility.\n\n"
        "To arrange daytime support for your parent or family member, call **07917 611 425**."
    ),
    "funding": (
        "We guide families through all available home care funding pathways across Cambridgeshire:\n\n"
        "*   **Direct Payments (Council Funded)**: If eligible through Cambridgeshire County Council Social Services, you can request Direct Payments to select Cambridge Care Services directly rather than council-allocated providers.\n"
        "*   **NHS Continuing Healthcare (CHC)**: If approved for NHS CHC due to complex health needs, the NHS covers 100% of care costs. We coordinate directly with your NHS Integrated Care Board (ICB).\n"
        "*   **Attendance Allowance / PIP**: Non-means-tested government benefits (£72.65 to £108.55/week) to help fund home care support without affecting your savings or pension.\n"
        "*   **Self-Funded (Private Pay)**: Transparent, itemized invoicing with no hidden management fees following your free assessment.\n\n"
        "Call our care advisors on **07917 611 425** to discuss your funding options."
    ),
    "assessment": (
        "Arranging a free, no-obligation home care assessment with Cambridge Care Services is a straightforward 3-step process:\n\n"
        "1.  **Initial Consultation Call**: Contact our care coordinators on **07917 611 425** (Mon-Fri, 9:30am-9pm) to discuss immediate needs, care preferences, and visit schedules.\n"
        "2.  **In-Person Home Assessment**: Our Registered Care Manager visits you and your family in Cambridge or South Cambridgeshire to assess daily routines, mobility, home safety, and medical history.\n"
        "3.  **Bespoke Care Plan & Quotation**: We draft a detailed, person-centered Care Plan and provide a transparent, itemized written quote.\n\n"
        "There is zero obligation, and for urgent post-hospital discharge situations, care can often commence within **24 to 48 hours**."
    ),
    "careers": (
        "Cambridge Care Services is actively recruiting compassionate Care Assistants and Senior Support Workers across Cambridge and South Cambridgeshire:\n\n"
        "*   **Entry Requirements**: Compassion, empathy, right to work in the UK, valid UK driving licence with access to a reliable vehicle, and a clear Enhanced DBS check.\n"
        "*   **Comprehensive Paid Training**: We fund your **Care Certificate** induction and provide paid shadow shifts alongside experienced senior carers-no prior experience required for entry roles.\n"
        "*   **Pay & Benefits**: Competitive pay rates above the National Living Wage (with higher weekend and Bank Holiday rates), paid mileage allowance (45p/mile), paid travel time between visits, and guaranteed-hours contracts.\n\n"
        "To apply, visit our website careers section or contact our recruitment team directly on **07917 611 425**."
    ),
    "cqc_leadership": (
        "Cambridge Care Services is fully regulated by the **Care Quality Commission (CQC)** and operates under high clinical standards:\n\n"
        "*   **Registered Manager**: Mr. Rudrayya Mathapati, an experienced clinical leader and former NHS Nurse Team Leader with extensive nursing and community care experience.\n"
        "*   **Official CQC Registration**: Registered since 17 March 2022 (Head Office: 15 Deal Grove, Sawston, Cambridge, CB22 3DR).\n"
        "*   **Rigorous Staff Vetting**: Every care assistant undergoes an Enhanced DBS check, verified employment history, and multiple professional reference checks.\n"
        "*   **Carer Continuity & Quality Spot Checks**: We prioritize consistent carer allocation and conduct regular unannounced quality spot checks to ensure the highest standards of safety and dignity.\n\n"
        "Please call our office on **07917 611 425** to speak directly with our Registered Care Manager."
    ),
    "emergency": (
        "⚠️ **Medical Emergency Protocol**:\n\n"
        "*   **Life-Threatening Situations**: If someone has suffered a severe fall, chest pain, difficulty breathing, acute trauma, or loss of consciousness, please call **999** immediately for an ambulance.\n"
        "*   **Urgent Non-Emergency Health Advice**: For urgent medical guidance that is not life-threatening, call NHS **111**.\n"
        "*   **Cambridge Care On-Call Line**: For existing clients needing urgent care visit adjustments, our 24/7 emergency support line is **07917 611 425**."
    ),
    "out_of_area": (
        "Thank you for contacting Cambridge Care Services. We are a CQC-regulated home care provider focused exclusively "
        "on **Cambridge City and South Cambridgeshire** (postcodes CB1-CB5, CB21-CB25).\n\n"
        "We do not provide care services outside Cambridgeshire. If you need care support for a loved one "
        "living in Cambridge or surrounding South Cambs villages, please contact our team directly on **07917 611 425**."
    ),
    "greeting": (
        "Hello! I am your virtual care advisor for **Cambridge Care Services**.\n\n"
        "How can I support you and your family today? You can tap any of the **Popular Inquiries** above, or ask below about:\n"
        "*   **Home Care Services** (Personal care, Dementia support, Night care, Companionship, Live-in care)\n"
        "*   **Areas Covered** (Sawston, Great & Little Shelford, Duxford, Cambridge postcodes CB1-CB5, CB21-CB25)\n"
        "*   **Funding Support** (Direct Payments, NHS Continuing Healthcare, Attendance Allowance)\n"
        "*   **Arranging a Free In-Home Assessment** (Call our Sawston team on 07917 611 425)"
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
        is_sawston = any(s in q for s in ["sawston", "swaston"])
        loc_str = "in Sawston and South Cambridgeshire" if is_sawston else "across Cambridge and South Cambridgeshire"
        
        # Identify family relative if mentioned
        relative = "your loved one"
        pronoun = "her"
        for rel, p in [
            ("mother", "her"), ("mum", "her"), ("mom", "her"), ("aunt", "her"), ("grandmother", "her"), ("grandma", "her"), ("wife", "her"), ("sister", "her"),
            ("father", "him"), ("dad", "him"), ("uncle", "him"), ("grandfather", "him"), ("grandpa", "him"), ("husband", "him"), ("brother", "him"),
            ("parent", "them")
        ]:
            if rel in q:
                relative = f"your {rel.capitalize()}"
                pronoun = p
                break
        
        possessive = "their" if pronoun == "them" else ("his" if pronoun == "him" else "her")

        schedule_text = ""
        if any(h in q for h in ["hour", "hours", "3pm", "6pm", "time", "schedule", "afternoon"]):
            schedule_text = ", including tailored visit schedules (such as 2-to-3-hour daytime visits or dedicated afternoon blocks)"

        return (
            f"Yes, absolutely. Cambridge Care Services provides dedicated, person-centered **Dementia and Alzheimer's home care** for **{relative}** {loc_str}{schedule_text}.\n\n"
            f"We understand how vital it is for families to find compassionate, dependable care for a loved one living with memory loss. Our service is designed to maintain {possessive} dignity, safety, and comfort in {possessive} own familiar home surroundings:\n\n"
            f"*   **Familiar Surroundings & Consistent Routines**: Remaining in one's own home surrounded by cherished memories, pets, and lifelong routines is clinically proven to reduce stress, disorientation, and confusion for individuals living with dementia. Our carers maintain consistent daily schedules tailored to {possessive} personal rhythm.\n"
            f"*   **Empathetic Daytime & Personal Care**: Our carers provide unhurried, patient support with morning routines, dignified bathing and dressing, preparing wholesome meals, afternoon tea, gentle mobility, stimulating memory activities, and reassuring companionship.\n"
            f"*   **Late-Afternoon Reassurance & Sundowning Support**: We understand that late afternoons can sometimes trigger restlessness, anxiety, or confusion (sundowning). Our staff are specially trained in gentle de-escalation, empathetic communication, and calming evening settling routines to ensure {relative} feels safe, understood, and relaxed.\n"
            f"*   **Small, Consistent Care Teams**: We assign a small, dedicated care team so {relative} sees the same trusted, friendly faces every day rather than rotating strangers, fostering genuine emotional comfort, continuity, and mutual trust.\n"
            f"*   **Flexible Visit Schedules**: We tailor visit durations to your family's exact needs-whether that is 1-hour visits, unhurried 2-to-3-hour daytime blocks (such as 3:00 PM to 6:00 PM), waking nights, or round-the-clock live-in care.\n"
            f"*   **Free In-Home Care Assessment**: Our Registered Care Manager, **Mr. Rudrayya Mathapati**, will visit your family home for an unhurried, no-obligation assessment to listen to your wishes and design a bespoke Dementia Support Plan.\n\n"
            f"To discuss {relative}'s care needs or book a free assessment, please call our Sawston care team directly on **07917 611 425** (Mon-Fri 09:30-21:00, Sat 10:00-15:00, with 24/7 on-call manager support)."
        )
    # 6. Specific covered locations
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
                f"*   **Comprehensive Services Available**: Personal care, dementia support, companionship, freshly prepared meals, medication management, and overnight waking care.\n"
                f"*   **Free In-Home Assessment**: Our Registered Care Manager can visit your home in {matched_town} for an unhurried, no-obligation care consultation.\n\n"
                f"Please call our local care team directly on **07917 611 425** to confirm immediate carer availability for {matched_town}."
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

def get_care_response(user_input: str) -> str:
    # 1. Instant domain intent routing directly in app.py (<0.001s)
    routed = route_query_intent(user_input)
    if routed:
        return routed
    
    # 2. Dynamic RAG retrieval fallback
    try:
        import rag
        return rag.ask_cambridge_care_bot(user_input)
    except Exception:
        return OFFICIAL_RESPONSES["all_services"]

# ----------------- USER CHAT CONVERSATION (METHOD B) -----------------
user_input = st.chat_input("Ask about care services, locations, funding...")

has_history = len(st.session_state.chat_history) > 0

# Case 1: Fresh visit - show welcome greeting
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
        response = get_care_response(user_input)
        st.write(response)

    # Save to history without st.rerun() to prevent connection blips or lost state
    st.session_state.chat_history.append({
        "question": user_input,
        "answer": response
    })

# Case 3: Page re-render or tab click - show folded past + latest in full view
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
