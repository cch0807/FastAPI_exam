from app.domain._base import BaseEntityRepo
from app.domain._base.repository import RepresentableEntityRepoMixin
from app.domain.segment.entity import Segment


class SegmentRepo(RepresentableEntityRepoMixin[Segment], BaseEntityRepo[Segment]):
    __entity_class__ = Segment
