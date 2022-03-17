from app.domain._base import BaseEntityRepo
from app.domain.dataset.entity import DatasetField


class DatasetFieldRepo(BaseEntityRepo):
    __entity_class__ = DatasetField
