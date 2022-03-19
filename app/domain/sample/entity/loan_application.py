from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from typing_extensions import Self

from app.common.enum import ApplicationStatus
from app.domain._base import BaseEntity


class LoanApplication(BaseEntity):
    __tablename__ = "loan_application"
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    comment = Column(String)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED)

    def start_processing(self) -> Self:
        assert self.status == ApplicationStatus.APPLIED
        self.status = ApplicationStatus.PROCESSING
        return self

    def set_pending(self) -> Self:
        assert self.status == ApplicationStatus.PROCESSING
        self.status = ApplicationStatus.PENDING
        return self

    def approve(self) -> Self:
        assert self.status == ApplicationStatus.PROCESSING
        self.status = ApplicationStatus.APPROVED
        return self

    def reject(self) -> Self:
        assert self.status == ApplicationStatus.PROCESSING
        self.status = ApplicationStatus.REJECTED
        return self

    @hybrid_property
    def is_finished(self) -> bool:
        if self.status in {ApplicationStatus.APPROVED, ApplicationStatus.REJECTED}:
            return True
        else:
            return False

    @is_finished.expression
    def is_finished(self):
        return self.status.in_(ApplicationStatus.APPROVED, ApplicationStatus.REJECTED)
