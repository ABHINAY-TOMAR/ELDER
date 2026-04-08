# 🪙 Architect Agent — Token Tracking & Cost Management

The Token Tracker provides comprehensive visibility into LLM usage and project budgets. It ensures that architectural reasoning is cost-effective and remains within specified limits.

## Key Features

1.  **Model-Specific Pricing:** Real-time cost calculation based on input/output tokens for OpenAI, Anthropic, DeepSeek, and Google models.
2.  **Token Estimation:** Fast heuristic (`char_len / 4`) for pre-call budget checks.
3.  **Project-Scoped Tracking:** Aggregate costs per architecture design session.
4.  **Temporal Statistics:** Daily, weekly, and monthly cost aggregation via Supabase RPC.
5.  **Budget Alerts:** Logic to identify when a project is approaching or exceeding its budget limit.
6.  **Retention Policy:** Automated cleanup of logs older than 90 days.

## Implementation Details

-   **Database:** `token_usage` table in Supabase.
-   **Aggregations:** Optimized via database RPC functions.
-   **Fallback:** Manual in-memory aggregation if RPC is unavailable.

## Supported Models (April 2026)

-   `claude-3-5-sonnet`
-   `claude-3-5-haiku`
-   `gpt-4o`
-   `gpt-4o-mini`
-   `deepseek-chat`
-   `gemini-1.5-pro`
-   `o1-preview`
-   `o1-mini`

## Core API

-   `track_usage(project_id, model, input_tokens, output_tokens, reasoning_type)`: Records a single LLM call.
-   `get_project_summary(project_id)`: Summarizes total cost and token breakdown.
-   `get_daily_stats(days)`: Provides usage trends over time.
-   `get_budget_alert(project_id, limit_usd)`: Checks status against project budget.

## SQL Schema

Refer to `supabase/migrations/20260407_init_schema.sql` for table and aggregation functions.
