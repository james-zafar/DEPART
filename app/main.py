import os

import uvicorn
from fastapi import FastAPI

from app.api.init_router import init_router
from app.store import ModelStore

V1_URL_PREFIX: str = '/v1'

app = FastAPI(
    title='Delay prediction Service',
    version='1.0.0',
    docs_url=None,
    redoc_url=None
)

app.include_router(init_router(V1_URL_PREFIX))
app.state.model_store = ModelStore()

if __name__ == '__main__':
    port = int(os.getenv('PORT', '8000'))
    config = {
        'app': app,
        'host': '0.0.0.0',
        'port': port,
        'log_level': 'info',
        'workers': 1,
    }

    if os.getenv('ENABLE_HTTPS', 'True') != 'False':
        config['ssl_keyfile'] = os.getenv('TLS_KEY_PATH', '/mnt/certs/tls.key')
        config['ssl_certfile'] = os.getenv('TLS_CERT_PATH', '/mnt/certs/tls.crt')

    uvicorn.run(**config, log_config=None)
