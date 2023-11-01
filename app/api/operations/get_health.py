from fastapi import APIRouter

health_router = APIRouter(prefix='/health')


@health_router.get('', status_code=204)
def get_health() -> None:
    return None
