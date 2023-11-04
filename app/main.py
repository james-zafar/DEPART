from typing import Final

import uvicorn
from fastapi import FastAPI

from app.api.init_router import init_router
from app.api.resources import Model
from app.model import DelayModel
from app.store import ModelStore

V1_URL_PREFIX: Final[str] = '/v1'


def _load_model() -> Model:
    delay_model = DelayModel.load('./models/modelv1.0.pkl')
    model = Model.new_model()
    model.model = delay_model
    return model


app = FastAPI(
    title='Delay prediction Service',
    version='1.0.0',
    docs_url=None,
    redoc_url=None
)

app.include_router(init_router(V1_URL_PREFIX))
app.state.model = _load_model()
app.state.model_store = ModelStore(default_model=app.state.model)

if __name__ == '__main__':
    # if os.getenv('ENABLE_HTTPS') != 'False':
    #     config['ssl_keyfile'] = os.getenv('TLS_KEY_PATH', '/mnt/certs/tls.key')
    #     config['ssl_certfile'] = os.getenv('TLS_CERT_PATH', '/mnt/certs/tls.crt')

    uvicorn.run(app)
