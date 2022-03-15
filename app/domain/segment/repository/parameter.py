from app.domain._base import BaseEntityRepo
from app.domain.segment.entity import Parameter


class ParameterRepo(BaseEntityRepo):
    __entity_class__ = Parameter
