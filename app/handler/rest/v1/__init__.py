from fastapi import APIRouter

from app.handler.rest.v1.api.endpoint import router as api_router
from app.handler.rest.v1.dataset.endpoint import router as dataset_router
from app.handler.rest.v1.healthcheck.endpoint import router as healthcheck_router
from app.handler.rest.v1.segment.endpoint import router as segment_router

# from app.handler.rest.v1.scorecard.endpoint import router as scorecard_router

router = APIRouter(prefix="/v1")
router.include_router(segment_router)
router.include_router(healthcheck_router)
router.include_router(dataset_router)
router.include_router(api_router)
# router.include_router(scorecard_router)