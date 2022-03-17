from app.domain._base import BaseEntityRepo
from app.domain._base.repository import RepresentableEntityRepoMixin
from app.domain.dataset.entity import Dataset


class DatasetRepo(RepresentableEntityRepoMixin[Dataset], BaseEntityRepo[Dataset]):
    __entity_class__ = Dataset
