import json
import os
from datetime import datetime

DOCUMENTS_FILE = "documents.json"
DOCUMENTS_FOLDER = "documents"


def load_documents():
    """Load saved medical documents."""

    if not os.path.exists(DOCUMENTS_FILE):
        return []

    try:
        with open(DOCUMENTS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except (json.JSONDecodeError, OSError):
        return []


def save_documents(documents):
    """Save document information."""

    with open(
        DOCUMENTS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            documents,
            file,
            indent=4,
            ensure_ascii=False
        )


def add_document(
    title,
    category,
    filename
):
    """Add a document record."""

    documents = load_documents()

    new_document = {
        "title": title,
        "category": category,
        "filename": filename,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    documents.append(new_document)

    save_documents(documents)

    return new_document


def delete_document(index):
    """Delete a document record."""

    documents = load_documents()

    if 0 <= index < len(documents):

        document = documents.pop(index)

        save_documents(documents)

        return document

    return None


def get_document_count():
    """Return number of saved documents."""

    return len(load_documents())