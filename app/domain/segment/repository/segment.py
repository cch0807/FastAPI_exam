from __future__ import annotations

from typing import Iterable
from sqlalchemy import select

from app.domain._base import BaseEntityRepo
from app.domain._base.repository import RepresentableEntityRepoMixin
from app.domain.segment.entity import Segment
from app.infra.db import session


class SegmentRepo(RepresentableEntityRepoMixin[Segment], BaseEntityRepo[Segment]):
    __entity_class__ = Segment

    async def retreive_filter_requestsed(
        self, limit: int | None = None
    ) -> Iterable[Segment]:
        """
        Requestsed 된 segment 조회
        """
        return await session.scalars(select(Segment).filter_by(status="Requested"))

    async def retrieve_dataset(self, limit: int | None = None) -> Iterable[Segment]:
        """
        Segment를 dataset으로 가정
        Activated 된 dataset 조회
        """
        return await session.scalars(select(Segment).filter_by(status="Active"))

    async def retrieve_for_pagenation(
        self, size: int, cursor: int
    ) -> tuple[list[Segment], int | None]:
        """Segment 조회 쿼리"""
        stmt = select(Segment).limit(size).where(Segment.idx > cursor)
        results = list(await session.scalars(stmt))
        cursor = None
        if results:
            cursor = results[-1].idx
        else:
            cursor = 0

        return results, cursor


segmentRepo = SegmentRepo()
