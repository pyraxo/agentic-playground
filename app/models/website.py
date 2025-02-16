from beanie import Document


class Website(Document):
    path: str
    content: str

    class Settings:
        name = "websites"
        indexes = ["path"]
