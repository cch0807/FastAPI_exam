from app.domain._base import BaseEntityRepo
from app.domain.segment.entity import SubSegment


class SubSegmentRepo(BaseEntityRepo):
    __entity_class__ = SubSegment
