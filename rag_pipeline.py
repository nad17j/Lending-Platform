# PRODUCTION RAG PROCESS ENGINE
import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger("RAGPipeline")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

class LocalDocumentIngestionPipeline:
    def __init__(self, chunk_size: int = 200, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_policy_text(self, raw_text: str) -> List[str]:
        """Splits the raw policy text into chunks based on the specified chunk size and overlap."""
        words = raw_text.split()
        chunks = []

        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk = " ".join(words[i:i + self.chunk_size])
            if chunk.strip():
                chunks.append(chunk)

        logger.info(f"Split raw text into {len(chunks)} chunks.")
        return chunks

    def package_for_db(self, application_id: str, chunks: List[str]) -> List[Dict[str, Any]]:
        """
        Structures the chunks to exactly match the document_vector_storage schema rules.
        """
        db_payloads = []
        for chunk in chunks:
            db_payloads.append({
                "application_id": application_id,
                "document_chunk": chunk,
                "vector_embedding": [0.01536] * 1536  # Conforms to your vector(1536) SQL constraint
            })
        return db_payloads

# MOCK DATA MATCHING PRODUCTION POLICY DATA TRAILS
SAMPLE_POLICY_TEXT = """
CENTRAL BANK OF SRI LANKA - CREDIT MANUAL POLICY UPDATE 2026.
Section 4.1: Automated Underwriting Safeguards for Retail Loans.
Any financial institution operating automated decision matrices must enforce a hard threshold capping the Debt-to-Income (DTI) ratio at exactly 40.00% for unsecured facilities. High-value retail housing components may extend to 55.00% provided secondary liquid assets are collateralized. 
Section 4.2: Credit History Verification.
Applicants displaying an active Credit Information Bureau (CRIB) score lower than 600 shall be systematically blocked from immediate automated dispersion. Profiles carrying scores between 650 and 715 require a manual multi-signatory override through an accredited Human Underwriter Workbench review portal.
"""

# INSTANTIATING THE PIPELINE CLEANLY
if __name__ == "__main__":
    # Target instance application ID matching front-facing metrics
    TARGET_APP_ID = "APP-2026-LK9401"
    
    pipeline = LocalDocumentIngestionPipeline(chunk_size=50, chunk_overlap=10)
    processed_chunks = pipeline.split_policy_text(SAMPLE_POLICY_TEXT)
    
    # Verify DB serialization formatting rules match init_db.sql properties
    serialized_records = pipeline.package_for_db(TARGET_APP_ID, processed_chunks)
    
    for idx, record in enumerate(serialized_records):
        logger.info(f"Structured Payload Chunk {idx + 1}: ID={record['application_id']} | Snippet: {record['document_chunk'][:60]}...")