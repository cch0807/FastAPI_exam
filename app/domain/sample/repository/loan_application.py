from __future__ import anotations

from typing import Iterable

from sqlalchemy import lambda_stmt, select, update

from app.common.enum import ApplicationStatus
from app.domain._base import BaseEntityRepo, BaseEntity
from app.domain.sample.entity.loan_application import LoanApplication
from app.core.config.data_source_configurer import session

class LoanApplicationRepo(BaseEntityRepo[LoanApplication]):
    __entity_class__ = LoanApplication

    async def retrieve_finished(
        self, limit: int | None = None
    ) -> Iterable[LoanApplication]:
        return await session.scalars(
            select(LoanApplication)
            .where(LoanApplication.is_finished == True)
            .limit(limit)
        )
    
    async def retrieve_by_amount(
        self, amount_ge: int, amount_lt: int, limit: int | None = None
    ) -> Iterable[LoanApplication]:
        stmt = lambda_stmt(
            select(LoanApplication)
            .where(LoanApplication >= amount_ge, LoanApplication.amount < amount_lt)
            .limit(limit)
        )

        return await session.scalars(stmt(amount_ge, amount_lt, limit))
    
    async def update_processing_as_pending(self) -> Iterable[Entity]:
        return await session.scalars(
            update(LoanApplication)
            .where(LoanApplication.status == ApplicationStatus.PROCESSING)
            .values(status=ApplicationStatus.PENDING)
            .returning(LoanApplication)
        )
