from app.ingestion.loaders.html import parse_html
from app.ingestion.loaders.office import parse_office
from app.ingestion.loaders.pdf import parse_pdf
from app.ingestion.loaders.text import parse_text

__all__ = ["parse_html", "parse_office", "parse_pdf", "parse_text"]
