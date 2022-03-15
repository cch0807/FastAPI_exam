from typing import Optional, List

from app.handler.rest.v1._base import BaseDTO


class APIInputDTO(BaseDTO):
    name: str
    description: Optional[str]


class APIFieldInputDTO(BaseDTO):
    name: str
    description: Optional[str]
    type: str


class APICreateDTO(BaseDTO):
    name: str
    description: Optional[str]
    type: str
    fields: List[APIFieldInputDTO]


class APIFieldsReponseDTO(BaseDTO):
    idx: int
    name: str
    description: str


class APIResponeDTO(BaseDTO):
    idx: int
    name: str
    description: Optional[str]
    fields: List[APIFieldsReponseDTO]
