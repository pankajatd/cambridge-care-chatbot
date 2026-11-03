# 🌸 Cambridge Care Services — AI Virtual Care Advisor

> **A Domain-Specific, CQC-Compliant RAG Assistant for Home Care Services across Cambridge, Sawston (CB22), and South Cambridgeshire.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg)](https://streamlit.io/)
[![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-orange.svg)](https://www.trychroma.com/)
[![LLM](https://img.shields.io/badge/LLM-Google%20Gemini-4285F4.svg)](https://ai.google.dev/)
[![CQC](https://img.shields.io/badge/CQC-Regulated%20Provider-E02424.svg)](https://www.cqc.org.uk/)

---

## 📖 Overview

The **Cambridge Care Services AI Assistant** is an intelligent, retrieval-augmented virtual advisor designed to help individuals, families, and jobseekers navigate home care options. Built specifically for **Cambridge Care Services** ([https://www.cambridgecareservices.co.uk](https://www.cambridgecareservices.co.uk)), this application pairs a persistent local vector database (**ChromaDB**) with **Google Gemini** language models to provide accurate, compassionate, and strictly compliant information.

The user interface is tailored to reflect the authentic branding of the care team: **Nurse Uniform Slate Grey (`#3A4046` / `#282D32`)** accented with **Blossom Rose-Pink piping (`#F66A71` / `#C43F4A`)** and official brand marks.

---

## 🌟 Key Capabilities

1. **Free Assessment Guidance:** Direct booking instructions for complimentary in-home needs and risk assessments across Cambridgeshire.
2. **Local Coverage Checking:** Instant verification of coverage across **Sawston (CB22)**, Cambridge City, Shelford, Duxford, Whittlesford, Pampisford, and surrounding South Cambs villages.
3. **Care Funding Pathways:** Clear navigation of NHS Continuing Healthcare (CHC), Local Authority Social Care Direct Payments, and private self-funding.
4. **Care Careers & Recruitment:** Guidance on entry requirements, full training, Care Certificate pathways, and DBS compliance for prospective carers.
5. **CQC Healthcare Safety Guardrails:** Strict operational boundaries preventing medical diagnostics or prescription advice, always prioritizing emergency escalation (`999` / `111`) and immediate telephone contact (`07917 611 425`).
6. **Unified Responsive UI:** Purpose-built CSS ensuring a seamless experience across desktop monitors, laptops, tablets, and mobile phones, with:
   - 4 horizontal quick-inquiry chips in a single row without awkward vertical stacking.
   - Highlighted query window with Rose-Pink focus ring and zero scrollbars.
   - Accordion view for past inquiries to keep the viewport tidy.

---

## 🏗️ Architecture

```
User Query (Chat Input / Quick Action Chip)
                   │
                   ▼
       In-Memory Response Cache
         ├── [Hit]  ──► Instant Response (<10ms)
         └── [Miss] ──► Query ChromaDB Vector Store
                              │
                              ▼
            Top-3 Document Chunks Retrieved
                              │
                              ▼
               Gemini Prompt Assembly
        (Care Guidelines + CQC Guardrails + Context)
                              │
                              ▼
            Multi-Model Fallback Pool
        [gemini-flash-lite-latest ──► gemini-2.5-flash-lite ──► gemini-3-flash-preview]
                              │
                              ▼
           Compassionate, Verified Answer
```

---

## 📁 Repository Structure

```
CAMBRIDGE_CARE_SERVICES_CHATBOT/
├── 01_about_and_services.txt                # Knowledge base: Home care, dementia, respite, palliative
├── 02_coverage_and_locations.txt            # Knowledge base: Postcodes, towns, travel zones
├── 03_process_and_faqs.txt                  # Knowledge base: Assessment steps, carer matching, hours
├── 04_careers_and_recruitment.txt           # Knowledge base: Carer roles, qualifications, benefits
├── 05_leadership_funding_and_compliance.txt # Knowledge base: CQC standards, NHS CHC, Direct Payments
├── chroma_db/                               # Persistent local vector database (37 embedded chunks)
├── app.py                                   # Streamlit frontend with responsive branded styling
├── rag.py                                   # RAG engine: ChromaDB retrieval, caching, Gemini fallback
├── logo-mark.png                            # Official transparent brand emblem
├── home-hero.jpg                            # Official hero photograph showcasing care team
├── cqc-logo.png                             # Official CQC compliance badge
├── requirements.txt                         # Python package dependencies
├── .gitignore                               # Git security exclusions (protects .env)
└── README.md                                # Project documentation
```

---

## 🚀 Local Installation & Running

### 1. Prerequisites
- **Python 3.10+** (Tested on Python 3.10 – 3.14)
- A **Google Gemini API Key** ([Get a free key at Google AI Studio](https://aistudio.google.com/))

### 2. Clone the Repository
```bash
git clone https://github.com/pankajatd/cambridge-care-chatbot.git
cd cambridge-care-chatbot
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Your API Key
Create a `.env` file in the project root directory:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 5. Launch the Streamlit App
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ Deploying to Streamlit Community Cloud

1. **Push to GitHub:** Commit your project code and push to a **Private** or Public repository on GitHub.
2. **Connect to Streamlit Cloud:**
   - Log in at [share.streamlit.io](https://share.streamlit.io/).
   - Click **"New App"** and select your GitHub repository (`cambridge-care-chatbot`).
   - Set **Main file path** to `app.py`.
3. **Configure Secrets (Crucial):**
   - In the deployment screen, open **Advanced settings** ➔ **Secrets**.
   - Paste your key in TOML format:
     ```toml
     GEMINI_API_KEY = "your_actual_gemini_api_key_here"
     ```
   - Click **Deploy!**
4. **Share Public Beta URL:** Streamlit will provide a live URL (e.g. `https://cambridge-care-chatbot.streamlit.app`) accessible from any laptop or mobile phone.

---

## 🔒 Security & CQC Healthcare Disclaimers

- **Zero Medical Advice:** This assistant provides information on services, operational hours, funding, and recruitment. It does not provide clinical diagnoses, prescribe treatment, or replace qualified medical professionals.
- **Emergency Situations:** The assistant instructs users to immediately call **999** for life-threatening emergencies or **111** for urgent NHS clinical guidance.
- **Credential Protection:** Local `.env` files are excluded via `.gitignore` to guarantee API keys are never published to public source control.

---

## 📞 Provider Contact Information

**Cambridge Care Services**  
- **Office / Hub:** Sawston, Cambridge (CB22)  
- **Coverage:** Cambridge City & South Cambridgeshire  
- **Telephone:** [07917 611 425](tel:07917611425)  
- **Official Website:** [www.cambridgecareservices.co.uk](https://www.cambridgecareservices.co.uk)  
- **Regulator:** Care Quality Commission (CQC)
