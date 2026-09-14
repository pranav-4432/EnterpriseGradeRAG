from langchain_text_splitters import RecursiveCharacterTextSplitter
import logfire


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[str]:
    """
    Split text into chunks using RecursiveCharacterTextSplitter.
    Ensures all execution paths return a list of strings.
    """
    if not text or not text.strip():
        return []

    with logfire.span("Chunking text", length=len(text)):
        try:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                separators=["\n\n", "\n", " ", ""],
            )
            chunks = splitter.split_text(text)
            return chunks
        except Exception as e:
            logfire.error(f"Chunking failed: {e}")
            return [text]
