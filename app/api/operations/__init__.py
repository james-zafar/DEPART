from app.api.operations.get_health import health_router
from app.api.operations.create_model import post_models_router

__all__ = [
    'health_router',
    'post_models_router'
]
