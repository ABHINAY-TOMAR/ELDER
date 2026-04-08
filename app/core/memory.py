import os
import re
import json
import logging
import hashlib
import asyncio
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Any, Optional, Tuple, Union

import httpx
from supabase import create_client, Client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Constants and Regex for Chunking (Adapted from MemSearch) ---

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_MIN_MEANINGFUL_LEN = 5
_SENTENCE_END_RE = re.compile(r"[。\uFF01\uFF1F.!?]\s*")

# --- Dataclasses ---

@dataclass(frozen=True)
class Chunk:
    """A single semantic chunk extracted from a document or architecture spec."""
    content: str
    source: str  # e.g., project_id or file path
    heading: str = ""
    heading_level: int = 0
    start_line: int = 1
    end_line: int = 1
    content_hash: str = field(default="", repr=False)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.content_hash:
            h = hashlib.sha256(self.content.encode()).hexdigest()[:16]
            object.__setattr__(self, "content_hash", h)

# --- Utility Functions ---

def clean_content_for_embedding(text: str) -> str:
    """Strip noise from text before embedding to improve vector quality."""
    # Remove HTML comments (often contain UUIDs/noise)
    cleaned = _HTML_COMMENT_RE.sub("", text)
    # Collapse multiple blank lines
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()

def _has_meaningful_content(text: str) -> bool:
    """Check if the text has enough substance for indexing."""
    stripped = _HTML_COMMENT_RE.sub("", text)
    # Filter out heading lines to check body substance
    lines = [ln for ln in stripped.splitlines() if not _HEADING_RE.match(ln)]
    body = "\n".join(lines).strip()
    return len(body) >= _MIN_MEANINGFUL_LEN

def chunk_markdown(
    text: str,
    source: str = "",
    max_chunk_size: int = 1000,
    overlap_lines: int = 2
) -> List[Chunk]:
    """Split markdown text into semantic chunks based on headings."""
    lines = text.split("\n")
    
    # Identify heading positions
    heading_positions: List[Tuple[int, int, str]] = []
    for i, line in enumerate(lines):
        m = _HEADING_RE.match(line)
        if m:
            heading_positions.append((i, len(m.group(1)), m.group(2).strip()))

    # Create sections
    sections: List[Tuple[int, int, str, int]] = []
    if not heading_positions or heading_positions[0][0] > 0:
        end = heading_positions[0][0] if heading_positions else len(lines)
        sections.append((0, end, "Preamble", 0))

    for idx, (line_idx, level, title) in enumerate(heading_positions):
        next_start = heading_positions[idx + 1][0] if idx + 1 < len(heading_positions) else len(lines)
        sections.append((line_idx, next_start, title, level))

    chunks: List[Chunk] = []
    for start, end, heading, level in sections:
        section_text = "\n".join(lines[start:end]).strip()
        if not section_text or not _has_meaningful_content(section_text):
            continue

        if len(section_text) <= max_chunk_size:
            chunks.append(
                Chunk(
                    content=section_text,
                    source=source,
                    heading=heading,
                    heading_level=level,
                    start_line=start + 1,
                    end_line=end,
                )
            )
        else:
            # Recursively split large sections
            chunks.extend(
                _split_large_section(
                    lines[start:end],
                    source=source,
                    heading=heading,
                    heading_level=level,
                    base_line=start,
                    max_size=max_chunk_size,
                    overlap=overlap_lines
                )
            )
    return chunks

def _split_large_section(
    lines: List[str],
    source: str,
    heading: str,
    heading_level: int,
    base_line: int,
    max_size: int,
    overlap: int
) -> List[Chunk]:
    """Sub-split large sections at paragraph boundaries."""
    chunks = []
    current_lines = []
    current_start = 0

    def _emit(content: str, s_line: int, e_line: int):
        if content:
            chunks.append(Chunk(content, source, heading, heading_level, s_line, e_line))

    for i, line in enumerate(lines):
        current_lines.append(line)
        text = "\n".join(current_lines)

        is_paragraph_break = line.strip() == "" and i + 1 < len(lines)
        is_last_line = i == len(lines) - 1

        if len(text) >= max_size and is_paragraph_break:
            _emit(text.strip(), base_line + current_start + 1, base_line + i + 1)
            overlap_start = max(0, len(current_lines) - overlap)
            current_lines = current_lines[overlap_start:]
            current_start = i + 1 - len(current_lines)
            continue

        if is_last_line:
            _emit(text.strip(), base_line + current_start + 1, base_line + i + 1)
            
    return chunks

# --- Main Memory Class ---

class ArchitectMemory:
    """
    Centralized memory system for the Architect Agent.
    
    Provides long-term storage and semantic retrieval of architectures,
    ADRs, requirements, and execution logs using Supabase pgvector.
    """

    def __init__(self, collection_name: str = "architect_memory"):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.collection_name = collection_name
        self.embedding_model = "text-embedding-3-small"
        self.dimension = 1536

        if self.supabase_url and self.supabase_key:
            try:
                self.client: Client = create_client(self.supabase_url, self.supabase_key)
            except Exception as e:
                logger.error(f"Supabase init error: {e}")
                self.client = None
        else:
            self.client = None
            logger.warning("Supabase credentials missing. Memory will operate in mock mode.")

    async def embed(self, texts: Union[str, List[str]]) -> List[List[float]]:
        """Generate OpenAI embeddings for one or more strings."""
        if not self.openai_key:
            # Fallback for local dev/testing
            return [[0.0] * self.dimension] * (1 if isinstance(texts, str) else len(texts))

        if isinstance(texts, str):
            texts = [texts]

        # Clean texts for better embedding quality
        cleaned_texts = [clean_content_for_embedding(t) for t in texts]

        url = "https://api.openai.com/v1/embeddings"
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url, 
                    headers=headers, 
                    json={"input": cleaned_texts, "model": self.embedding_model},
                    timeout=20.0
                )
                response.raise_for_status()
                data = response.json()
                return [item["embedding"] for item in data["data"]]
            except Exception as e:
                logger.error(f"Embedding error: {e}")
                return [[0.0] * self.dimension] * len(texts)

    async def store_chunk(self, chunk: Chunk, category: str, tags: List[str] = None) -> bool:
        """Store a single chunk with its embedding in Supabase."""
        if not self.client:
            return False

        embedding = (await self.embed(chunk.content))[0]
        
        data = {
            "chunk_hash": chunk.content_hash,
            "content": chunk.content,
            "embedding": embedding,
            "source": chunk.source,
            "heading": chunk.heading,
            "category": category,
            "tags": tags or [],
            "metadata": {
                **chunk.metadata,
                "start_line": chunk.start_line,
                "end_line": chunk.end_line,
                "heading_level": chunk.heading_level
            },
            "created_at": datetime.now().isoformat()
        }

        try:
            self.client.table(self.collection_name).upsert(data, on_conflict="chunk_hash").execute()
            return True
        except Exception as e:
            logger.error(f"Failed to store chunk {chunk.content_hash}: {e}")
            return False

    async def store_text(self, text: str, source: str, category: str, tags: List[str] = None):
        """Split text into chunks and store them all."""
        chunks = chunk_markdown(text, source=source)
        logger.info(f"Storing {len(chunks)} chunks from {source} into category {category}")
        
        tasks = [self.store_chunk(c, category, tags) for c in chunks]
        results = await asyncio.gather(*tasks)
        return all(results)

    async def store_architecture(self, project_id: str, architecture_spec: Dict[str, Any]):
        """
        Specialized method to store a full architecture design.
        Breaks down the JSON spec into semantic text chunks.
        """
        # Convert JSON parts to markdown-like text for better embedding
        content_parts = [
            f"# Architecture: {architecture_spec.get('name', project_id)}",
            f"## Description\n{architecture_spec.get('description', 'N/A')}",
            f"## Domain\n{architecture_spec.get('domain', 'N/A')}"
        ]
        
        # Add Services
        services = architecture_spec.get("services", [])
        if services:
            content_parts.append("## Services")
            for svc in services:
                content_parts.append(f"### Service: {svc.get('name')}\n{svc.get('description')}\nStack: {svc.get('stack')}")

        # Add ADRs
        adrs = architecture_spec.get("adrs", [])
        if adrs:
            content_parts.append("## Decisions (ADRs)")
            for adr in adrs:
                content_parts.append(f"### {adr.get('title')}\n{adr.get('context')}\nDecision: {adr.get('decision')}")

        full_text = "\n\n".join(content_parts)
        tags = [architecture_spec.get("domain", "unknown"), "architecture_spec"]
        return await self.store_text(full_text, source=project_id, category="architecture", tags=tags)

    async def search(
        self, 
        query: str, 
        category: Optional[str] = None, 
        tags: Optional[List[str]] = None, 
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant memories using vector similarity.
        
        Args:
            query: Natural language query.
            category: Filter by category (e.g., 'architecture').
            tags: Filter by tags (OR matching).
            limit: Max results.
            
        Returns:
            List of matching memory records.
        """
        if not self.client:
            return []

        query_embedding = (await self.embed(query))[0]
        
        # We use an RPC call 'match_architect_memory' which must be defined in Supabase
        # See docs/memory_layer.md for SQL definition
        rpc_params = {
            "query_embedding": query_embedding,
            "match_threshold": 0.3,
            "match_count": limit,
            "filter_category": category,
            "filter_tags": tags
        }

        try:
            result = self.client.rpc("match_architect_memory", rpc_params).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Search error: {e}")
            # Fallback to simple category filter if RPC fails
            query_obj = self.client.table(self.collection_name).select("*")
            if category:
                query_obj = query_obj.eq("category", category)
            
            # Simple select (not semantic)
            result = query_obj.limit(limit).execute()
            return result.data or []

    async def compact(self, project_id: str, llm_summarizer_func) -> str:
        """
        Compact project memories into a summary to prevent context bloat.
        
        Args:
            project_id: The project to compact.
            llm_summarizer_func: Async function that takes a list of chunks and returns a summary.
            
        Returns:
            str: The generated summary.
        """
        # 1. Fetch all chunks for the project
        try:
            result = self.client.table(self.collection_name).select("content").eq("source", project_id).execute()
            chunks = [r["content"] for r in result.data or []]
            
            if not chunks:
                return "No memories found to compact."
                
            # 2. Call the provided LLM summarizer
            summary = await llm_summarizer_func(chunks)
            
            # 3. Store the summary as a new 'compact' memory
            summary_text = f"# Compacted Memory: {project_id}\n\n{summary}\n\n*Generated on {date.today()}*"
            await self.store_text(summary_text, source=project_id, category="compact_summary", tags=["compaction"])
            
            return summary
        except Exception as e:
            logger.error(f"Compaction failed: {e}")
            return f"Error during compaction: {str(e)}"

    async def get_stats(self) -> Dict[str, Any]:
        """Get high-level statistics about the memory layer."""
        if not self.client:
            return {"status": "offline"}
            
        try:
            # Get total count and category breakdown
            # Note: For large tables, this should be an RPC or estimate
            res = self.client.table(self.collection_name).select("category", count="exact").execute()
            total = res.count
            
            # Manual breakdown from sample or separate queries
            categories = {}
            for row in res.data:
                cat = row["category"]
                categories[cat] = categories.get(cat, 0) + 1
                
            return {
                "total_chunks": total,
                "categories": categories,
                "dimension": self.dimension,
                "model": self.embedding_model
            }
        except Exception as e:
            return {"error": str(e)}

    async def delete_project_memory(self, project_id: str) -> bool:
        """Wipe all memories associated with a project."""
        if not self.client:
            return False
        try:
            self.client.table(self.collection_name).delete().eq("source", project_id).execute()
            return True
        except Exception as e:
            logger.error(f"Delete failed: {e}")
            return False

# --- Documentation (Markdown) ---

"""
## Supabase Setup for ArchitectMemory

The following SQL should be run in your Supabase SQL Editor to enable vector search:

```sql
-- Enable the pgvector extension to work with embeddings
create extension if not exists vector;

-- Create the memory table
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
create index on architect_memory using ivfflat (embedding vector_cosine_ops)
  with (lists = 100);

-- Create the RPC function for semantic search
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
```
"""
