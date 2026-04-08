-- Finalized Schema for Architect Agent MVP
-- Date: 2026-04-08

-- Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 1. Architecture Embeddings Table (Main Memory)
CREATE TABLE IF NOT EXISTS architecture_embeddings (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id varchar(255) NOT NULL,
    architecture jsonb NOT NULL,
    embedding vector(1536), -- Dimension for text-embedding-3-small
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);

-- Index for vector similarity search
CREATE INDEX IF NOT EXISTS idx_architecture_embeddings_vector 
ON architecture_embeddings USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- 2. Token Usage Table (Cost Tracking)
CREATE TABLE IF NOT EXISTS token_usage (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id varchar(255),
    model varchar(255) NOT NULL,
    input_tokens integer DEFAULT 0,
    output_tokens integer DEFAULT 0,
    cost_usd numeric DEFAULT 0.0,
    reasoning_type varchar(50) DEFAULT 'fast',
    timestamp timestamptz DEFAULT now()
);

-- Index for project-based lookups
CREATE INDEX IF NOT EXISTS idx_token_usage_project_id ON token_usage(project_id);

-- 3. Vector Search RPC Function
CREATE OR REPLACE FUNCTION match_architectures (
  query_embedding vector(1536),
  match_count int DEFAULT 5
)
RETURNS TABLE (
  id uuid,
  project_id varchar,
  architecture jsonb,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    architecture_embeddings.id,
    architecture_embeddings.project_id,
    architecture_embeddings.architecture,
    1 - (architecture_embeddings.embedding <=> query_embedding) AS similarity
  FROM architecture_embeddings
  ORDER BY architecture_embeddings.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
