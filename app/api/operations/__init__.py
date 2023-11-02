from app.api.operations.delete_model import delete_models_router
from app.api.operations.get_health import health_router
from app.api.operations.create_model import post_models_router

__all__ = [
    'delete_models_router',
    'health_router',
    'post_models_router'
]
