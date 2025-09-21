from pydantic import BaseModel

class ProducerEdit(BaseModel):
    id: int
    entry: str

class VocalEdit(BaseModel):
    id: int
    entry: str

class SongEdit(BaseModel):
    id: int
    entry: str

class SongList(BaseModel):
    producer_id: int
    song_id: int
