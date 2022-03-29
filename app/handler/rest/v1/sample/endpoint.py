from fastapi import APIRouter

from app.handler.rest.v1.sample.service import (
    LoanApplicationInput,
    LoanApplicationOut,
    loanApplicationService,
)

router = APIRouter(prefix="/sample")

@router.post("", response_model= LoanApplicationOut)
async def create_loan_application(loan_application: LoanApplicationInput):
    """대출 신청 정보를 등록"""
    return await loanApplicationService.create(loan_application)

@router.get("/{appl_id}", response_model=LoanApplicationOut)
async def get_application_info(appl_id: int):
    """id에 맞는 대출 신청 정보를 확인"""
    return await loanApplicationService.read(id=appl_id)