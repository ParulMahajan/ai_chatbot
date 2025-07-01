from enum import Enum

class DocumentType(str,Enum):
    PDF = "pdf"
    TXT = "txt"
    RTF = "rtf"

ALLOWED_EXTENSIONS = {
    DocumentType.RTF: {'rtf', 'rtfd'},
    DocumentType.TXT: {'txt'},
    DocumentType.PDF: {'pdf'},
}