import re
import pathlib

def test_readme_contains_required_sections():
    readme_path = pathlib.Path("README.md")
    assert readme_path.is_file(), "README.md does not exist"
    content = readme_path.read_text(encoding="utf-8")

    required_headings = [
        r"#\s+Project Title",               # Title
        r"!\[.*\]\(.*\)",                   # Badges (at least one image)
        r"##\s+Table of Contents",          # TOC
        r"##\s+Installation",               # Installation
        r"##\s+Usage",                      # Usage
        r"##\s+API Reference",              # API Reference
        r"##\s+Data Model",                 # Data Model
        r"##\s+Persistence",                # Persistence
        r"##\s+Testing",                    # Testing
        r"##\s+CI\s*/\s*Contributing",       # CI/Contributing
        r"##\s+License",                    # License
    ]

    for pattern in required_headings:
        assert re.search(pattern, content, re.IGNORECASE), f"Missing required section matching: {pattern}"