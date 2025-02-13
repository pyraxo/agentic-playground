from beanie import Document


class Website(Document):
    path: str
    content: str
