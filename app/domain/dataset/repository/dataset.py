from __future__ import annotations

from typing import List

from sqlalchemy import func, select

from app.domain._base import BaseEntityRepo
from app.domain._base.repository import RepresentableEntityRepoMixin
from app.domain.api.entity import API
from app.domain.dataset.entity import Dataset
from app.infra.db import session


class DatasetRepo(RepresentableEntityRepoMixin[Dataset], BaseEntityRepo[Dataset]):
    __entity_class__ = Dataset

    async def retrieve_for_pagination(
        self, *, api_idx: int, cursor: int, size: int
    ) -> tuple[List[Dataset], int | None]:
        """
        Dataset 검색, Pagination 적용

        Tips:
            특정 API idx 값을 가진 Dataset만 필터링하여 조회 가능
        """
        stmt = select(Dataset).limit(size).where(Dataset.idx > cursor)
        if api_idx:
            stmt = stmt.where(api_idx == api_idx)

        results = list(await session.scalars(stmt))
        cursor = None
        if results:
            cursor = results[-1].idx
        return results, cursor

    async def retrieve_one(self, idx: int) -> Dataset:
        """
        하나의 Dataset을 조회

        Arguments:
            idx: 조회할 Dataset의 id

        Tips:
            Dataset과 DatasetField 테이블을 조인하여 조회
        """
        return await session.scalars(
            select(Dataset, API.name)
            .join(API, Dataset.api_idx == API.idx)
            .where(idx == idx)
        )

    async def get_total_count(self) -> int:
        """Dataset 전체 리스트 개수 조회"""
        return await session.scalars(select(func.count()).select_from(Dataset))


datasetRepo = DatasetRepo()
