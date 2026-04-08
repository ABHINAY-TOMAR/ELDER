"""
Setup script to initialize the Architect Agent project structure
"""
import os
from pathlib import Path

# Define project structure
DIRECTORIES = [
    "app",
    "app/api",
    "app/core",
    "app/engines",
    "scripts",
    "tests",
    "config",
    ".github/workflows"
]

def create_directories():
    """Create all project directories"""
    base_path = Path(__file__).parent
    
    for directory in DIRECTORIES:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {directory}")
        
        # Create __init__.py for Python packages
        if directory.startswith("app"):
            init_file = dir_path / "__init__.py"
            if not init_file.exists():
                init_file.write_text("# Architect Agent Package\n")

if __name__ == "__main__":
    print("Initializing Architect Agent project structure...")
    create_directories()
    print("\n✅ Project structure initialized successfully!")
