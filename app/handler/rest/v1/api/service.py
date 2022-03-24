from __future__ import annotations

from typing import NoReturn

from fastapi import HTTPException

from app.domain.api.entity import API, APIField
from app.domain.api.repository import APIFieldRepository, APIRepository
from app.handler.rest.v1._base import BaseService
from app.handler.rest.v1._base.dto import PaginatedResponse
from app.handler.rest.v1.api.dto import (
    APICreateDTO,
    APIDetailResponseDTO,
    APIPatchDTO,
    APIResponeDTO,
)


class APIService(BaseService):
    api_repo: APIRepository
    api_field_repo: APIFieldRepository

    async def get_one(self, idx: int) -> APIDetailResponseDTO:
        """API 1개 조회. 필드 포함."""
        obj = await self.api_repo.get(id=idx)
        if obj:
            return APIDetailResponseDTO.from_orm(obj)
        else:
            # TODO: detail 메시지 수정
            raise HTTPException(status_code=404, detail=f"API idx={idx} not found.")

    async def retrieve(
        self,
        *,
        name: str,
        cursor: int,
        size: int,
    ) -> PaginatedResponse[APIResponeDTO]:
        """API 리스트 조회"""
        apis, cursor = await self.api_repo.retrieve_for_pagination(
            name=name, size=size, cursor=cursor
        )
        return PaginatedResponse[APIResponeDTO](
            datas=[APIResponeDTO.from_orm(api) for api in apis],
            size=size,
            cursor=cursor,
        )

    async def create(self, api_create_object: APICreateDTO) -> APIDetailResponseDTO:
        """
        API Entity 하나를 추가

        Arguments:
            api_create_object: 생성할 api 정보 값.

        Tips:
            API와 APIField 값을 인자로 받아 한꺼번에 생성처리.
        """
        api = API(**api_create_object.dict(exclude={"fields"}))
        # for api_field in [
        #     APIField(**mapping)
        #     for mapping in api_create_object.dict(include={"fields"})["fields"]
        # ]:

        api_fields = [
            {
                "api_idx": api.idx,
                "name": "field1",
                "type": "enum",
                "type_attribute": {"gender": "male"},
            },
            {
                "api_idx": api.idx,
                "name": "field2",
                "type": "text",
                "type_attribute": {"address": "hanoi"},
            },
            {
                "api_idx": api.idx,
                "name": "field3",
                "type": "enum",
                "type_attribute": {"company_size": "A"},
            },
            {
                "api_idx": api.idx,
                "name": "field4",
                "type": "boolean",
                "type_attribute": {"lay_payment": "True"},
            },
        ]

        for api_field in api_fields:
            api_field_obj = APIField(**api_field)
            api.fields.append(api_field_obj)

        api = await self.api_repo.save(api)

        return APIResponeDTO.from_orm(api)

    async def update_meta_data(
        self, idx: int, api_object: APIPatchDTO
    ) -> APIResponeDTO:
        """
        API Entity 하나를 수정

        Arguments:
            idx: API Entity의 primary_key 값.
            api_object: 수정할 내용 값.
        """
        api = await self.api_repo.get(id=idx, for_update=True)
        if api:
            api.name = api_object.name
            api.description = api_object.description
            api.url = api_object.url
            api = await self.api_repo.save(api)
        else:
            # TODO: detail 메시지 수정
            raise HTTPException(status_code=404, detail="Not found")

        return APIResponeDTO.from_orm(api)

    async def delete(self, idx: int) -> NoReturn:
        """
        API Entity 하나를 삭제

        Arguments:
            idx: API Entity의 primary_key 값.
        """
        await self.api_repo.remove(idx)


apiService = APIService(api_repo=APIRepository(), api_field_repo=APIFieldRepository())