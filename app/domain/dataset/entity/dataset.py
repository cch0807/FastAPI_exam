from typing import Sequence, TYPE_CHECKING

from sqlalchemy import Column, Enum, Integer

from app.common.enum import DatasetStatus
from app.domain._base import BaseEntity
from app.domain._base.entity import RepresentableEntityMixin

if TYPE_CHECKING:
    from app.domain.dataset.entity.dataset_field import DatasetField


class Dataset(BaseEntity, RepresentableEntityMixin):
    __tablename__ = "dataset"
    idx = Column(Integer, primary_key=True)
    status = Column(Enum(DatasetStatus))
    fields: Sequence[DatasetField]
    name: str
    description: str
