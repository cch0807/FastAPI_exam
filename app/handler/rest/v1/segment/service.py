from __future__ import annotations

from typing import NoReturn, List

from app.domain.segment import SegmentRepo, ParameterRepo, SubSegmentRepo
from app.handler.rest.v1._base import BaseService
from app.handler.rest.v1.segment import (
  SegmentResponseDTO,
  SegmentCreateDTO,
  SegmentInputDTO,
  DatasetResponseDTO
)

from app.domain.segment.entity import Segment, Parameter, SubSegment

class SegmentService(BaseService):
  seg_repo: SegmentRepo
  param_repo: ParameterRepo
  sub_seg_repo: SubSegmentRepo

  async def read(self, limit=None) -> List[SegmentResponseDTO]:
    """
    Segment 목록 조회
    """
    segments = self.seg_repo.retrieve(limit=limit)
    return [SegmentResponseDTO.from_orm(segment) for segment in segments]

  
  async def create(self, segment_create_object: SegmentCreateDTO) -> SegmentResponseDTO:
    """
    Segment Entity 하나를 추가

    Arguments: Segment_create_object: 생성할 segment 정보 값.

    Tips: Segment와 Parameter 값을 인자로 받아 한꺼번에 생성처리
    SubSegment도 함께 만들어야 하는지?
    """
    segment = Segment()
    segment.name = SegmentCreateDTO.name
    segment.description = SegmentCreateDTO.description
    segment = await self.seg_repo.save()

    parameter = Parameter()
    for parameter in segment_create_object.parameters:
      await self.param_repo.save(
        Parameter(
          segment_idx = segment.id,
          name = parameter.name,
          description= parameter.description,
          type = parameter.type,
          fomula = parameter.formula
        )
      )
    return SegmentResponseDTO.from_orm([segment, parameter])
  
  async def delete(self, idx: int) -> NoReturn:
    """
    Segment Entity 하나를 삭제

    Arguments: Segment Entity의 primary key 값
    
    체크박스에 체크된 것들이 삭제되는거니까 여러개가 한번에 삭제되야 하나?
    """

    await self.seg_repo.remove(idx)

  async def copy(self, idx: int) -> SegmentResponseDTO:
    """
    Segment Entity 하나를 복제

    Arguments: Segment Entity의 primary key 값
    """

    segment = await self.seg_repo.get(id=idx)
    copy_segment = segment
    copy_segment.name = "Copy_" + copy_segment.name
    copy_segment= await self.seg_repo.save(copy_segment)

    return SegmentResponseDTO.from_orm(copy_segment)

  async def update_status(self, idx: int, segment_obj: SegmentInputDTO) -> SegmentResponseDTO:
    segment = await self.seg_repo.get(id=idx)
    segment.status = segment_obj.status
    segment = await self.seg_repo.save(segment)

    return SegmentResponseDTO.from_orm(segment)

  async def dataset_get_by_name(self, name:str) -> DatasetResponseDTO:
    """
    DATASET 변수 조회
    
    Arguments: Dataset Entity 의 name 값

    dataset repo를 받아오는것 수정 필요
    """
    dataset = self.seg_repo.get_by_name(name = name)
    return DatasetResponseDTO.from_orm(dataset)

  async def dataset_read(self, limit=None) -> List[DatasetResponseDTO]:
    """
    Dataset 목록 조회
    """

    datasets = self.seg_repo.retrieve(limit=limit)
    return [DatasetResponseDTO.from_orm(dataset) for dataset in datasets]
  
  # async def dataset_condition_read(self, )



