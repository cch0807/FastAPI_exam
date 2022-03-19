from app.domain._base import BaseEntityModule
from app.domain.sample.repository import LoanApplicationRepo, loanApplicationRepo


class LoanApplicationModule(BaseEntityModule[LoanApplicationRepo]):
    repo: LoanApplicationRepo


loanApplicationModule = LoanApplicationModule(repo=loanApplicationRepo)
