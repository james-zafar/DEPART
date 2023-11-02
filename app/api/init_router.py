from fastapi import APIRouter

from app.api.operations import (delete_models_router, deploy_models_router, get_models_router,
                                health_router, post_models_router, post_models_upload_router, predictions_router)


def init_router(url_prefix: str = None) -> APIRouter:
    router = APIRouter()
    if url_prefix:
        router.prefix = url_prefix
    router.include_router(delete_models_router)
    router.include_router(deploy_models_router)
    router.include_router(get_models_router)
    router.include_router(health_router)
    router.include_router(post_models_router)
    router.include_router(post_models_upload_router)
    router.include_router(predictions_router)

    return router
