import unittest
import uuid

from fastapi.testclient import TestClient

from app.api.errors import UnsupportedModelTypeError
from app.api.resources import Model
from app.api.schemas import Status
from app.main import app
from app.model import DelayModel


class TestUploadModel(unittest.TestCase):
    _TEST_MODEL = './models/modelv1.0.pkl'

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def tearDown(self) -> None:
        self.client.app.state.model_store.clear()

    def test_can_upload_model(self) -> None:
        # Check the model store is empty
        self.assertEqual(len(self.client.app.state.model_store), 0)
        # Upload an existing model
        resp = self.client.post('/v1/models/upload', json={'model_location': self._TEST_MODEL})
        self.assertEqual(resp.status_code, 201)
        resp_json = resp.json()
        # The response should have only two fields - `id` and `status`
        self.assertCountEqual(['id', 'status'], resp_json)
        # Check the model ID is a UUID
        try:
            _ = uuid.UUID(resp_json['id'])
        except ValueError:
            self.fail('The model id must be a valid UUID')
        # And that the model is in the `ModelStore`
        self.assertIn(resp_json['id'], self.client.app.state.model_store)
        # The status of the model should be `completed`
        self.assertEqual(resp_json['status'], Status.COMPLETED.value)
        # Check the model is stored as a `Model` resource
        self.assertIsInstance(self.client.app.state.model_store[resp_json['id']], Model)
        # And that the model itself is a `DelayModel`
        self.assertIsInstance(self.client.app.state.model_store[resp_json['id']].model, DelayModel)
        # There should be a location header
        self.assertIn('location', resp.headers)
        # And the value should be the location of the model
        expected_location = f'{self.client.base_url}/v1/models/{resp_json["id"]}'
        self.assertEqual(expected_location, resp.headers['location'])

    def test_upload_with_invalid_file_fails(self) -> None:
        # Check the model store is empty
        self.assertEqual(len(self.client.app.state.model_store), 0)
        resp = self.client.post('/v1/models/upload', json={'model_location': './invalid/file/path.pkl'})
        # The response should be 422
        self.assertEqual(resp.status_code, 422)
        # The model store should still be empty
        self.assertEqual(len(self.client.app.state.model_store), 0)

    def test_upload_fails_with_wrong_model(self) -> None:
        # Uploading a file that does not have a `DelayModel` should fail
        self.assertEqual(len(self.client.app.state.model_store), 0)
        resp = self.client.post('/v1/models/upload', json={'model_location': './tests/data/bad_model.pkl'})
        self.assertEqual(resp.status_code, 400)
        resp_json = resp.json()
        # The response should have one field - `errors`
        self.assertCountEqual(['errors'], resp_json)
        # There should be only 1 error
        self.assertEqual(len(resp_json['errors']), 1)
        # The error should be a `UnsupportedModelTypeError`
        self.assertEqual(resp_json['errors'][0], UnsupportedModelTypeError().json())
        # The model store should still be empty
        self.assertEqual(len(self.client.app.state.model_store), 0)

    def test_upload_fails_with_non_binary_file(self) -> None:
        resp = self.client.post('/v1/models/upload', json={'model_location': './data/data.csv'})
        self.assertEqual(resp.status_code, 400)
        resp_json = resp.json()
        # The response should have one field - `errors`
        self.assertCountEqual(['errors'], resp_json)
        # There should be only 1 error
        self.assertEqual(len(resp_json['errors']), 1)
        # The error should be a `UnsupportedModelTypeError`
        self.assertEqual(resp_json['errors'][0], UnsupportedModelTypeError().json())
        # The model store should still be empty
        self.assertEqual(len(self.client.app.state.model_store), 0)


if __name__ == '__main__':
    unittest.main()
