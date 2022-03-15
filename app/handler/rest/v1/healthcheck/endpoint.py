from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/health")


class Health(BaseModel):
    health: bool = True


health = Health()


@router.get("", response_model=Health, include_in_schema=False)
async def healthcheck() -> Health:
    return health
