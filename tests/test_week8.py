import unittest
import asyncio
from app.models.architecture import Architecture, Service
from app.engines.coherence_checker import CoherenceChecker
from app.engines.spec_parser import SpecParser

class TestWeek8(unittest.IsolatedAsyncioTestCase):
    """
    Test suite for Week 8 deliverables: Coherence Checking.
    """

    def test_spec_parser_openapi(self):
        parser = SpecParser()
        code = """
        @app.get("/users")
        async def get_users(): pass
        
        @app.post("/login")
        async def login(): pass
        """
        spec = parser.parse_openapi(code)
        self.assertEqual(len(spec["routes"]), 2)
        self.assertEqual(spec["routes"][0][1], "/users")

    def test_spec_parser_sql(self):
        parser = SpecParser()
        sql = "CREATE TABLE users (id INT, name TEXT);"
        tables = parser.parse_sql_schema(sql)
        self.assertEqual(len(tables), 1)
        self.assertEqual(tables[0]["name"], "users")
        self.assertIn("id INT", tables[0]["columns"])

    async def test_coherence_checker_smoke(self):
        checker = CoherenceChecker()
        arch = Architecture(
            project_id="p1", project_name="T", domain="ms", tech_stack={}, 
            services=[Service(id="s1", name="S1", description="D", stack="S")],
            rationale="R"
        )
        # Empty specs -> no issues
        result = await checker.check(arch, {})
        self.assertTrue(result.passed)
        self.assertEqual(result.score, 1.0)

if __name__ == "__main__":
    unittest.main()
