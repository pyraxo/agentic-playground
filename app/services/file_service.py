import io

import tiktoken
from unstructured.partition.auto import partition

encoding = tiktoken.encoding_for_model("gpt-4o-mini")


async def upload_file(file_content: bytes):
    # Convert bytes to a file-like object that has .read()
    file_obj = io.BytesIO(file_content)

    elements = partition(file=file_obj)

    print("\n\n".join([str(el) for el in elements]))

    return elements


def tokenize(text: str) -> int:
    return len(encoding.encode(text))
