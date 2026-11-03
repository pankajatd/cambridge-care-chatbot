# Test Execution Report: Cambridge Care Services AI Chatbot

**Project Path:** `C:\Pankaja\CAMBRIDGE_CARE_SERVICES_CHATBOT`  
**Test Suite:** Unit & Retrieval Verification  
**Status:** Complete (6/6 Tests Passed Successfully)  
**Date:** November 2026  

---

## Section 1: Local Drive In-Memory Tests (TC-01 to TC-06)

| Test Case ID | Test Description | Files / Scope Tested | Result |
| :---: | :--- | :--- | :---: |
| **TC-01** | Knowledge Document Ingestion & Chunking | All 5 `.txt` source files in workspace | **PASSED** ✅ |
| **TC-02** | Geographic Coverage Retrieval (Sawston / CB22) | `02_coverage_and_locations.txt` | **PASSED** ✅ |
| **TC-03** | Care Services Retrieval (Dementia / Alzheimer's) | `01_about_and_services.txt` | **PASSED** ✅ |
| **TC-04** | Leadership & CQC Verification (Rudrayya Mathapati) | `05_leadership_funding_and_compliance.txt` | **PASSED** ✅ |
| **TC-05** | Onboarding & 24–48h Start Time FAQs | `03_process_and_faqs.txt` | **PASSED** ✅ |
| **TC-06** | Recruitment, DBS & Driver Criteria | `04_careers_and_recruitment.txt` | **PASSED** ✅ |

---

## Section 2: ChromaDB Vector Database Tests (CDB-01 to CDB-05)

| ChromaDB Test ID | Test Description | Natural Language Query | Top Retrieved Source | Result |
| :---: | :--- | :--- | :--- | :---: |
| **CDB-01** | Geographic Coverage & Postcodes | *"What areas and postcodes do you cover in Sawston...?"* | `02_coverage_and_locations.txt` | **PASSED** ✅ |
| **CDB-02** | Specialist Care (Dementia / Alzheimer's) | *"Do you provide specialist care for Alzheimer's...?"* | `01_about_and_services.txt` | **PASSED** ✅ |
| **CDB-03** | Leadership & Legal CQC Registration | *"Who is Registered Manager Rudrayya Mathapati...?"* | `05_leadership_funding_and_compliance.txt` | **PASSED** ✅ |
| **CDB-04** | Onboarding & 24–48h Hospital Discharge | *"How quickly can care start after hospital discharge...?"* | `03_process_and_faqs.txt` | **PASSED** ✅ |
| **CDB-05** | Recruitment Criteria & Carer DBS Checks | *"What are the entry requirements and background checks...?"* | `04_careers_and_recruitment.txt` / `03` | **PASSED** ✅ |

---

## Detailed Test Logs

### Test Case 1: Knowledge Document Ingestion & Chunking (TC-01)
* **Objective:** Verify all 5 `.txt` knowledge documents exist on disk, are readable with UTF-8 encoding, and are correctly segmented into semantic paragraphs (chunks).
* **Execution Timestamp:** 2026-11-02 22:10 UTC
* **Individual File Verification:**
  1. `01_about_and_services.txt` $\rightarrow$ **12 chunks loaded** (Personal care, Live-in, Dementia, Complex, Respite, Night care, etc.)
  2. `02_coverage_and_locations.txt` $\rightarrow$ **5 chunks loaded** (CB1–CB5, CB21–CB25, villages, out-of-area policy)
  3. `03_process_and_faqs.txt` $\rightarrow$ **8 chunks loaded** (3-step onboarding, 24–48h start, DBS, funding)
  4. `04_careers_and_recruitment.txt` $\rightarrow$ **5 chunks loaded** (Roles, Right to work, driving license, training)
  5. `05_leadership_funding_and_compliance.txt` $\rightarrow$ **7 chunks loaded** (Registered manager, CQC history, council funding, 999/111 safety)
* **Metrics:**
  * **Files Loaded:** 5 / 5 (100%)
  * **Total Semantic Chunks Created:** 37 chunks
* **Result:** **PASSED ✅**

---

### Test Case 2: Geographic Coverage Retrieval (TC-02)
* **Objective:** Verify that asking about a local postcode or village (*"Does Cambridge Care Services cover Sawston CB22?"*) correctly retrieves geographic coverage facts.
* **Execution Timestamp:** 2026-11-02 22:26 UTC
* **Query Evaluated:** `"Does Cambridge Care Services cover Sawston CB22?"`
* **Retrieved Results:**
  * **Match #1:** `02_coverage_and_locations.txt` $\rightarrow$ Pulled the Postcode list containing `CB22: Sawston, Great Shelford, Little Shelford...`
  * **Match #2:** `01_about_and_services.txt` $\rightarrow$ Pulled the Office base confirming `15 Deal Grove, Sawston, CB22 3DR`
* **Assertions Verified:**
  * Target file `02_coverage_and_locations.txt` located: **TRUE**
  * Keyword `"Sawston"` present in retrieved context: **TRUE**
  * Keyword `"CB22"` present in retrieved context: **TRUE**
* **Result:** **PASSED ✅**

---

### Test Case 3: Specialist Care Services Retrieval (TC-03)
* **Objective:** Verify that inquiries regarding Alzheimer's and memory support accurately pull specialist Dementia care protocols.
* **Execution Timestamp:** 2026-11-02 22:27 UTC
* **Query Evaluated:** `"Do you provide specialist care for people with Alzheimer's disease and dementia?"`
* **Retrieved Results:**
  * **Match #1:** `01_about_and_services.txt` $\rightarrow$ Pulled Section 3: *Dementia Care: Specialist support for individuals living with Alzheimer's disease, vascular dementia... gentle reassurance, de-escalation strategies.*
  * **Match #2:** `05_leadership_funding_and_compliance.txt` $\rightarrow$ Pulled NHS Continuing Healthcare details covering advanced dementia care.
* **Assertions Verified:**
  * Target file `01_about_and_services.txt` located: **TRUE**
  * Keyword `"Alzheimer's"` present in retrieved context: **TRUE**
  * Keyword `"Dementia"` present in retrieved context: **TRUE**
* **Result:** **PASSED ✅**

---

### Test Case 4: Leadership, CQC & Compliance Verification (TC-04)
* **Objective:** Verify that governance inquiries regarding the registered manager and legal CQC registration history are retrieved accurately.
* **Execution Timestamp:** 2026-11-02 22:29 UTC
* **Query Evaluated:** `"Who is Registered Manager Rudrayya Mathapati and when was the service registered with CQC?"`
* **Retrieved Results:**
  * **Match #1:** `05_leadership_funding_and_compliance.txt` $\rightarrow$ Pulled Section 1: *Registered Manager: Mr. Rudrayya Mathapati, Nurse Team Leader background, legal responsibility under CQC regulations, registered since 17 March 2022.*
  * **Match #2:** `01_about_and_services.txt` $\rightarrow$ Pulled CQC regulatory overview and Deal Grove, Sawston address.
* **Assertions Verified:**
  * Target file `05_leadership_funding_and_compliance.txt` located: **TRUE**
  * Keyword `"Rudrayya Mathapati"` present in retrieved context: **TRUE**
  * Keyword `"CQC"` present in retrieved context: **TRUE**
* **Result:** **PASSED ✅**

---

### Test Case 5: Client Onboarding & Fast Response Time (TC-05)
* **Objective:** Verify that families asking about emergency or rapid care start after a hospital discharge receive the accurate 24 to 48-hour timeline and onboarding pathway.
* **Execution Timestamp:** 2026-11-02 22:31 UTC
* **Query Evaluated:** `"How quickly can care start after hospital discharge, and what is the onboarding process?"`
* **Retrieved Results:**
  * **Match #1:** `03_process_and_faqs.txt` $\rightarrow$ Pulled FAQ: *Q: How quickly can care start? A: Urgent care or post-hospital discharge support can often be arranged within 24 to 48 hours following a completed assessment.*
  * **Match #2:** `01_about_and_services.txt` $\rightarrow$ Pulled Personal Care routine details.
* **Assertions Verified:**
  * Target file `03_process_and_faqs.txt` located: **TRUE**
  * Hospital discharge timeline retrieved: **TRUE**
  * 24–48 hour start window confirmed: **TRUE**
* **Result:** **PASSED ✅**

---

### Test Case 6: Recruitment Criteria & DBS Background Checks (TC-06)
* **Objective:** Verify that job inquiries regarding carer requirements pull the accurate UK Right to Work, Enhanced DBS check, and induction training facts.
* **Execution Timestamp:** 2026-11-02 22:32 UTC
* **Query Evaluated:** `"What are the entry requirements and background checks needed to apply as a care assistant?"`
* **Retrieved Results:**
  * **Match #1:** `04_careers_and_recruitment.txt` $\rightarrow$ Pulled Section: *Minimum Entry Requirements for Applicants (Right to Work in the UK, Enhanced DBS check, UK driving license preference, NVQ Level 2/3 or induction training).*
  * **Match #2:** `03_process_and_faqs.txt` $\rightarrow$ Pulled FAQ on carer vetting (Enhanced DBS, full employment history, minimum 2 professional references).
* **Assertions Verified:**
  * Target file `04_careers_and_recruitment.txt` located: **TRUE**
  * Keyword `"DBS"` present in retrieved context: **TRUE**
  * Keyword `"Requirements / Right to Work"` present in retrieved context: **TRUE**
* **Result:** **PASSED ✅**

---

## Section 2: Detailed ChromaDB Vector Database Logs

### ChromaDB Test 1: Geographic Coverage & Postcodes (CDB-01)
* **Vector Store Path:** `C:\Pankaja\CAMBRIDGE_CARE_SERVICES_CHATBOT\chroma_db`
* **Collection Name:** `cambridge_care_knowledge` (37 embedded vectors)
* **Query:** `"What areas and postcodes do you cover in Sawston and South Cambridgeshire?"`
* **Vector Match #1:** `02_coverage_and_locations.txt` $\rightarrow$ `PRIMARY POSTCODES COVERED: - CB1: Cambridge City Center... - CB22: Sawston, Great Shelford, Little Shelford...`
* **Result:** **PASSED ✅**

---

### ChromaDB Test 2: Specialist Care (Dementia / Alzheimer's) (CDB-02)
* **Query:** `"Do you provide specialist care for people with Alzheimer's disease and dementia?"`
* **Vector Match #1:** `01_about_and_services.txt` $\rightarrow$ `3. DEMENTIA CARE: Specialist support for individuals living with Alzheimer's disease, vascular dementia...`
* **Result:** **PASSED ✅**

---

### ChromaDB Test 3: Leadership & CQC Registration (CDB-03)
* **Query:** `"Who is Registered Manager Rudrayya Mathapati and when was the service registered with CQC?"`
* **Vector Match #1:** `05_leadership_funding_and_compliance.txt` $\rightarrow$ `1. LEADERSHIP & CQC REGISTRATION: Registered Manager: Mr. Rudrayya Mathapati... Registered since 17 March 2022.`
* **Result:** **PASSED ✅**

---

### ChromaDB Test 4: Onboarding & Hospital Discharge Response (CDB-04)
* **Query:** `"How quickly can care start after hospital discharge, and what is the onboarding process?"`
* **Vector Match #1:** `03_process_and_faqs.txt` $\rightarrow$ `Q: How quickly can care start? A: Urgent care or post-hospital discharge support can often be arranged within 24 to 48 hours...`
* **Result:** **PASSED ✅**

---

### ChromaDB Test 5: Recruitment Criteria & DBS Background Checks (CDB-05)
* **Query:** `"What are the entry requirements and background checks needed to apply as a care assistant?"`
* **Vector Match #1 & #2:** `03_process_and_faqs.txt` & `04_careers_and_recruitment.txt` $\rightarrow$ Enhanced DBS check, UK Right to Work, and driver criteria.
* **Result:** **PASSED ✅**

---

## Conclusion
Both the Local Drive verification and the ChromaDB Vector Database verification have achieved **100% test passage (11 out of 11 total tests passed)**. The vector database is persistently stored on disk and accurately retrieves the official Cambridge Care Services knowledge chunks in milliseconds.
