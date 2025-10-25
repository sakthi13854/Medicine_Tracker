from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src import database
from src.Schemas.adherence_schema import AdherenceLogs,AdherenceLogsResponse
from src.crud.adherence_crud import adherence_log

router = APIRouter(prefix="/Adherence", tags=["Adherence"])

@router.post("/", response_model=AdherenceLogsResponse)
async def adherence_add(user_id : int ,adherencelog: AdherenceLogs ,db: AsyncSession = Depends(database.get_db)):
    result = await adherence_log(db , adherencelog,user_id)
    return result