from logging import getLogger

from app.handler.rest.v1._base import BaseService
from app.handler.rest.v1.users.dto import V1UsersMeGetResponseDto
from app.core.const.service_constant import ServiceConstant
from app.common.enum.user_role import UserRole
from app.common.enum.deploy_env import DeployEnv

class V1UsersService(BaseService):
    logger = getLogger("app.V1UsersService")

    async def me_get(
        self,
    ) -> V1UsersMeGetResponseDto:

        self.logger.debug("V1UsersService.me_get")

        response_dto = V1UsersMeGetResponseDto()

        if ServiceConstant.DEPLOY_ENV == DeployEnv.LOCAL:
            response_dto.detail = "Success"
            response_dto.email = "ks.seo@aizen.co"
            response_dto.roles = [UserRole.CHECKER, UserRole.MAKER]

        return response_dto
        