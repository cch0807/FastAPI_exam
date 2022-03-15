from __future__ import annotations

from typing import NoReturn, List

from app.domain.segment import SegmentRepo, ParameterRepo, SubSegmentRepo
from app.handler.rest.v1._base import BaseService
from app.handler.rest.v1.segment import (
  SegmentResponseDTO,
  SegmentCreateDTO
)

from app.domain.segment.entity import Segment, Parameter, SubSegment

class SegmentService(BaseService):
  seg_repo: SegmentRepo
  param_repo: ParameterRepo
  sub_seg_repo: SubSegmentRepo

  async def read(self, limit=None) -> List[SegmentResponseDTO]:
    """
    Segment 전체 리스트 조회
    """
    segments = self.seg_repo.retrieve(limit=limit)
    return [SegmentResponseDTO.from_orm(segment) for segment in segments]

  
  async def create(self, segment_create_object: SegmentCreateDTO) -> SegmentResponseDTO:
    """
    Segment Entity 하나를 추가

    Arguments: Segment_create_object: 생성할 segment 정보 값.

    Tips: Segment와 Parameter 값을 인자로 받아 한꺼번에 생성처리
    """


