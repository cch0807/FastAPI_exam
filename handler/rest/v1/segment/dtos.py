from datetime import datetime
from pydoc import describe
from typing import Optional, List, json

from app.handler.rest.v1._base import BaseDTO
from app.common.enum.dataset import DatasetStatus

class SegmentInputDTO(BaseDTO):
  name: str
  description: Optional[str]
  # api_idx: int
  # dataset_idx: int
  status: str

class ParameterInputDTO(BaseDTO):
  name: str
  description: Optional[str]
  

class ParameterResponseDTO(BaseDTO):
  idx: int
  name: str
  type: str
  formula: json # json 형식 사용법 알아보기
  

class SegmentResponseDTO(BaseDTO):
  idx: int
  name: str
  # api_name: str
  # dataset_name: str
  parameter: List[ParameterResponseDTO]
  region_count: int
  # creater: str
  # checker: str
  created_at: datetime
  Modified_at: datetime
  # Checked_at: datetime
  status: str


