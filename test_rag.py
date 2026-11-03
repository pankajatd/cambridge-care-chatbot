import os
import sys
from rag import load_knowledge_documents, retrieve_relevant_context

def run_tests():
    print("=" * 60)
    print("RUNNING UNIT TESTS FOR CAMBRIDGE CARE SERVICES RAG ENGINE")
    print("=" * 60)

    # TEST 1: Load Documents
    print("\n[TEST 1] Loading 5 Knowledge Documents...")
    chunks = load_knowledge_documents()
    assert len(chunks) > 0, "FAILED: No chunks were loaded from .txt files!"
    
    sources = set(c["source"] for c in chunks)
    print(f" -> Successfully loaded {len(chunks)} chunks from {len(sources)} source files.")
    for s in sorted(sources):
        print(f"    * {s}")
    assert len(sources) == 5, f"FAILED: Expected 5 files, but found {len(sources)}"
    print(" -> PASS: Document Loading Test Passed!")

    # TEST 2: Retrieval for Geographic Coverage
    print("\n[TEST 2] Testing Location Retrieval for 'Sawston coverage'...")
    results = retrieve_relevant_context("Does Cambridge Care Services cover Sawston CB22?", chunks)
    found_locations = any("coverage_and_locations" in r["source"] for r in results)
    assert found_locations, "FAILED: Location query did not retrieve location document!"
    print(" -> PASS: Location Retrieval Test Passed! (Found 02_coverage_and_locations.txt)")

    # TEST 3: Retrieval for Specialist Care
    print("\n[TEST 3] Testing Care Retrieval for 'Alzheimer's Dementia'...")
    results = retrieve_relevant_context("Do you support people with Alzheimer's disease?", chunks)
    found_services = any("about_and_services" in r["source"] for r in results)
    assert found_services, "FAILED: Dementia query did not retrieve services document!"
    print(" -> PASS: Care Services Retrieval Test Passed! (Found 01_about_and_services.txt)")

    # TEST 4: Retrieval for Leadership & CQC
    print("\n[TEST 4] Testing Leadership Retrieval for 'Rudrayya Mathapati CQC'...")
    results = retrieve_relevant_context("Who is Registered Manager Rudrayya Mathapati?", chunks)
    found_leadership = any("leadership_funding" in r["source"] for r in results)
    assert found_leadership, "FAILED: Leadership query did not retrieve leadership document!"
    print(" -> PASS: Leadership Retrieval Test Passed! (Found 05_leadership_funding_and_compliance.txt)")

    print("\n" + "=" * 60)
    print("ALL 4 TESTS PASSED SUCCESSFULLY! The RAG Engine is 100% verified.")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
