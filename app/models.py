from sqlalchemy import ForeignKey, String, Integer, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime, timezone

utc = timezone.utc

class Base(DeclarativeBase):
    pass

class CommonEntry:
    """
    VocaDB 和 Vocawiki 都有条目的对象。
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="VocaDB的id")
    entry: Mapped[int] = mapped_column(String(100), comment="萌百条目名")
    pass

class User(SQLAlchemyBaseUserTable, Base):
    """
    我们系统的用户，包括编辑者和管理员等
    """
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(length=32), nullable=False, server_default="temp")

    class Config:
        from_attributes = True

class EditLog(Base):
    """
    编辑记录。非管理员的编辑需要被审核后才能写入。
    """
    __tablename__ = "edit_log"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    old_content: Mapped[dict] = mapped_column(JSONB)
    new_content: Mapped[dict] = mapped_column(JSONB)
    edited_by: Mapped[int] = mapped_column(ForeignKey("user.id"))
    edited_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(utc))
    approved_by: Mapped[int] = mapped_column(ForeignKey("user.id"))
    approved_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(utc))

class Producer(Base, CommonEntry):
    """
    P主
    """
    __tablename__ = "producer"

    songs_blacklist: Mapped[list["ProducerSongBlacklist"]] = relationship("ProducerSongBlacklist", back_populates="producer")
    songs_whitelist: Mapped[list["ProducerSongWhitelist"]] = relationship("ProducerSongWhitelist", back_populates="producer")

class Vocal(Base, CommonEntry):
    """
    歌手
    """
    __tablename__ = "vocal"

class Song(Base, CommonEntry):
    """
    歌曲
    """
    __tablename__ = "song"

class ProducerSongBlacklist(Base):
    __tablename__ = 'producer_song_blacklist'
    id: Mapped[int] = mapped_column(primary_key=True)
    producer_id: Mapped[int] = mapped_column(ForeignKey("producer.id"))
    song_id: Mapped[int] = mapped_column(ForeignKey("song.id"))

    producer: Mapped["Producer"] = relationship("Producer", back_populates="songs_blacklist")
    song: Mapped["Song"] = relationship("Song")


class ProducerSongWhitelist(Base):
    __tablename__ = 'producer_song_whitelist'
    id: Mapped[int] = mapped_column(primary_key=True)
    producer_id: Mapped[int] = mapped_column(ForeignKey("producer.id"))
    song_id: Mapped[int] = mapped_column(ForeignKey("song.id"))

    producer: Mapped["Producer"] = relationship("Producer", back_populates="songs_whitelist")
    song: Mapped["Song"] = relationship("Song")
