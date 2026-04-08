-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Memory table for storing architectural patterns and memories
CREATE TABLE memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(1536),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for vector similarity search
CREATE INDEX idx_memory_embedding ON memory USING ivfflat (embedding vector_cosine_ops);

-- Create index for category filtering
CREATE INDEX idx_memory_category ON memory(category);

-- Create index for full-text search
CREATE INDEX idx_memory_content_fts ON memory USING gin(to_tsvector('english', content));

-- Token usage tracking table
CREATE TABLE token_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id VARCHAR(100),
    model VARCHAR(100) NOT NULL,
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL,
    total_tokens INTEGER NOT NULL,
    cost_usd DECIMAL(10, 6) NOT NULL,
    task_type VARCHAR(50) DEFAULT 'general',
    session_id UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for session-based queries
CREATE INDEX idx_token_usage_session ON token_usage(session_id);

-- Create index for project-based aggregation
CREATE INDEX idx_token_usage_project ON token_usage(project_id);

-- Create index for time-based queries
CREATE INDEX idx_token_usage_created ON token_usage(created_at DESC);

-- Trigger to update updated_at on memory table
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_memory_updated_at
    BEFORE UPDATE ON memory
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
