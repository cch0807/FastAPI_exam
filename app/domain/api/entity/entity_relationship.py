from sqlalchemy.orm import relationship

from app.domain.api.entity import API, APIField


def make_relationship():
    API.fields = relationship("APIField", uselist=True)
    APIField.api = relationship("API")
