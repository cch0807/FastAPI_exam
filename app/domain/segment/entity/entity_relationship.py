from sqlalchemy.orm import relationship

from app.domain.segment.entity.segment import Segment
from app.domain.segment.entity.subsegment import SubSegment
from app.domain.segment.entity.parameter import Parameter


def make_relationship():
    Segment.parameter = relationship("Parameter", uselist=True)
    Parameter.segment = relationship("Segment")
    
    Parameter.subsegment = relationship("Subsegment", uselist=True)
    SubSegment.parameter = relationship("Parameter")
