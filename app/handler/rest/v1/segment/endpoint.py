from fastapi import APIRouter, status

from app.handler.rest.v1.segment.dtos import (
    SegmentInputDTO,
    SegmentResponseDTO,
    ParameterInputDTO,
    DatasetResponeDTO,
)
from app.handler.rest.v1.segment.service import segmentService

router = APIRouter(prefix="/segment")


@router.get("", response_model=SegmentResponseDTO, status_code=status.HTTP_200_OK)
async def get_segment_list(limit: int, offset: int = 0):
    """
    segment 목록 조회
    """
    limit = offset + limit
    segment_list = await segmentService.read()
    return segment_list[offset:limit]


@router.get("", reponse_model=DatasetResponeDTO, status_code=status.HTTP_200_OK)
async def get_dataset_list(limit: int):
    """
    dataset 목록 조회
    """
    dataset_list = await segmentService.dataset_read()
    return dataset_list


@router.post("", response_model=SegmentResponseDTO)
async def create_segment(
    segment_object: SegmentInputDTO,
    parameter_object: ParameterInputDTO,
    status_code=status.HTTP_201_CREATED,
):
    """
    Segment 정보와 Parameter 정보를 받아 새로운 데이터 생성
    """
    return await segmentService.create(
        segment_object, parameter_object
    )  # 이 부분 다시 생각 필요


@router.get("/{segment_idx}", response_model=SegmentResponseDTO)
async def copy_segment(segment_idx: int, status_code=status.HTTP_201_CREATED):
    """
    id를 통한 segment entity 하나를 복사
    복사된 entity는 이름이 copy+ segment이름 같은 방식으로 새로운 이름 부여

    """
    return await segmentService.copy(segment_idx)


@router.delete("/{segment_idx}")
async def delete_segment(segment_idx: int, status_code=status.HTTP_200_OK):
    """
    id를 통한 segment 삭제
    """

    return await segmentService.delete(segment_idx)


@router.patch("/{segment_idx}/", response_model=SegmentResponseDTO)
async def update_segment_status(
    segment_idx: int, segment_object: SegmentInputDTO, status_code=status.HTTP_200_OK
):
    """
    id를 통한 segment 객체하나를 받아서 status값을 update
    """
    return await segmentService.update_status(segment_idx, segment_object)
