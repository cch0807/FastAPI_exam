from typing import Sequence, TYPE_CHECKING

from sqlalchemy import Column, Enum, Integer

from app.common.enum import DatasetStatus
from app.domain._base import BaseEntity
from app.domain._base.entity import RepresentableEntityMixin

if TYPE_CHECKING:
    from app.domain.segment.entity.subsegment import Parameter



class Segment(BaseEntity, RepresentableEntityMixin):
    __tablename__= "segment"
    idx = Column(Integer, primary_key=True)
    status = Column(Enum(DatasetStatus))
    parameter: Sequence[Parameter]
    name: str
    description: str