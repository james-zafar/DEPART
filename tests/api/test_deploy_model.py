import os
import random
import string
import unittest
import uuid

from fastapi.testclient import TestClient

from app.api.errors import UnauthorizedError, ForbiddenError, ModelNotFoundError, ModelNotReadyError
from app.api.resources import Model
from app.api.schemas import Status
from app.main import app


class TestCreateModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)
        api_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        os.environ['API_KEY'] = f'admin={api_key}'
        cls.api_key = api_key

    def setUp(self) -> None:
        model = Model.new_model()
        self.client.app.state.model_store.add_model(model)
        self.client.app.state.model_store.update_status(str(model.id), Status.COMPLETED)
        self.model_id = str(model.id)

    def tearDown(self) -> None:
        self.model_id = None
        self.client.app.state.model_store.clear()
        self.client.app.state.model = None

    @classmethod
    def tearDownClass(cls) -> None:
        del os.environ['API_KEY']

    def test_deploy_existing_model(self) -> None:
        resp = self.client.put(f'/v1/models/deploy?model-id={self.model_id}',
                               headers={'X-api-key': f'admin={self.api_key}'})
        self.assertEqual(resp.status_code, 200)
        resp_json = resp.json()
        # The response should have 2 keys - the model ID and the status
        self.assertCountEqual(['model_id', 'deployed'], resp_json.keys())
        # Check the model ID matches the ID specified
        self.assertEqual(resp_json['model_id'], self.model_id)
        # Check deployed is "ok"
        self.assertEqual(resp_json['deployed'], 'OK')

    def test_deploy_fails_with_unauthorized_user(self) -> None:
        resp = self.client.put(f'/v1/models/deploy?model-id={self.model_id}',
                               headers={'X-api-key': f'user={self.api_key}'})
        self.assertEqual(resp.status_code, 401)
        resp_json = resp.json()
        # The response should only contain errors
        self.assertCountEqual(['errors'], resp_json.keys())
        # Check there is only a single error
        self.assertEqual(len(resp_json['errors']), 1)
        # And that it's the error we expect
        self.assertEqual(resp_json['errors'][0], UnauthorizedError().json())

    def test_deploy_fails_with_invalid_api_key(self) -> None:
        resp = self.client.put(f'/v1/models/deploy?model-id={self.model_id}', headers={'X-api-key': 'admin=APIKEY'})
        self.assertEqual(resp.status_code, 403)
        resp_json = resp.json()
        # The response should only contain errors
        self.assertCountEqual(['errors'], resp_json.keys())
        # Check there is only a single error
        self.assertEqual(len(resp_json['errors']), 1)
        # And that it's the error we expect
        self.assertEqual(resp_json['errors'][0], ForbiddenError().json())

    def test_deploy_fails_with_invalid_model(self) -> None:
        fake_model = str(uuid.uuid4())
        resp = self.client.put(f'/v1/models/deploy?model-id={fake_model}',
                               headers={'X-api-key': f'admin={self.api_key}'})
        self.assertEqual(resp.status_code, 404)
        resp_json = resp.json()
        # The response should only contain errors
        self.assertCountEqual(['errors'], resp_json.keys())
        # Check there is only a single error
        self.assertEqual(len(resp_json['errors']), 1)
        # And that it's the error we expect
        self.assertEqual(resp_json['errors'][0], ModelNotFoundError().json())

    def test_deploy_fails_when_model_not_ready(self) -> None:
        # Create a new model
        model = Model.new_model()
        self.client.app.state.model_store.add_model(model)
        model_id = str(model.id)
        resp = self.client.put(f'/v1/models/deploy?model-id={model_id}', headers={'X-api-key': f'admin={self.api_key}'})
        self.assertEqual(resp.status_code, 400)
        resp_json = resp.json()
        # The response should only contain errors
        self.assertCountEqual(['errors'], resp_json.keys())
        # Check there is only a single error
        self.assertEqual(len(resp_json['errors']), 1)
        # And that it's the error we expect
        self.assertEqual(resp_json['errors'][0], ModelNotReadyError().json())

        # Deploy should also fail for running models
        self.client.app.state.model_store.update_status(model_id, Status.RUNNING)
        resp = self.client.put(f'/v1/models/deploy?model-id={model_id}', headers={'X-api-key': f'admin={self.api_key}'})
        self.assertEqual(resp.status_code, 400)
        resp_json = resp.json()
        # The response should only contain errors
        self.assertCountEqual(['errors'], resp_json.keys())
        # Check there is only a single error
        self.assertEqual(len(resp_json['errors']), 1)
        # And that it's the error we expect
        self.assertEqual(resp_json['errors'][0], ModelNotReadyError().json())

        # Deploy should also fail for failed models
        self.client.app.state.model_store.update_status(model_id, Status.FAILED)
        resp = self.client.put(f'/v1/models/deploy?model-id={model_id}', headers={'X-api-key': f'admin={self.api_key}'})
        self.assertEqual(resp.status_code, 400)
        resp_json = resp.json()
        # The response should only contain errors
        self.assertCountEqual(['errors'], resp_json.keys())
        # Check there is only a single error
        self.assertEqual(len(resp_json['errors']), 1)
        # And that it's the error we expect
        self.assertEqual(resp_json['errors'][0], ModelNotReadyError().json())


if __name__ == '__main__':
    unittest.main()
