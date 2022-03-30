from app.core.type import BaseBuisnessLoginRunner

from ..entity import Entity
from ..repository import BaseEntityRepo

class BaseModuel(BaseBuisnessLoginRunner):

    __runner_typr__= "module"

class BaseEntityModule(BaseModule, Generic[EntityRepo]):

    repo: EntityRepo

    async def retrieve(self, limit: int | None = None) -> Sequence[Entity]:
        return await self.repo.retrieve(limit=limit)