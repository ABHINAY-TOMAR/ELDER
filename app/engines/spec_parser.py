import logging
import json
import re
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpecParser:
    """
    Extracts structured API and Database specifications from code or config files.
    Used by the CoherenceChecker to validate implementations.
    """

    def parse_openapi(self, content: str) -> Dict[str, Any]:
        """
        Attempt to parse an OpenAPI YAML/JSON string.
        """
        try:
            # Simple JSON check
            return json.loads(content)
        except:
            # In a real implementation, we'd use a YAML parser or 
            # regex to extract FastAPI routes if it's raw code
            logger.warning("Fast OpenAPI parser fallback: extracting routes via regex.")
            routes = re.findall(r'@app\.(get|post|put|delete)\("([^"]+)"\)', content)
            return {"routes": routes}

    def parse_sql_schema(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract table and column information from SQL DDL.
        """
        tables = []
        # Basic regex to find CREATE TABLE statements
        matches = re.findall(r'CREATE TABLE (\w+) \((.*?)\);', content, re.DOTALL | re.IGNORECASE)
        for table_name, columns_raw in matches:
            tables.append({
                "name": table_name,
                "columns": [c.strip() for f in columns_raw.split(',') for c in [f.strip()] if c]
            })
        return tables
