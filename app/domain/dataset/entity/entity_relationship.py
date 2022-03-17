from sqlalchemy.orm import relationship

from app.domain.dataset.entity.dataset import Dataset
from app.domain.dataset.entity.dataset_field import DatasetField


def make_relationship():
    Dataset.fields = relationship("DatasetField", uselist=True)
    DatasetField.dataset = relationship("Dataset")
