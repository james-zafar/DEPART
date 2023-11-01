from fastapi import APIRouter

from app.api.operations import health_router


def init_router(url_prefix: str = None) -> APIRouter:
    router = APIRouter()
    if url_prefix:
        router.prefix = url_prefix
    router.include_router(health_router)
    # router.include_router(probe_router)

    return router
