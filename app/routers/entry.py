from fastapi import APIRouter, Depends, Query, Body, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, or_
from sqlalchemy.dialects.postgresql import insert

from app.user_manager import current_active_user
from app.session import get_async_session
from app.models import Producer, ProducerSongBlacklist, ProducerSongWhitelist
from app.schemas.entry import ProducerEdit, SongList
router = APIRouter(prefix="/entry")

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
        return HTTPException(status_code=404, detail="Not Found")
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

@router.post("/producer/song/blacklist/add")
async def add_song_blacklist(
    song_list: list[SongList] = Body(...),
    session: AsyncSession = Depends(get_async_session)
):
    values = [p.model_dump() for p in song_list]
    stmt = insert(ProducerSongBlacklist).values(values)
    stmt = stmt.on_conflict_do_nothing(
        index_elements=["producer_id", "song_id"]
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "ok"}

@router.post("/producer/song/whitelist/add")
async def add_song_whitelist(
    song_list: list[SongList] = Body(...),
    session: AsyncSession = Depends(get_async_session)
):
    values = [p.model_dump() for p in song_list]
    stmt = insert(ProducerSongWhitelist).values(values)
    stmt = stmt.on_conflict_do_nothing(
        index_elements=["producer_id", "song_id"]
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "ok"}

@router.delete("/producer/song/blacklist/remove")
async def remove_song_blacklist(
    song_list: list[SongList] = Body(...),
    session: AsyncSession = Depends(get_async_session)
):
    values = [p.model_dump() for p in song_list]
    conditions = [
        (ProducerSongBlacklist.producer_id == v["producer_id"]) &
        (ProducerSongBlacklist.song_id == v["song_id"])
        for v in values
    ]

    if conditions:
        stmt = delete(ProducerSongBlacklist).where(or_(*conditions))
        result = await session.execute(stmt)
        await session.commit()
        return {"deleted": result.rowcount}

@router.delete("/producer/song/whitelist/remove")
async def remove_song_whitelist(
    song_list: list[SongList] = Body(...),
    session: AsyncSession = Depends(get_async_session)
):
    values = [p.model_dump() for p in song_list]
    conditions = [
        (ProducerSongWhitelist.producer_id == v["producer_id"]) &
        (ProducerSongWhitelist.song_id == v["song_id"])
        for v in values
    ]

    if conditions:
        stmt = delete(ProducerSongWhitelist).where(or_(*conditions))
        result = await session.execute(stmt)
        await session.commit()
        return {"deleted": result.rowcount}


