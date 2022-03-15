from sqlalchemy import select
from app.domain._base import BaseEntityRepo
from app.domain.api.entity import API
from app.infra.db import session


class APIRepository(BaseEntityRepo):
    __entity_class__ = API

    async def retrieve_with_name(self, name: str):
        """이름을 통한 API 검색"""
        return await session.scalars(select(API).where(API.name == name))


apiRepository = APIRepository()
