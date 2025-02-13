from beanie import Document


class File(Document):
    name: str
    text: str
    tokens: int = 0

    class Config:
        schema_extra = {
            "example": {
                "name": "example.pdf",
                "text": "This is the extracted text from the file.",
                "tokens": 100,
            }
        }

    class Settings:
        name = "files"
        indexes = ["name"]
