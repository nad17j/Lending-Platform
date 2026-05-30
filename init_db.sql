-- 1. Lifecycle Control Management Matrix
-- Terminate existing connections to allow dropping/rebuilding without locking conflicts
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'lending_db' AND pid <> pg_backend_pid();

DROP DATABASE IF EXISTS lending_db;
CREATE DATABASE lending_db;

-- Explicitly switch our execution session context into the newly initialized lending database container
\c lending_db;

-- Configuration boundaries matching core schema parameters
-- Note: JavaScript properties like BACKEND_URL = 'http://127.0.0.1:8000/v1/underwriting/override-submit' should be handled inside application code layers.

-- 1. Activating the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Creating a table to store core application details and full-document metadata embeddings
CREATE TABLE IF NOT EXISTS document_embeddings (
    application_id VARCHAR(50) PRIMARY KEY, -- Fixed: Removed 'SERIAL' conflict with VARCHAR
    ocr_confidence NUMERIC(4, 2),
    applicant_name VARCHAR(255) DEFAULT 'Anonymous Applicant',
    salary_lkr NUMERIC(12, 2),
    calculated_dti NUMERIC(5, 4),           -- Fixed: Changed hyphen to underscore
    crib_score INTEGER,
    loan_amount NUMERIC(12, 2),
    final_decision VARCHAR(30),             -- Bumped to 30 characters for "ESCALATED TO HUMAN REVIEW"
    compliance_rationale TEXT,
    embedding VECTOR(1536),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Corrected & unified Trigger Function Block
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;    
$$ LANGUAGE plpgsql;    

-- 4. Binding the trigger to document_embeddings
CREATE TRIGGER update_document_embeddings_updated_at
BEFORE UPDATE ON document_embeddings
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 5. Creating an IVFFlat index for fast similarity search
-- Note: ivfflat recommends having data in the table before defining lists, HNSW is an alternative.
CREATE INDEX IF NOT EXISTS idx_document_embeddings_embedding 
ON document_embeddings USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);

-- 6. Creating the agent security table (Audit logs)
CREATE TABLE IF NOT EXISTS agent_security (
    log_id SERIAL PRIMARY KEY,
    api_key VARCHAR(255) NOT NULL, -- Fixed: Removed UNIQUE constraint so keys can log multiple events
    application_id VARCHAR(50) NOT NULL REFERENCES document_embeddings(application_id) ON DELETE CASCADE, -- Linked relational foreign key
    active_agent_id VARCHAR(50) NOT NULL,
    log_level VARCHAR(20),
    telemetry_data TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW() -- Removed unnecessary updated_at for immutable logs
);

-- 7. Creating the granular chunk storage table for deep RAG searches
CREATE TABLE IF NOT EXISTS document_vector_storage (
    doc_id SERIAL PRIMARY KEY,
    application_id VARCHAR(50) REFERENCES document_embeddings(application_id) ON DELETE CASCADE, -- Linked relational foreign key
    document_chunk TEXT, -- Cleaned casing naming convention
    vector_embedding VECTOR(1536),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. Binding the timestamp trigger to chunk storage as well
CREATE TRIGGER update_document_vector_storage_updated_at
BEFORE UPDATE ON document_vector_storage
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();