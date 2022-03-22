from __future__ import annotations
from http.client import HTTPException

from typing import NoReturn, List

from app.domain.segment import SegmentRepo, ParameterRepo, SubSegmentRepo

from app.handler.rest.v1._base import BaseService, PagenatedResponse
from app.handler.rest.v1.segment import (
    SegmentResponseDTO,
    SegmentCreateDTO,
    SegmentPatchDTO,
    DatasetDetailResponseDTO,
    DatasetResponseDTO,
)
from app.common.enum.segment import SegmentStatus
from app.domain.segment.entity import Segment, Parameter, SubSegment


class SegmentService(BaseService):
    seg_repo: SegmentRepo
    param_repo: ParameterRepo
    sub_seg_repo: SubSegmentRepo

    async def read(
        self, cursor: int, size: int
    ) -> PagenatedResponse[SegmentResponseDTO]:
        """
        Segment 목록 조회
        """
        segments, cursor = await self.seg_repo.retrieve_for_pagenation(cursor, size)
        return PagenatedResponse[
            SegmentResponseDTO(
                segment=[SegmentResponseDTO.from_orm(segment) for segment in segments],
                size=size,
                cursor=cursor,
            )
        ]

    async def filter(self) -> List[SegmentResponseDTO]:
        """
        상태가 Requested 인 segment filter
        """
        segments = self.seg_repo.retreive_filter_requestsed()

        return [SegmentResponseDTO.from_orm(segment) for segment in segments]

    async def create(self, segment_object: SegmentCreateDTO) -> SegmentResponseDTO:
        """
        Segment Entity 하나를 추가

        Arguments: Segment_create_object: 생성할 segment 정보 값.

        Tips: Segment와 Parameter 값을 인자로 받아 한꺼번에 생성처리

        SubSegment도 함께 만들어야 하는지?
        """
        segment = Segment(**segment_object.dict(exclude="parameters, subsegment"))
        for parameter in [
            Parameter(**mapping)
            for mapping in segment_object.dict(include="parameters")["parameters"](
                exclude="subsegment"
            )
        ]:
            segment.parameter.append(parameter)
        
        # subsegment = SubSegment()
        # subsegment.name = segment.name
        # subsegment.description = segment.description
        # subsegment.param1 = segment.parameter[0].idx
        # subsegment.param2 = segment.parameter[1].idx

        # segment.parameter.subsegment.append(subsegment)
        segment = await self.seg_repo.save(segment)
        return SegmentResponseDTO.from_orm(segment)

    async def delete(self, idx_list: List[int]) -> NoReturn:
        """
        Segment Entity 하나를 삭제

        Arguments:
            idx_list: Segment Entity의 id값들
        """

        segment_list = [await self.seg_repo.get(id=idx) for idx in idx_list]
        for segment in segment_list:
            if segment.status == SegmentStatus.ACTIVE:
                raise HTTPException(status_code=400, detail="Not deleted")
            else:
                await self.seg_repo.remove(segment.id)

    async def copy(self, idx_list: List[int]) -> List[SegmentResponseDTO]:
        """
        사용자가 원하는 Segment Entity 복사

        Arguments:
            idx:Segment Entity의 id값들

        Tips:
            여러개의 Entity가 복사될 수 있다.
            id가 존재하지 않을 시 에러처리
        """

        segment_list = [await self.seg_repo.get(id=idx) for idx in idx_list]
        if segment_list:
            for segment in segment_list:
                segment.name = "Copy_" + segment.name

            copied_segment = await self.seg_repo.save_all(**segment_list)
            return SegmentResponseDTO.from_orm(copied_segment)

        else:
            raise HTTPException(status_code=404, detail="Not found")

    async def update_status(
        self, idx_list: List[int], segment_obj: SegmentPatchDTO
    ) -> List[SegmentResponseDTO]:

        """
        사용자가 원하는 Segment Entity status update

        Arguments:
            idx:Segment Entity의 id
            segment_obj: 변경될 status값

        Tips:

        """

        segment_list = [await self.seg_repo.get(id=idx) for idx in idx_list]
        if segment_list:
            for segment in segment_list:
                if segment_obj.status == "Requested":
                    if segment.status == SegmentStatus.ACTIVE:
                        raise HTTPException(status_code=400, detail="Not Accepted")
                    else:
                        segment.status = segment_obj.status

                elif segment_obj.status == "Active":
                    if segment.status != SegmentStatus.REQUESTED:
                        raise HTTPException(status_code=400, detail="Not Accepted")
                    else:
                        segment.status = segment_obj.status

                elif segment_obj.status == "Inactive":
                    if segment.status != SegmentStatus.REQUESTED:
                        raise HTTPException(status_code=400, detail="Not Accepted")
                    else:
                        segment.status = segment_obj.status
                segment = await self.seg_repo.save(segment)

        else:
            raise HTTPException(status_code=404, detail="Not found")

        return SegmentResponseDTO.from_orm(segment)

    async def get_dataset(self, idx: int) -> DatasetDetailResponseDTO:
        """
        DATASET 1개 조회

        Arguments:

            name: Dataset Entity 의 name
            idx : Dataset Entity 의 id

        dataset repo를 받아오는것 수정 필요
        """
        dataset = await self.api_repo.get(id=idx)
        if dataset:
            return DatasetDetailResponseDTO.from_orm(dataset)
        else:
            raise HTTPException(status_code=404, detail="Not found")

    async def read_dataset(self) -> List[DatasetResponseDTO]:
        """
        Dataset 목록 조회
        """

        datasets = self.seg_repo.retrieve_dataset()
        return [DatasetResponseDTO.from_orm(dataset) for dataset in datasets]


segmentService = SegmentService(
    seg_repo=SegmentRepo(), param_repo=ParameterRepo(), sub_seg_repo=SubSegmentRepo()
)
