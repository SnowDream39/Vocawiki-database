from fastapi import APIRouter, Depends, Query, Body, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_
from sqlalchemy.dialects.postgresql import insert

from app.user_manager import current_active_user
from app.session import get_async_session
from app.models import Song
from app.schemas.entry import SongEdit

router = APIRouter(prefix="/song", tags=["song"])

@router.get("")
async def get_songs_entrie(
    ids: list[int] = Query(...),
    session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Song).where(Song.id.in_(ids))
    result = await session.execute(stmt)
    songs = result.scalars().all()
    return songs

@router.get("/id")
async def search_song_ids(
    entry: str = Query(...),
    session: AsyncSession = Depends(get_async_session)
):
    """
    一个歌曲条目可以对应多个id
    """
    stmt = select(Song.id).where(Song.entry == entry)
    result = await session.execute(stmt)
    ids = result.scalars().all()
    return ids


@router.post("/upsert")
async def upsert_songs(
    update_songs: list[SongEdit] = Body(...),
    user = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    values = [p.model_dump() for p in update_songs]

    stmt = insert(Song).values(values)
    stmt = stmt.on_conflict_do_update(
        index_elements=["id"],  # 以 id 作为唯一约束
        set_={  # 冲突时更新的字段
            "entry": stmt.excluded.entry
        }
    )

    await session.execute(stmt)
    await session.commit()
    return {"status": "ok"}