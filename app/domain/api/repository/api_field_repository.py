from app.domain._base import BaseEntityRepo

from app.domain.api.entity import APIField


class APIFieldRepository(BaseEntityRepo):
    __entity_class__ = APIField


apiFieldRepository = APIFieldRepository()
