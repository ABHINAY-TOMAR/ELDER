# 🏛️ Architect Agent — Memory Layer

The Memory Layer is the semantic storage backbone of the Architect Agent. It uses **Supabase (PostgreSQL)** with the `pgvector` extension to store and retrieve architectural patterns, decisions, and execution history.

## Key Features

1.  **Semantic Search:** Retrieve past architectures based on natural language similarity.
2.  **Smart Chunking:** Markdown-aware splitting that respects headings and paragraph boundaries.
3.  **Content Cleaning:** Strips HTML comments and noise before embedding to improve vector quality.
4.  **Compaction:** Summarizes project-specific memories to prevent context window bloat during long-running design sessions.
5.  **Categorization:** Tags and categories (e.g., `architecture`, `adr`, `requirements`) for precise filtering.

## Implementation Details

-   **Model:** `text-embedding-3-small` (1536 dimensions).
-   **Vector Index:** `ivfflat` for efficient similarity search.
-   **Similarity Metric:** Cosine Similarity (`<=>` operator in pgvector).

## Core API

-   `store_text(text, source, category, tags)`: Chunks and stores any text content.
-   `store_architecture(project_id, architecture_spec)`: specialized storage for JSON architecture designs.
-   `search(query, category, tags, limit)`: Semantic retrieval via Supabase RPC.
-   `compact(project_id, summarizer_func)`: Project memory aggregation.

## SQL Schema

Refer to `supabase/migrations/20260407_init_schema.sql` for the complete table and RPC definitions.
