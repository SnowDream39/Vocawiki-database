from pydantic import BaseModel

class ProducerEdit(BaseModel):
    id: int
    entry: str

