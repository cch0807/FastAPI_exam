from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, JSON, String, TypeDecorator

from app.domain._base import BaseEntity, RepresentableEntityMixin

if TYPE_CHECKING:
    from app.domain.segment.entity.segment import Segment 

class ParameterFormula(TypeDecorator):
    impl = JSON

class Parameter(BaseEntity, RepresentableEntityMixin):
    idx = Column(Integer, primary_key=True)
    type = Column(String, comment="파라미터의 반환 타입")
    formula = Column(JSON, commnet="추출하는 계산식")
    segment_idx = Column(ForeignKey("segment.idx"))
    segment: Segment
    name: str
    description: str

