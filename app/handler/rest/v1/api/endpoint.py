from fastapi import APIRouter, status

from app.handler.rest.v1.api.dtos import APIResponeDTO, APIFieldInputDTO, APIInputDTO
from app.handler.rest.v1.api.service import apiService

router = APIRouter(prefix="/api")


@router.get("", reponse_model=APIResponeDTO, status_code=status.HTTP_200_OK)
async def get_api_list(limit: int, offset: int = 0):
    """전체 API 목록 조회"""
    api_list = await apiService.read()
    return api_list[offset : offset + limit]


@router.get("", reponse_model=APIResponeDTO, status_code=status.HTTP_200_OK)
async def search_api_with_name(api_name: str):
    """이름을 통한 API 조회"""
    return await apiService.retrieve_with_name(api_name)


@router.post("", response_model=APIResponeDTO)
async def create_api(
    api_object: APIInputDTO,
    api_field_object: APIFieldInputDTO,
    status_code=status.HTTP_201_CREATED,
):
    """API 정보를 받아 새로운 데이터를 생성"""
    return await apiService.create(api_object, api_field_object)


@router.patch("/{api_idx}")
async def update_api(
    api_idx: int, api_object: APIInputDTO, status_code=status.HTTP_200_OK
):
    """API 수정"""
    return await apiService.update_meta_data(api_idx, api_object)


@router.delete("/{api_idx}")
async def delete_api(api_idx: int, status_code=status.HTTP_200_OK):
    """id를 통한 API 삭제"""
    return await apiService.delete(api_idx)
