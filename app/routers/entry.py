from fastapi import APIRouter, Depends, Query, Body

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update

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
  
@router.post("/producer/add")
async def add_producers(
    update_producers: list[ProducerEdit] = Body(),
    session: AsyncSession = Depends(get_async_session)
):
    values = [p.model_dump() for p in update_producers]
    stmt = insert(Producer).values(values)
    await session.execute(stmt)
    await session.commit()

@router.post("/producer/edit")
async def edit_producers(
    update_producers: list[ProducerEdit] = Body(),
    session: AsyncSession = Depends(get_async_session)
):
    values = [p.model_dump() for p in update_producers]
    await session.execute(update(Producer), values)
    await session.commit()

