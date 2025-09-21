from fastapi import APIRouter, Depends, Query, Body

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.user_manager import current_active_user
from app.session import get_async_session
from app.models import Producer
from app.schemas.entry import ProducerEdit 
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

