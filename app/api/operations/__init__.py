from app.api.operations.delete_model import delete_models_router
from app.api.operations.get_model import get_models_router
from app.api.operations.get_health import health_router
from app.api.operations.create_model import post_models_router
from app.api.operations.post_predictions import predictions_router
from app.api.operations.put_deploy import deploy_models_router

__all__ = [
    'delete_models_router',
    'deploy_models_router',
    'get_models_router',
    'health_router',
    'post_models_router',
    'predictions_router'
]
