from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CreateTask(BaseModel):
    title: str
    content: str | None = None

class ReturnTask(CreateTask):
    id: int
    created_at: datetime
    completed: bool

    model_config = ConfigDict(from_attributes=True)