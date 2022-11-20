from pydantic import BaseModel


class Comment(BaseModel):
    user_id: int
    text: str
    