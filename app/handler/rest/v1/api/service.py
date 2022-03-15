from __future__ import annotations

from typing import NoReturn, List

from app.domain.api.repository import APIRepository, APIFieldRepository
from app.handler.rest.v1._base import BaseService
from app.handler.rest.v1.api import APIResponeDTO, APIInputDTO, APICreateDTO
from app.domain.api.entity import API, APIField


class APIService(BaseService):
    api_repo: APIRepository
    api_field_repo: APIFieldRepository

    async def read(self, limit=None) -> List[APIResponeDTO]:
        """
        API 전체 리스트 조회
        """
        apis = self.api_repo.retrieve(limit=limit)
        return [APIResponeDTO.from_orm(api) for api in apis]

    async def create(self, api_create_object: APICreateDTO) -> APIResponeDTO:
        """
        API Entity 하나를 추가

        Arguments:
            api_field_object: 생성할 api 정보 값.

        Tips:
            API와 APIField 값을 인자로 받아 한꺼번에 생성처리.
        """
        api = API()
        api.name = api_create_object.name
        api.description = api_create_object.description
        api = await self.api_repo.save(api)

        api_field = APIField()
        for api_field in api_create_object.field:
            await self.api_field_repo.save(
                APIField(
                    api_idx=api.id,
                    name=api_field.name,
                    description=api_field.description,
                    type=api_field.type,
                )
            )

        return APIResponeDTO.from_orm([api, api_field])

    async def update_meta_data(
        self, idx: int, api_object: APIInputDTO
    ) -> APIResponeDTO:
        """
        API Entity 하나를 수정

        Arguments:
            idx: API Entity의 primary_key 값.
            api_object: 수정할 내용 값.
        """
        api = await self.api_repo.get(id=idx, for_update=True)
        api.name = api_object.name
        api.description = api_object.description
        api = await self.api_repo.save(api)

        return APIResponeDTO.from_orm(api)

    async def delete(self, idx: int) -> NoReturn:
        """
        API Entity 하나를 삭제

        Arguments:
            idx: API Entity의 primary_key 값.
        """
        await self.api_repo.remove(idx)

    async def retrieve_with_name(self, name: str):
        """
        이름으로 API 조회

        Arguments:
            name: 조회할 API Entity의 이름.
        """
        api = await self.api_repo.retrieve_with_name(name)
        return APIResponeDTO.from_orm(api)


apiService = APIService(api_repo=APIRepository(), api_field_repo=APIFieldRepository())
