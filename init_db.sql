-- ====================================================================
-- MASTER PRODUCTION ENTERPRISE PERSISTENCE ARCHITECTURE
-- ====================================================================

-- Enable the high-performance pgvector module extension natively
CREATE EXTENSION IF NOT EXISTS vector;

-- 1. CENTRAL BANK OF SRI LANKA REGULATORY COMPLIANCE MATRIX (For RAG Engine)
CREATE TABLE IF NOT EXISTS central_bank_regulations (
    id SERIAL PRIMARY KEY,
    section_reference VARCHAR(50) NOT NULL,
    chunk_content TEXT NOT NULL,
    embedding vector(3) -- Match your exact LLM embedding dimensions (e.g., 768 or 1536)
);

-- 2. PRODUCTION TRANSACTIONAL LEDGER (The new core schema)
CREATE TABLE IF NOT EXISTS loan_applications (
    id SERIAL PRIMARY KEY,
    tx_id VARCHAR(50) UNIQUE NOT NULL,
    user_identity VARCHAR(100) NOT NULL,
    crib_score INT NOT NULL,
    dti NUMERIC(5,2) NOT NULL,
    execution_status VARCHAR(50) NOT NULL,
    rationale TEXT NOT NULL,
    policy_evidence TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. AUDITING & COMPLIANCE LOGS (Keeps your security tracking intact)
CREATE TABLE IF NOT EXISTS agent_security (
    id SERIAL PRIMARY KEY,
    api_key VARCHAR(255),
    application_id VARCHAR(100) NOT NULL,
    active_agent_id VARCHAR(100) NOT NULL,
    log_level VARCHAR(20) NOT NULL,
    telemetry_data JSONB, -- Stores full dynamic metadata payloads securely
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. PERFORMANCE TUNING & INDEXES
-- Builds an IVFFlat spatial index to optimize search lookups across vector clusters
CREATE INDEX IF NOT EXISTS cbsl_vector_cosine_idx 
ON central_bank_regulations USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- B-Tree Index for rapid transaction log tracing lookups
CREATE INDEX IF NOT EXISTS idx_loan_apps_tx_id ON loan_applications(tx_id);