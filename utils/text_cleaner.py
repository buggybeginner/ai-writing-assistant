"""
PersonaWrite AI — Text Cleaner Utility

Strips ANSI escape sequences, terminal control codes, and garbage tokens
from text. Used to sanitize both generator input and output.
"""

import re


def sanitize_text(text: str) -> str:
    """
    Remove all ANSI escape sequences, terminal control codes, and garbage
    tokens from text. Returns clean, readable English.

    Handles:
      - Full ANSI escape sequences: \\x1b[...m, \\x1b[K, \\x1b[1D, etc.
      - Partial/broken sequences: [K, [1D, [2D, m[1D[K, etc.
      - Non-printable / control characters (\\x00–\\x1f except \\n and \\t)
      - Stray dimensional tokens: 1D, 2D, 3D
      - Extra whitespace
    """
    if not text:
        return ""

    # 1. Remove full ANSI escape sequences: ESC[...X
    cleaned = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text)

    # 2. Remove any remaining raw ESC characters
    cleaned = re.sub(r'\x1b', '', cleaned)

    # 3. Remove broken bracket sequences: [K, [1D, [2D, [0m, etc.
    cleaned = re.sub(r'\[\d*[A-Za-z]', '', cleaned)

    # 4. Remove non-printable control characters (keep newlines and tabs)
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', cleaned)

    # 5. Remove stray "1D", "2D", "3D" tokens (word-boundary)
    cleaned = re.sub(r'\b\d+[dD]\b', '', cleaned)

    # 6. Collapse multiple spaces (preserve newlines)
    cleaned = re.sub(r'[^\S\n]+', ' ', cleaned)

    # 7. Collapse multiple blank lines into one
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)

    return cleaned.strip()
