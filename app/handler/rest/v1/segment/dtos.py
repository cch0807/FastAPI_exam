from datetime import datetime
from pydoc import describe
from typing import Optional, List, json

from app.handler.rest.v1._base import BaseDTO
from app.common.enum.dataset import DatasetStatus

class SegmentInputDTO(BaseDTO):
  name: Optional[str]
  description: Optional[str]
  # api_idx: int
  # dataset_idx: int
  status: str

class ParameterInputDTO(BaseDTO):
  name: str
  description: Optional[str]
  type: str
  formula: dict

class SegmentCreateDTO(BaseDTO):
  name: str
  description: Optional[str]
  type: str
  prameters: List[ParameterInputDTO]

class ParameterResponseDTO(BaseDTO):
  idx: int
  name: str
  type: str
  formula: dict

class SegmentResponseDTO(BaseDTO):
  idx: int
  name: str
  # api_name: str
  # dataset_name: str
  parameter: List[ParameterResponseDTO]
  region_count: int
  # creater: str
  # checker: str
  created_date: datetime
  modified_date: datetime
  # Checked_date: datetime
  status: str

class DatasetFieldsReponseDTO(BaseDTO):
    idx: int
    name: str
    description: str

class DatasetResponeDTO(BaseDTO):
    idx: int
    name: str
    description: Optional[str]
    fields: List[DatasetFieldsReponseDTO]

