from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.common.enum.sample import ApplicationStatus
from app.domain.sample import LoanApplication, LoanApplicationRepo, loanApplicationRepo
from app.handler.rest.v1._base import BaseService

router = APIRouter(prefix="/sample")


class LoanApplicationInput(BaseModel):
    amount: int
    comment: str

    class Config:
        orm_mode = True


class LoanApplicationOut(BaseModel):
    id: int
    amount: int
    comment: str
    status: ApplicationStatus

    class Config:
        orm_mode = True


class LoanApplicationService(BaseService):
    repo: LoanApplicationRepo

    async def create(
        self, loan_application: LoanApplicationInput
    ) -> LoanApplicationOut:
        obj = LoanApplication(**loan_application.dict())
        obj = await self.repo.save(obj)
        return LoanApplicationOut.from_orm(obj)

    async def read(self, id: int) -> LoanApplicationOut:
        obj = await self.repo.get(id)
        if obj:
            return LoanApplicationOut.from_orm(obj)
        else:
            raise HTTPException(
                status_code=404, detail=f"LoanApplication {id} is not exist."
            )


loanApplicationService = LoanApplicationService(repo=loanApplicationRepo)
