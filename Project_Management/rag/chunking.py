# ============================================================
# PROJECT HUB RAG - RECURSIVE CHUNKING
# ============================================================

from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter


# ------------------------------------------------------------
# Chunk Configuration
# ------------------------------------------------------------

DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 100


# ------------------------------------------------------------
# Create Recursive Text Splitter
# ------------------------------------------------------------

def get_text_splitter() -> RecursiveCharacterTextSplitter:

    return RecursiveCharacterTextSplitter(
        chunk_size=DEFAULT_CHUNK_SIZE,
        chunk_overlap=DEFAULT_CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ],
        length_function=len,
    )


# ------------------------------------------------------------
# Chunk Text
# ------------------------------------------------------------

def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> List[str]:

    # --------------------------------------------------------
    # Validate Input
    # --------------------------------------------------------

    if not text or not text.strip():
        return []

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0."
        )

    if chunk_overlap < 0:
        raise ValueError(
            "chunk_overlap cannot be negative."
        )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size."
        )

    # --------------------------------------------------------
    # Create Splitter
    # --------------------------------------------------------

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ],
        length_function=len,
    )

    # --------------------------------------------------------
    # Split Text
    # --------------------------------------------------------

    chunks = splitter.split_text(
        text.strip()
    )

    return [
        chunk.strip()
        for chunk in chunks
        if chunk.strip()
    ]