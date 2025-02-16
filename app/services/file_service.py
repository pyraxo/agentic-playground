import io
from hashlib import sha256

import tiktoken
from fastapi import UploadFile
from unstructured.partition.auto import partition

from app.models.file import File

encoding = tiktoken.encoding_for_model("gpt-4o-mini")


async def process_file(file: UploadFile):
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


def tokenize(text: str) -> int:
    return encoding.encode(text)
