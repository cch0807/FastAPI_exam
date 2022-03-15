from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from app.domain._base import BaseEntity, RepresentableEntityMixin

if TYPE_CHECKING:
    from app.domain.api.entity.api_field import APIField


class API(BaseEntity, RepresentableEntityMixin):
    __tablename__ = "api"
    idx = Column(Integer, primary_key=True)
    fields = relationship("APIField", uselist=True)
