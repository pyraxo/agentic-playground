from beanie import Document


class File(Document):
    name: str
    text: str
    tokens: int = 0

    class Settings:
        name = "files"
        indexes = ["name"]
