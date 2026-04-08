import unittest
from app.models.architecture import Architecture, Service, Phase
from app.engines.implementation_planner import ImplementationPlanner
from app.engines.phase_spec_generator import PhaseSpecGenerator

class TestWeek6(unittest.TestCase):
    """
    Test suite for Week 6 deliverables: Implementation Planning.
    """

    def setUp(self):
        # Create a mock architecture with dependencies
        self.services = [
            Service(id="auth", name="Auth", description="A", stack="S"),
            Service(id="product", name="Product", description="P", stack="S"),
            Service(id="order", name="Order", description="O", stack="S", dependencies=["auth", "product"]),
            Service(id="gateway", name="Gateway", description="G", stack="S", dependencies=["order"])
        ]
        self.arch = Architecture(
            project_id="p1", project_name="Test", domain="microservices",
            tech_stack={"s": "s"}, services=self.services, rationale="R"
        )

    def test_implementation_planner(self):
        planner = ImplementationPlanner()
        phases = planner.plan(self.arch)
        
        # Expected Phasing:
        # Phase 1: auth, product (0 in-degree)
        # Phase 2: order (depends on auth, product)
        # Phase 3: gateway (depends on order)
        
        self.assertEqual(len(phases), 3)
        self.assertIn("auth", phases[0].service_ids)
        self.assertIn("product", phases[0].service_ids)
        self.assertIn("order", phases[1].service_ids)
        self.assertIn("gateway", phases[2].service_ids)
        self.assertEqual(phases[1].dependencies[0], 1) # Depends on phase 1

    def test_phase_spec_generator(self):
        planner = ImplementationPlanner()
        phases = planner.plan(self.arch)
        
        generator = PhaseSpecGenerator()
        phases_with_specs = generator.generate_specs(self.arch, phases)
        
        self.assertIsNotNone(phases_with_specs[0].spec_markdown)
        self.assertIn("# Phase 1", phases_with_specs[0].spec_markdown)
        self.assertIn("Service: Auth", phases_with_specs[0].spec_markdown)
        self.assertIn("Success Criteria", phases_with_specs[0].spec_markdown)

if __name__ == "__main__":
    unittest.main()
