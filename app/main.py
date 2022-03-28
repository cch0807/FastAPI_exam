from fastapi.middleware.cors import CORSMiddleware

from app.core.asgi import app # noqa: F401
from app.core.log import configure_logging
from app.handler.rest import router as router
from app.infra.middleware.sqlalchemy_session import set_sesion_scope

app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://localhost:3000",
        "http://localhost:3000",
        "https://stg-banko-www.aizendev.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    alow_headers=["*"],
    expose_headers=["Authorization"],
)

app.middleware("http")(set_sesion_scope)