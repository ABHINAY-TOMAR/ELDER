import unittest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from app.core.token_tracker import ArchitectTokenTracker
from app.core.memory import ArchitectMemory, Chunk, chunk_markdown, clean_content_for_embedding

class TestWeek1(unittest.IsolatedAsyncioTestCase):
    """
    Test suite for Week 1 deliverables: Memory Layer and Token Tracking.
    Using IsolatedAsyncioTestCase for cleaner async testing.
    """

    # --- Token Tracker Tests ---

    def test_token_estimation(self):
        tracker = ArchitectTokenTracker()
        self.assertEqual(tracker.estimate_tokens(""), 0)
        self.assertEqual(tracker.estimate_tokens("abcd"), 1)  # 4 chars = 1 token
        self.assertEqual(tracker.estimate_tokens("abcde"), 2) # 5 chars = 2 tokens
        self.assertEqual(tracker.estimate_tokens("hello world"), 3) # 11 chars = 3 tokens

    def test_cost_calculation(self):
        tracker = ArchitectTokenTracker()
        # Claude 3.5 Sonnet: $3.0 input, $15.0 output per 1M
        cost = tracker.calculate_cost("claude-3-5-sonnet", 1_000_000, 1_000_000)
        self.assertEqual(cost, 18.0)
        
        # GPT-4o Mini: $0.15 input, $0.60 output per 1M
        cost = tracker.calculate_cost("gpt-4o-mini", 1_000_000, 1_000_000)
        self.assertEqual(cost, 0.75)

    @patch("app.core.token_tracker.create_client")
    async def test_track_usage_mock(self, mock_create_client):
        # Mock Supabase client
        mock_supabase = MagicMock()
        mock_create_client.return_value = mock_supabase
        
        tracker = ArchitectTokenTracker()
        tracker.client = mock_supabase
        
        cost = await tracker.track_usage("proj_123", "gpt-4o", 1000, 500, "fast")
        
        self.assertGreater(cost, 0)
        mock_supabase.table.assert_called_with("token_usage")
        mock_supabase.table().insert.assert_called()

    # --- Memory Layer Tests ---

    def test_content_cleaning(self):
        raw = "Hello world <!-- secret uuid -->\n\n\nNew line"
        cleaned = clean_content_for_embedding(raw)
        self.assertNotIn("secret uuid", cleaned)
        self.assertNotIn("<!--", cleaned)
        # Expected 'Hello world\n\nNew line'
        self.assertEqual(cleaned, "Hello world\n\nNew line")

    def test_markdown_chunking(self):
        md = """# Title
This is some content.

## Section 1
More content here.
It spans multiple lines.

## Section 2
Final section.
"""
        chunks = chunk_markdown(md, source="test.md")
        self.assertEqual(len(chunks), 3)
        self.assertEqual(chunks[0].heading, "Title")
        self.assertEqual(chunks[1].heading, "Section 1")
        self.assertEqual(chunks[2].heading, "Section 2")
        self.assertEqual(chunks[1].source, "test.md")

    def test_large_chunk_splitting(self):
        # Create a text large enough to trigger splitting with paragraph breaks.
        long_text = "# Header\n\n" + "\n\n".join(["LongContent " * 10 for _ in range(5)])
        chunks = chunk_markdown(long_text, max_chunk_size=50)
        self.assertGreater(len(chunks), 1)
        self.assertEqual(chunks[0].heading, "Header")

    @patch("app.core.memory.httpx.AsyncClient.post")
    @patch("app.core.memory.create_client")
    async def test_memory_store_and_search_mock(self, mock_create_client, mock_post):
        # Mock OpenAI Embedding Response
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {
            "data": [{"embedding": [0.1] * 1536}]
        }
        # httpx post is async, but we can mock it as an async return value if needed
        # Or just use AsyncMock for the post method
        mock_post.return_value = mock_resp
        
        # Mock Supabase
        mock_supabase = MagicMock()
        mock_create_client.return_value = mock_supabase
        
        memory = ArchitectMemory()
        memory.openai_key = "fake_key"
        memory.client = mock_supabase
        
        # Test Embed
        embeddings = await memory.embed("test query")
        self.assertEqual(len(embeddings), 1)
        self.assertEqual(len(embeddings[0]), 1536)
        
        # Test Search (RPC call)
        mock_supabase.rpc().execute.return_value = MagicMock(data=[{"content": "found it"}])
        results = await memory.search("where is it?")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["content"], "found it")

    @patch("app.core.memory.create_client")
    async def test_memory_compaction_mock(self, mock_create_client):
        mock_supabase = MagicMock()
        mock_create_client.return_value = mock_supabase
        memory = ArchitectMemory()
        memory.client = mock_supabase
        
        # Mock data for compaction
        mock_supabase.table().select().eq().execute.return_value = MagicMock(
            data=[{"content": "chunk 1"}, {"content": "chunk 2"}]
        )
        
        # Mock summarizer
        async def mock_summarizer(chunks):
            return "Summary of " + " and ".join(chunks)
            
        summary = await memory.compact("proj_1", mock_summarizer)
        
        self.assertEqual(summary, "Summary of chunk 1 and chunk 2")
        # Should have called store_text which calls store_chunk
        mock_supabase.table().upsert.assert_called()

if __name__ == "__main__":
    unittest.main()
