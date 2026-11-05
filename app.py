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
        ("cambridge", "in Cambridge and South Cambridgeshire", "Cambridge"),
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

    # 2. Out of Area
    out_of_area_cities = ["london", "manchester", "birmingham", "leeds", "glasgow", "edinburgh", "liverpool", "bristol", "sheffield", "cardiff", "belfast", "scotland", "wales"]
    if any(city in q for city in out_of_area_cities):
        return (
            "Thank you for contacting Cambridge Care Services. We are a CQC-regulated home care provider focused exclusively "
            "on **Cambridge City and South Cambridgeshire** (postcodes CB1-CB5, CB21-CB25).\n\n"
            "We do not provide care services outside Cambridgeshire. If you need care support for a loved one "
            "living in Cambridge or surrounding South Cambs villages, please contact our team directly on **07917 611 425**."
        )

    # 3. Direct Contact Details
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
    
    has_nurse = any(k in q for k in ["nurse", "nurses", "nursing"])
    has_discharge = any(k in q for k in ["discharged", "hospital discharge", "hospital", "surgery"])
    has_male_carer = any(k in q for k in ["male nurse", "male carer", "male staff", "man carer", "male care assistant"])
    has_female_carer = any(k in q for k in ["female carer", "female nurse", "female staff", "woman carer"])

    # Base office text
    office_intro = (
        f"Because our head office is located right in **Sawston** (15 Deal Grove, CB22 3DR), our local carers are based within the village, "
        f"allowing us to provide prompt, dependable, and consistent visits tailored to {possessive} routines:\n\n"
        if is_sawston else
        f"Our local care team provides prompt, dependable, and consistent visits {loc_text}, tailored to {possessive} personal care plan:\n\n"
    )

    # 4. OVERNIGHT & NIGHT CARE (Evaluated when night/overnight is requested)
    if has_night:
        night_timing = f"({hours_mention or 'typically 10:00 PM to 7:00 AM'})"
        discharge_text = " following hospital discharge" if has_discharge else ""
        
        nurse_bullet = ""
        if has_nurse:
            nurse_bullet = (
                "*   **Overnight Care vs. Registered Nurse Distinction**: We provide trained **Overnight Care Assistants** who stay in the home through the night to assist with mobility, toileting, repositioning, and safety. If specialized clinical procedures (such as IV medications or sterile catheter care) are required, our overnight carers coordinate directly alongside NHS District Nurses.\n"
            )
            
        discharge_bullet = ""
        if has_discharge:
            discharge_bullet = (
                "*   **Immediate Hospital Discharge Handover**: Overnight care can be arranged to commence the very evening your loved one returns home from hospital to ensure a safe, smooth transition.\n"
            )
            
        condition_night_bullet = ""
        if any(k in q for k in ["parkinson", "parkinsons"]):
            condition_night_bullet = (
                "*   **Nocturnal Parkinson's Support**: Our overnight carers provide patient assistance with turning and repositioning in bed to relieve stiffness, managing nocturnal restlessness, and strict on-time administration of night medications.\n"
            )
        elif any(k in q for k in ["dementia", "alzheimer"]):
            condition_night_bullet = (
                "*   **Calming Nighttime Dementia Care**: Gentle reassurance, comforting communication, and supervision to prevent disorientation, anxiety, or wandering during the night.\n"
            )

        day_bullet = ""
        if has_day:
            day_bullet = (
                "*   **Combined Daytime Support**: Alongside overnight care, we can also provide daytime visits for nutritious meal preparation, morning/afternoon personal care, and companionship.\n"
            )

        return (
            f"Yes, absolutely. Cambridge Care Services provides dedicated, CQC-regulated **overnight care** for **{relative}** {loc_text}{discharge_text}:\n\n"
            f"{office_intro}"
            f"*   **Waking Night Support**: A trained, compassionate care assistant stays awake throughout the entire night {night_timing} to assist with bathroom visits, safe bed transfers, repositioning, medication prompting, and preventing nighttime falls or disorientation.\n"
            f"*   **Sleeping Night Support**: A carer sleeps on-site in a spare bedroom, available up to twice during the night for unexpected needs, reassurance, or assistance.\n"
            f"{nurse_bullet}"
            f"{condition_night_bullet}"
            f"{discharge_bullet}"
            f"{day_bullet}"
            f"*   **Consistent Night Carers**: Small, dedicated night teams so {relative} sees the same trusted, friendly faces each night rather than rotating strangers.\n\n"
            f"To discuss {relative}'s overnight care requirements and arrange a free consultation, please call our care coordination team directly on **07917 611 425** (Mon-Fri 09:30-21:00, Sat 10:00-15:00, with 24/7 on-call manager support)."
        )

    # 5. Parkinson's (Daytime or general)
    if any(k in q for k in ["parkinson", "parkinsons", "tremor", "rigidity", "neurological"]):
        return (
            f"Yes, absolutely. Cambridge Care Services provides dedicated, person-centered care for **{relative}** {loc_text}:\n\n"
            f"{office_intro}"
            f"*   **Specialist Parkinson's & Mobility Support**: Parkinson's symptoms vary significantly throughout the day and evening. Our carers assist with safe transfers, posture support, gentle mobility to reduce fall risks, and unhurried personal care that respects {possessive} pace and dignity.\n"
            f"*   **Time-Critical Medication Management**: In Parkinson's care, strict timing of prescribed medication is essential to minimize tremors and motor fluctuations (the 'on/off' effect). Our carers ensure prompt, accurate administration audited on Medication Administration Records (MAR) under strict CQC clinical guidelines.\n"
            f"*   **Daytime Companionship & Nutrition**: Preparing wholesome, nutritious meals, encouraging hydration, medication prompting, and providing compassionate companionship to keep {relative} engaged, comfortable, and safe in {possessive} familiar home surroundings.\n"
            f"*   **Small, Consistent Care Teams**: We assign a small, dedicated care team so {relative} sees the same trusted, friendly faces rather than rotating strangers, fostering genuine emotional comfort, continuity, and mutual trust.\n\n"
            f"To discuss {relative}'s care schedule or book a free assessment, please call our care team directly on **07917 611 425**."
        )

    # 6. Dementia & Alzheimer's (Daytime or general)
    if any(k in q for k in ["dementia", "demntia", "alzheimer", "alzheimers", "memory loss", "confusion", "cognitive"]):
        sched_note = f", including tailored visit schedules (such as {hours_mention or 'unhurried daytime visits'})" if (hours_mention or has_day) else ""
        return (
            f"Yes, absolutely. Cambridge Care Services provides dedicated, person-centered **Dementia and Alzheimer's home care** for **{relative}** {loc_text}{sched_note}.\n\n"
            f"{office_intro}"
            f"*   **Familiar Surroundings & Consistent Routines**: Remaining in one's own home surrounded by cherished memories, pets, and lifelong routines is clinically proven to reduce stress, disorientation, and confusion for individuals living with dementia. Our carers maintain consistent daily schedules tailored to {possessive} personal rhythm.\n"
            f"*   **Empathetic Daytime & Personal Care**: Our carers provide unhurried, patient support with morning routines, dignified bathing and dressing, preparing wholesome meals, afternoon tea, gentle mobility, stimulating memory activities, and reassuring companionship.\n"
            f"*   **Late-Afternoon Reassurance & Sundowning Support**: We understand that late afternoons can sometimes trigger restlessness, anxiety, or confusion (sundowning). Our staff are specially trained in gentle de-escalation, empathetic communication, and calming evening settling routines to ensure {relative} feels safe, understood, and relaxed.\n"
            f"*   **Small, Consistent Care Teams**: We assign a small, dedicated care team so {relative} sees the same trusted, friendly faces every day rather than rotating strangers, fostering genuine emotional comfort, continuity, and mutual trust.\n\n"
            f"To discuss {relative}'s care needs or book a free assessment, please call our care team directly on **07917 611 425**."
        )

    # 7. Stroke / Hospital Discharge / Reablement (Daytime)
    if has_discharge or any(k in q for k in ["stroke", "rehab", "reablement", "post-hospital"]):
        male_carer_bullet = ""
        opening_custom = f"Yes, absolutely. Cambridge Care Services provides specialized post-hospital and reablement care for **{relative}** {loc_text}:"
        
        if has_male_carer:
            opening_custom = f"Yes, absolutely. Cambridge Care Services can accommodate your request for a **male carer** to support **{relative}** {loc_text} following hospital discharge:"
            male_carer_bullet = (
                "*   **Male Carer Allocation for Dignity & Preference**: We fully respect client preferences for male or female carers. For personal care routines, washing, dressing, and daily assistance, a trained **male care assistant** can be dedicated to his care team.\n"
            )
            
        nurse_bullet = ""
        if has_nurse:
            nurse_bullet = (
                "*   **Carer vs. Registered Nurse Distinction**: Our staff are CQC-regulated Home Care Assistants and Support Workers rather than acute hospital ward nurses. However, our team works in direct coordination with NHS District Nurses and GPs for any clinical procedures.\n"
            )

        return (
            f"{opening_custom}\n\n"
            f"{office_intro}"
            f"{male_carer_bullet}"
            f"{nurse_bullet}"
            f"*   **Mobility Rebuilding & Safe Transfers**: Assisting with safe bed-to-chair transfers, walking practice, and prescribed physiotherapy exercises to regain physical strength and prevent fall injuries.\n"
            f"*   **Dignified Personal Care**: Respectful assistance with morning and evening routines, washing, dressing, and hygiene tailored to {possessive} recovery pace.\n"
            f"*   **Clinical & Medication Coordination**: Timely medication prompting on Medication Administration Records (MAR) and direct collaboration with NHS District Nurses and GPs.\n"
            f"*   **Nutritious Meal Preparation & Hydration**: Freshly cooking balanced meals and monitoring fluid intake to support healing and strength.\n"
            f"*   **Rapid Onboarding Guarantee**: For urgent hospital discharge reablement, care visits can often commence within **24 to 48 hours** following an in-home assessment.\n\n"
            f"To discuss {relative}'s hospital discharge date and arrange care, please call our care team on **07917 611 425**."
        )

    # 8. Respite Care
    if has_respite:
        return (
            f"Yes, Cambridge Care Services provides dedicated, CQC-regulated **Respite Care** for **{relative}** {loc_text}.\n\n"
            f"We understand that family caregiving is both deeply rewarding and physically demanding. Our respite care service provides primary family carers with restful peace of mind while they take a well-deserved break or holiday:\n\n"
            f"{office_intro}"
            f"*   **Flexible Cover Periods**: Whether you require respite cover for a few hours a week, several full days, overnight support, or full 1-to-2-week live-in cover while your family travels, we adapt to your exact timetable.\n"
            f"*   **Seamless Continuity of Care**: Our carers strictly follow {possessive} established daily routines, dietary preferences, and medication schedules so {relative} experiences zero disruption in their familiar home surroundings.\n"
            f"*   **Comprehensive In-Home Assistance**: Covers personal hygiene, morning/evening dressing, fresh home cooking, companionship, and medication administration on MAR records.\n"
            f"*   **Guaranteed Staff Cover**: You can travel with complete peace of mind knowing backup carer cover is guaranteed under our CQC operational guidelines.\n\n"
            f"To discuss your holiday dates and arrange a free respite assessment, please call our care team on **07917 611 425**."
        )

    # 9. 24/7 Live-In Care
    if has_live_in:
        return (
            f"Our 24/7 Live-In Care service provides a dedicated, full-time professional carer residing with **{relative}** {loc_text}:\n\n"
            f"{office_intro}"
            f"*   **24/7 One-to-One Peace of Mind**: A compassionate, dignified alternative to moving into a residential care home. Your loved one receives 100% personalized attention.\n"
            f"*   **Preserving Home, Memories & Pets**: Clients remain in their familiar home surroundings, sleep in their own bed, keep their pets, and welcome family whenever they wish.\n"
            f"*   **Comprehensive Daily Support**: Covers personal care, freshly prepared meals, light housekeeping, medication administration, companionship, and nighttime presence.\n"
            f"*   **Carefully Matched Carers**: Carers are matched based on personality, shared interests, dietary skills, and clinical care requirements.\n\n"
            f"To discuss live-in care arrangements, please call our care team on **07917 611 425**."
        )

    # 10. Chronic Health (Arthritis, Diabetes, Mobility, Wheelchair, Palliative)
    health_keywords = ["arthritis", "diabetes", "diabetic", "mobility", "fall", "falls", "palliative", "terminal", "cancer", "vision", "blind", "sensory", "catheter", "stoma", "incontinence", "pain", "wheelchair", "hoist", "frail", "frailty", "elderly", "aged"]
    if any(k in q for k in health_keywords):
        condition_mention = next((k.title() for k in health_keywords if k in q), "Physical Health & Mobility")
        return (
            f"Yes, absolutely. Cambridge Care Services provides specialized, person-centered home care for **{relative}** {loc_text}, tailored to support **{condition_mention}** and daily wellbeing:\n\n"
            f"{office_intro}"
            f"*   **Un-Hurried Daily Personal Care**: Respectful, patient support with morning wake-up routines, bathing, showering, dressing, and skin care designed to accommodate physical stiffness, pain, or limited mobility.\n"
            f"*   **Mobility Assistance & Fall Prevention**: Safe transfer assistance (bed, chair, commode), safe positioning, and gentle mobility encouragement to promote independence while strictly guarding against fall hazards.\n"
            f"*   **Strict Medication Clinical Governance**: Prescription prompting and administration recorded on formal Medication Administration Records (MAR) under CQC clinical guidelines.\n"
            f"*   **Wholesome Cooking & Nutritional Care**: Freshly cooking healthy meals tailored to special dietary requirements (such as diabetic-friendly, low-sodium, or soft textures) and monitoring daily hydration.\n"
            f"*   **Small, Consistent Care Teams**: Small teams of DBS-checked, Care Certificate-trained carers so {relative} builds trust with familiar friendly faces.\n\n"
            f"To discuss {relative}'s daily routine or book your free assessment, please call our care coordinators directly on **07917 611 425**."
        )

    # 11. Personal Care (Washing, Bathing, Dressing, Continence)
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

    # 12. Companionship & Day Assistance
    if any(k in q for k in ["companionship", "lonely", "loneliness", "outing", "outings", "day assistance", "befriending", "hobbies"]):
        return (
            f"Our Companionship and Day Assistance services for **{relative}** {loc_text} are designed to combat loneliness, encourage social connection, and support independent living:\n\n"
            f"{office_intro}"
            f"*   **Meaningful Social Connection**: Friendly conversation, reading mail, listening to music, sharing memories, and participating in favorite hobbies.\n"
            f"*   **Community Outings & Medical Appointments**: Accompaniment to GP appointments, hospital clinics, cafes, garden centres, or shopping trips across Cambridge.\n"
            f"*   **Unhurried Daytime Support**: Flexible visits (from 1-hour sessions to full daytime blocks) providing meal preparation, light housekeeping, and gentle mobility.\n\n"
            f"To arrange companionship visits, please contact our team on **07917 611 425**."
        )

    # 13. Pricing, Costs, and Funding
    if any(k in q for k in ["cost", "costs", "price", "prices", "pricing", "rate", "rates", "charge", "charges", "how much", "fee", "fees", "quote", "pay for care", "funding", "direct payment", "direct payments", "nhs", "chc", "continuing healthcare", "attendance allowance", "pip"]):
        return (
            "At Cambridge Care Services, we operate a person-centered, bespoke fee structure with complete pricing transparency:\n\n"
            "*   **Transparent, Tailored Quotations**: Because every individual's needs differ, care rates depend on visit duration (e.g. 1-hour, 2-hour, or 3+ hour visits), visit frequency, time of day (daytime vs waking night vs sleep-in), and specialist skill level.\n"
            "*   **Clear Written Agreement**: Following your free in-home assessment, you receive a full, written, itemized quotation. There are **zero hidden administration fees**, no unexpected setup charges, and no unannounced rate increases.\n"
            "*   **Council Direct Payments**: If eligible for social care through Cambridgeshire County Council, you have the legal right to request Direct Payments, allowing you to choose Cambridge Care Services directly.\n"
            "*   **NHS Continuing Healthcare (CHC)**: For clients with primary complex health or nursing needs, care may be **100% funded by the NHS**. We coordinate directly with your NHS Integrated Care Board (ICB).\n"
            "*   **Attendance Allowance / PIP**: Non-means-tested state benefits (£72.65 to £108.55 per week) available to help support home care costs regardless of your personal savings.\n\n"
            "To discuss your budget, explore funding options, and receive a free personalized quote, please call our care team on **07917 611 425**."
        )

    # 14. Assessment / Process / Booking
    if any(k in q for k in ["assessment", "arrange", "book", "start care", "consultation", "onboarding", "how do we begin"]):
        return (
            "Arranging a free, no-obligation home care assessment with Cambridge Care Services is a straightforward 3-step process:\n\n"
            "1.  **Initial Consultation Call**: Contact our care coordinators on **07917 611 425** (Mon-Fri 09:30-21:00, Sat 10:00-15:00) to discuss immediate needs, care preferences, and visit schedules.\n"
            "2.  **In-Person Home Assessment**: Our Care Manager visits your family home in Cambridge or South Cambridgeshire to assess daily routines, mobility, home safety, and medical history.\n"
            "3.  **Bespoke Care Plan & Quotation**: We draft a detailed, person-centered Care Plan and provide a transparent, itemized written quote.\n\n"
            "There is zero obligation, and for urgent post-hospital discharge situations, care can often commence within **24 to 48 hours**."
        )

    # 15. Careers & Recruitment
    if any(k in q for k in ["job", "jobs", "career", "careers", "hiring", "apply", "carer vacancy", "recruitment", "salary", "wage", "training"]):
        return (
            "Cambridge Care Services is actively recruiting compassionate Care Assistants and Senior Support Workers across Cambridge and South Cambridgeshire:\n\n"
            "*   **Entry Requirements**: Compassion, empathy, right to work in the UK, valid UK driving licence with access to a reliable vehicle, and a clear Enhanced DBS check.\n"
            "*   **Comprehensive Paid Training**: We fund your **Care Certificate** induction and provide paid shadow shifts alongside experienced senior carers-no prior experience required for entry roles.\n"
            "*   **Pay & Benefits**: Competitive pay rates above the National Living Wage (with higher weekend and Bank Holiday rates), paid mileage allowance (45p/mile), paid travel time between visits, and guaranteed-hours contracts.\n\n"
            "To apply, visit our website careers section or contact our recruitment team directly on **07917 611 425**."
        )

    # 16. CQC Regulation & Leadership
    if any(k in q for k in ["cqc", "regulated", "rating", "inspection", "manager", "mathapati", "rudrayya", "dbs", "background", "police"]):
        return (
            "Cambridge Care Services is fully regulated by the **Care Quality Commission (CQC)** and operates under high clinical standards:\n\n"
            "*   **Registered Manager**: Mr. Rudrayya Mathapati, an experienced clinical leader and former NHS Nurse Team Leader with extensive nursing and community care experience.\n"
            "*   **Official CQC Registration**: Registered since 17 March 2022 (Head Office: 15 Deal Grove, Sawston, Cambridge, CB22 3DR).\n"
            "*   **Rigorous Staff Vetting**: Every care assistant undergoes an Enhanced DBS check, verified employment history, and multiple professional reference checks.\n"
            "*   **Carer Continuity & Quality Spot Checks**: We prioritize consistent carer allocation and conduct regular unannounced quality spot checks to ensure the highest standards of safety and dignity.\n\n"
            "Please call our office on **07917 611 425** to speak directly with our Registered Care Manager."
        )

    # 17. Pure Location Inquiry
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
                f"*   **Comprehensive Services Available**: Personal care, dementia support, Parkinson's care, companionship, freshly prepared meals, medication management, and overnight waking care.\n"
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

    # 18. All Services Overview & Comprehensive Catch-All
    return (
        f"Cambridge Care Services is a regulated home care provider registered with the Care Quality Commission (CQC), delivering high-quality, compassionate care for **{relative}** {loc_text}:\n\n"
        f"{office_intro}"
        f"1.  **Personal Care**: Respectful support with morning, afternoon, and evening routines, including washing, bathing, showering, oral hygiene, dressing, grooming, continence care, and catheter/stoma management.\n"
        f"2.  **Specialist Dementia & Alzheimer's Care**: Person-centered support focused on maintaining familiar routines, gentle communication, de-escalation for anxiety or sundowning, and comforting companionship in familiar home surroundings.\n"
        f"3.  **Specialist Parkinson's & Neurological Care**: Mobility assistance, fall prevention, safe transfers, posture support, and time-critical medication prompting.\n"
        f"4.  **Companionship & Day Assistance**: Combatting loneliness through friendly conversation, accompaniment to GP appointments or local shops, hobby engagement, and nutritious meal preparation.\n"
        f"5.  **Medication Management**: Safe administration and prompting of prescribed tablets, blister packs, and eye drops, all recorded on formal Medication Administration Records (MAR) under strict CQC clinical guidelines.\n"
        f"6.  **Night Care Support**: Waking nights (carer awake all night to support with medication, repositioning, and nocturnal restlessness) and Sleeping nights (carer sleeps on-site for peace of mind).\n"
        f"7.  **Respite Care**: Flexible cover from a few hours a week to multi-week live-in cover while family caregivers rest or travel.\n"
        f"8.  **24/7 Live-In Care**: A dedicated, full-time professional carer residing in the home, offering an unhurried, dignified alternative to moving into a residential care home.\n"
        f"9.  **Complex Care & Hospital Discharge**: Post-stroke rehabilitation, neurological support, and reablement care coordinated alongside NHS District Nurses and GPs.\n"
        f"10. **Palliative & End-of-Life Care**: Compassionate, dignified comfort care focusing on pain relief assistance and emotional family support during life's most sensitive moments.\n\n"
        f"To discuss {relative}'s care needs and book a free in-home consultation, please call our care team on **07917 611 425**."
    )

def get_care_response(user_input: str) -> str:
    # 1. Instant multi-factor clinical & service intent routing (<0.001s)
    routed = route_care_inquiry(user_input)
    if routed:
        return routed
    
    # 2. Dynamic RAG retrieval fallback
    try:
        import rag
        return rag.ask_cambridge_care_bot(user_input)
    except Exception:
        return route_care_inquiry("services")

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
