-- Enable the pgvector extension to work with embeddings
create extension if not exists vector;

-- 1. Create the Architect Memory Table
create table if not exists architect_memory (
  id bigserial primary key,
  chunk_hash text unique not null,
  content text not null,
  embedding vector(1536), -- 1536 is the dimension for text-embedding-3-small
  source text not null,
  heading text,
  category text not null,
  tags text[] default '{}',
  metadata jsonb default '{}',
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Create an index for faster similarity search
-- Adjust lists based on expected table size (100 is good for small/medium)
create index on architect_memory using ivfflat (embedding vector_cosine_ops)
  with (lists = 100);

-- 2. Create the Token Usage Table
create table if not exists token_usage (
  id uuid primary key default gen_random_uuid(),
  project_id text not null,
  model text not null,
  input_tokens integer not null,
  output_tokens integer not null,
  total_tokens integer not null,
  cost_usd double precision not null,
  reasoning_type text not null, -- 'fast', 'deep', 'structured'
  metadata jsonb default '{}',
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Index for project-based cost reporting
create index idx_token_usage_project_id on token_usage(project_id);
create index idx_token_usage_created_at on token_usage(created_at);

-- 3. RPC Function for Semantic Search
create or replace function match_architect_memory (
  query_embedding vector(1536),
  match_threshold float,
  match_count int,
  filter_category text default null,
  filter_tags text[] default null
)
returns table (
  id bigint,
  content text,
  source text,
  category text,
  tags text[],
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    architect_memory.id,
    architect_memory.content,
    architect_memory.source,
    architect_memory.category,
    architect_memory.tags,
    1 - (architect_memory.embedding <=> query_embedding) as similarity
  from architect_memory
  where 1 - (architect_memory.embedding <=> query_embedding) > match_threshold
    and (filter_category is null or architect_memory.category = filter_category)
    and (filter_tags is null or architect_memory.tags && filter_tags)
  order by architect_memory.embedding <=> query_embedding
  limit match_count;
end;
$$;

-- 4. RPC Function for Daily Stats
create or replace function get_daily_token_stats(days_limit int)
returns table (
  date date,
  total_cost float8,
  total_tokens bigint
) 
language plpgsql
as $$
begin
  return query
  select 
    created_at::date as date,
    sum(cost_usd)::float8 as total_cost,
    sum(total_tokens)::bigint as total_tokens
  from token_usage
  where created_at > now() - (days_limit || ' days')::interval
  group by 1
  order by 1 desc;
end;
$$;

-- 5. Create Task Assignments Table
create table if not exists task_assignments (
  id bigserial primary key,
  task_id text unique not null,
  project_id text not null,
  phase_number integer not null,
  status text not null, -- 'dispatched', 'in_progress', 'completed', 'failed'
  agent_url text not null,
  output_repo_url text,
  error_message text,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  completed_at timestamp with time zone
);

create index idx_task_assignments_project_id on task_assignments(project_id);
create index idx_task_assignments_task_id on task_assignments(task_id);
