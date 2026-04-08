"""
Requirements Parser Engine - Mock/Regex Version
Extracts structured data from natural language requirements using regex and keyword matching.
No LLM dependencies - works offline without API keys.
"""

import re
from typing import List
import logging

from app.models.schemas import RequirementSpec

logger = logging.getLogger("architect_agent.requirement_parser")


class RequirementParser:
    """
    Parses natural language requirements into structured RequirementSpec using regex.
    Fast, deterministic, no external API dependencies.
    """
    
    def __init__(self):
        # Keyword patterns for feature detection
        self.feature_keywords = {
            "authentication": ["auth", "login", "oauth", "sso", "jwt"],
            "api": ["api", "rest", "graphql", "endpoint"],
            "real-time": ["real-time", "realtime", "websocket", "live"],
            "batch": ["batch", "scheduled", "cron"],
            "analytics": ["analytics", "metrics", "reporting"],
            "notifications": ["notification", "alert", "email", "sms"],
            "search": ["search", "elasticsearch", "algolia"],
            "recommendations": ["recommend", "suggestion", "personalization"],
            "AI": ["ai", "ml", "machine learning", "agent", "llm"],
            "RAG": ["rag", "vector", "embedding", "semantic search"],
            "streaming": ["stream", "kafka", "rabbitmq", "event"],
            "ETL": ["etl", "pipeline", "transform", "data warehouse"]
        }
    
    def parse(self, text: str) -> RequirementSpec:
        """
        Parse natural language requirements into structured RequirementSpec.
        
        Args:
            text: Natural language project description
            
        Returns:
            RequirementSpec with extracted fields
        """
        logger.info(f"Parsing requirements (length: {len(text)})")
        
        text_lower = text.lower()
        
        # Extract team size
        team_size = self._extract_team_size(text_lower)
        
        # Extract budget
        budget_usd = self._extract_budget(text_lower)
        
        # Extract expected users
        expected_users = self._extract_users(text_lower)
        
        # Extract latency requirement
        latency_requirement_ms = self._extract_latency(text_lower)
        
        # Extract data sensitivity
        data_sensitivity = self._extract_sensitivity(text_lower)
        
        # Extract deployment target
        deployment_target = self._extract_deployment(text_lower)
        
        # Extract timeline
        timeline_weeks = self._extract_timeline(text_lower)
        
        # Extract features
        key_features = self._extract_features(text_lower)
        
        # Extract constraints
        constraints = self._extract_constraints(text)
        
        spec = RequirementSpec(
            team_size=team_size,
            budget_usd=budget_usd,
            expected_users=expected_users,
            latency_requirement_ms=latency_requirement_ms,
            data_sensitivity=data_sensitivity,
            deployment_target=deployment_target,
            timeline_weeks=timeline_weeks,
            key_features=key_features,
            constraints=constraints
        )
        
        logger.info(f"Parsed: team={team_size}, budget=${budget_usd}, users={expected_users}")
        return spec
    
    def _extract_team_size(self, text: str) -> int:
        """Extract team size from text"""
        patterns = [
            r'(\d+)\s*(?:developers?|engineers?|people|person)',
            r'team\s*(?:of\s*)?(\d+)',
            r'(\d+)\s*person\s*team'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return min(int(match.group(1)), 100)
        
        return 3  # Default
    
    def _extract_budget(self, text: str) -> int:
        """Extract budget in USD"""
        patterns = [
            r'\$\s*(\d+)k',
            r'\$\s*(\d+),?(\d+)',
            r'(\d+)k\s*(?:dollars|usd|budget)',
            r'budget.*?(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                amount = int(match.group(1).replace(',', ''))
                # Check if it's in thousands
                if 'k' in text[max(0, match.start()-5):match.end()+5].lower():
                    amount *= 1000
                return min(amount, 10000000)
        
        return 10000  # Default $10k
    
    def _extract_users(self, text: str) -> int:
        """Extract expected users"""
        patterns = [
            r'(\d+)m\s*(?:users|customers)',
            r'(\d+)k\s*(?:users|customers)',
            r'(\d+),?(\d+)\s*(?:users|customers)',
            r'(?:users|customers).*?(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                num = int(match.group(1).replace(',', ''))
                match_text = text[match.start():match.end()]
                
                if 'm' in match_text:
                    num *= 1000000
                elif 'k' in match_text:
                    num *= 1000
                
                return min(num, 1000000000)
        
        return 10000  # Default 10k users
    
    def _extract_latency(self, text: str) -> int:
        """Extract latency requirement in ms"""
        patterns = [
            r'(\d+)\s*ms',
            r'sub-(\d+)ms',
            r'less than (\d+)\s*ms',
            r'latency.*?(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return int(match.group(1))
        
        # Check for keywords
        if any(word in text for word in ['real-time', 'realtime', 'instant', 'fast']):
            return 100
        elif any(word in text for word in ['slow', 'batch', 'offline']):
            return 5000
        
        return 500  # Default 500ms
    
    def _extract_sensitivity(self, text: str) -> str:
        """Extract data sensitivity level"""
        if any(word in text for word in ['pii', 'personal', 'sensitive', 'hipaa', 'gdpr', 'protected']):
            return "pii"
        elif any(word in text for word in ['public', 'open', 'external']):
            return "public"
        else:
            return "internal"
    
    def _extract_deployment(self, text: str) -> str:
        """Extract deployment target"""
        if any(word in text for word in ['on-prem', 'on prem', 'datacenter', 'self-hosted']):
            return "on_prem"
        elif any(word in text for word in ['hybrid', 'multi-cloud']):
            return "hybrid"
        else:
            return "cloud"
    
    def _extract_timeline(self, text: str) -> int:
        """Extract timeline in weeks"""
        patterns = [
            r'(\d+)\s*weeks?',
            r'(\d+)\s*months?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                weeks = int(match.group(1))
                if 'month' in text[match.start():match.end()]:
                    weeks *= 4
                return min(weeks, 104)  # Max 2 years
        
        return 12  # Default 12 weeks
    
    def _extract_features(self, text: str) -> List[str]:
        """Extract key features from text"""
        features = []
        
        for feature_name, keywords in self.feature_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    features.append(feature_name)
                    break
        
        return list(set(features))[:10]  # Max 10 features
    
    def _extract_constraints(self, text: str) -> List[str]:
        """Extract explicit constraints"""
        constraints = []
        
        # Look for "must" statements
        must_pattern = r'must\s+(?:use|have|support|include)\s+([^.,\n]+)'
        for match in re.finditer(must_pattern, text, re.IGNORECASE):
            constraints.append(match.group(1).strip())
        
        # Look for "required" statements
        required_pattern = r'(?:required|requires|requirement):\s*([^.,\n]+)'
        for match in re.finditer(required_pattern, text, re.IGNORECASE):
            constraints.append(match.group(1).strip())
        
        return constraints[:5]  # Max 5 constraints


# Module-level function for backward compatibility
def parse(text: str) -> RequirementSpec:
    """Parse requirements (non-async version)"""
    parser = RequirementParser()
    return parser.parse(text)
