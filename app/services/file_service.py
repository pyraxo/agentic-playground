import io
from hashlib import sha256

import tiktoken
from courlan import clean_url
from fastapi import UploadFile
from unstructured.partition.auto import partition
from unstructured.partition.html import partition_html

from app.models.file import File

encoding = tiktoken.encoding_for_model("gpt-4o-mini")


async def process_file(file: UploadFile):
    """Process a file and return a File object.

    Args:
        file (UploadFile): The file to process.

    Returns:
        File: The processed File object.
    """
    contents = await file.read()
    file_hash = sha256(contents).hexdigest()

    if file_doc := await File.find_one(File.hash == file_hash):
        return file_doc

    elements = partition(file=io.BytesIO(contents))

    text = "\n".join([str(el) for el in elements])

    tokens = tokenize(text)

    file_doc = File(name=file.filename, text=text, tokens=len(tokens), hash=file_hash)
    await file_doc.insert()

    return file_doc


async def process_website(url: str):
    """Process a website and return a File object.

    Args:
        url (str): The URL of the website to process.

    Returns:
        File: The processed File object.
    """
    cleaned_url = clean_url(url)
    elements = partition_html(url=cleaned_url)

    # text = "\n".join([el.text for el in elements if isinstance(el, NarrativeText)])
    text = "\n".join([str(el) for el in elements])
    tokens = tokenize(text)

    if file_doc := await File.find_one(File.name == cleaned_url):
        return file_doc

    file_doc = File(name=cleaned_url, text=text, tokens=len(tokens))
    await file_doc.insert()

    return file_doc


def tokenize(text: str) -> int:
    """Tokenize a text string.

    Args:
        text (str): The text to tokenize.

    Returns:
        int: The number of tokens in the text.
    """
    return encoding.encode(text)
