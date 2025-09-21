from fastapi import APIRouter, Depends, Query, Body, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_
from sqlalchemy.dialects.postgresql import insert

from app.user_manager import current_active_user
from app.session import get_async_session
from app.models import Producer, ProducerSong
from app.schemas.entry import ProducerEdit, ProducerSongAdd, ProducerSongRemove, ProducerSongOut

router = APIRouter(prefix="/entry", tags=["entry"])

@router.get("/producer")
async def get_producers_entrie(
    ids: list[int] = Query(...),
    session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Producer).where(Producer.id.in_(ids))
    result = await session.execute(stmt)
    producers = result.scalars().all()
    return producers

@router.get("/producer/id")
async def search_producer_id(
    entry: str = Query(...),
    session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Producer.id).where(Producer.entry == entry)
    result = await session.execute(stmt)
    ids = result.scalars().all()
    if not ids:
        raise HTTPException(status_code=404, detail="Not Found")
    return ids[0]

@router.post("/producer/upsert")
async def upsert_producers(
    update_producers: list[ProducerEdit] = Body(...),
    session: AsyncSession = Depends(get_async_session),
):
    values = [p.model_dump() for p in update_producers]

    stmt = insert(Producer).values(values)
    stmt = stmt.on_conflict_do_update(
        index_elements=["id"],  # 以 id 作为唯一约束
        set_={  # 冲突时更新的字段
            "entry": stmt.excluded.entry
        }
    )

    await session.execute(stmt)
    await session.commit()
    return {"status": "ok"}

@router.get("/producer/song", response_model=list[ProducerSongOut])
async def get_producer_song(
    id: int = Query(...),
    session: AsyncSession = Depends(get_async_session)
):
    stmt = select(ProducerSong).where(ProducerSong.producer_id == id)
    result = await session.execute(stmt)
    producers =  result.scalars().all()
    return producers

@router.get("/producer/song/check")
async def check_producer_song(
    producer_id: int = Query(...),
    song_id: int = Query(...),
    session: AsyncSession = Depends(get_async_session)
):
    stmt = select(ProducerSong).where(and_(
        ProducerSong.producer_id == producer_id,
        ProducerSong.song_id == song_id
    ))
    result = await session.execute(stmt)
    producers =  result.scalars().all()
    if producers:
        return True
    else:
        return False


@router.post("/producer/song")
async def add_producer_song(
    song: ProducerSongAdd = Body(...),
    session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(ProducerSong).values(song.model_dump())
    stmt = stmt.on_conflict_do_update(
        index_elements=["producer_id", "song_id"],
        set_={
            "description": stmt.excluded.description
        }
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "ok"}

@router.delete("/producer/song")
async def remove_producer_song(
    song: ProducerSongRemove = Body(...),
    session: AsyncSession = Depends(get_async_session)
):
    stmt = delete(ProducerSong).where(and_(
        ProducerSong.producer_id == song.producer_id,
        ProducerSong.song_id == song.song_id
    ))
    await session.execute(stmt)
    await session.commit()
    return {"status": "ok"}

