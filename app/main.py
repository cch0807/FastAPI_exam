#로거 초기화
from app.core.config.logging_configurer import configure_logging
# 시스템 상수 초기화
from app.core.config.constant_initializer import constant_initializer
from app.core.const.service_constant import ServiceConstant
from app.core.server.fast_api import app # noqa: F401
#예외 핸들러 등록
from app.core.resolver.exception_resolver import root_exception_resolver
from fastapi.middleware.cors import CORSMiddleware
from app.common.middleware.request_id_middleware import instance as request_id_middleware_instance
from app.common.middleware.sql_session_middlewareimport import instance as sql_session_middleware_instance
from app.common.middleware.auth_middleware import auth_middleware
from app.handler.rest import router

# 위치 변경하는 경우 cors상태일 때 auth_middleware에서 응답 시 response body 누락됨.

app.add_middleware(AuthMiddleware)

if ServiceConstant.CORS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ServiceConstant.CORS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Authorization"],
    )

app.include_router(router)

app.middleware("http")(request_id_middleware_instance.inject_request_id)
app.middleware("http")(sql_session_middleware_instance.inject_sql_session)

@app.on_event("startup")
async def startup():
    # configure_logging()
    pass