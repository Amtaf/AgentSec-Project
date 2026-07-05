"""
source_tool.py

Simulates the agent reading an untrusted external source: a webpage,
a document, a token's on-chain metadata, an API response, etc.

For this project we just read local .txt files that stand in for
"content the agent fetched from the internet." This keeps the exploit
demo reproducible and doesn't require you to actually stand up a
malicious website.

This is the injection vector: whatever text lives in these files gets
concatenated into the agent's context as "tool output," and the agent
has to decide whether it's data to summarize or instructions to obey.
"""

from pathlib import Path

SOURCES_DIR = Path(__file__).parent.parent / "malicious_sources"


def read_source(filename: str) -> str:
    path = SOURCES_DIR / filename
    if not path.exists():
        return f"[error: source '{filename}' not found]"
    return path.read_text()
