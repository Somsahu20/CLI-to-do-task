from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CreateTask(BaseModel):
    title: str
    content: str | None = None

class ReturnTask(CreateTask):
    id: int
    # created_at: datetime
    completed: bool

    model_config = ConfigDict(from_attributes=True)

class UpdateTask(BaseModel):
    title: str | None = None
    content: str | None = None
    completed: bool | None = None