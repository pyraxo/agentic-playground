import io

import tiktoken
from fastapi import UploadFile
from unstructured.partition.auto import partition

from app.models import File

encoding = tiktoken.encoding_for_model("gpt-4o-mini")


async def process_file(file: UploadFile):
    contents = await file.read()
    elements = partition(file=io.BytesIO(contents))

    text = "\n".join([str(el) for el in elements])

    tokens = tokenize(text)

    file_doc = File(name=file.filename, text=text, tokens=len(tokens))
    await file_doc.insert()

    return file_doc


def tokenize(text: str) -> int:
    return encoding.encode(text)
