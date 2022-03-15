from typing import Sequence, TYPE_CHECKING

from sqlalchemy import Column, Enum, Integer, ForeignKey

from app.common.enum import DatasetStatus
from app.domain._base import BaseEntity
from app.domain._base.entity import RepresentableEntityMixin

if TYPE_CHECKING:
    from app.domain.segment.entity.segment import Segment



class SubSegment(BaseEntity, RepresentableEntityMixin):
    __tablename__= "subsegment"
    idx = Column(Integer, primary_key=True)
    param1 = Column(ForeignKey("parameter.idx"))
    param2 = Column(ForeignKey("parameter.idx"))
    name: str
    description: str