-- Supabase Architect Agent Schema MVP

-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Memory Embeddings table representing parsed pattern references and past projects
CREATE TABLE IF NOT EXISTS architecture_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id VARCHAR(255) NOT NULL,
    embedding vector(1536),
    architecture JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Token Tracker Table
CREATE TABLE IF NOT EXISTS token_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id VARCHAR(255),
    reasoning_type VARCHAR(50),
    model VARCHAR(255) NOT NULL,
    input_tokens INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    cost_usd NUMERIC(10,5) DEFAULT 0.0,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Basic indexes for fast fetching
CREATE INDEX IF NOT EXISTS arch_proj_idx ON architecture_embeddings(project_id);
CREATE INDEX IF NOT EXISTS token_proj_idx ON token_usage(project_id);
CREATE INDEX IF NOT EXISTS token_time_idx ON token_usage(timestamp);
