from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.domain._base import BaseEntity, RepresentableEntityMixin

if TYPE_CHECKING:
    from app.domain.api.entity.api import API


class APIField(BaseEntity, RepresentableEntityMixin):
    __tablename__ = "api_field"
    api_idx = Column(Integer, ForeignKey("api.idx"))
    api = relationship("API", cascade="all, delete")
    type = Column(String)
