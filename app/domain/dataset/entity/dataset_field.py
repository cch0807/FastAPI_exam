from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, JSON, String, TypeDecorator

from app.domain._base import BaseEntity, RepresentableEntityMixin

if TYPE_CHECKING:
    from app.domain.dataset.entity.dataset import Dataset


class DatasetFormula(TypeDecorator):
    impl = JSON


class DatasetField(BaseEntity, RepresentableEntityMixin):
    idx = Column(Integer, primary_key=True)
    type = Column(String, comment="이 데이터셋 필드의 반환 타입. 계산식 결과와 일치해야 함.")
    formula = Column(JSON, comment="이 데이터셋 필드를 추출하는 계산식")
    dataset_idx = Column(ForeignKey("dataset.idx"))
    dataset: Dataset
    name: str
    description: str
