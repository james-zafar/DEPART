import unittest
import uuid

from fastapi.testclient import TestClient
from sklearn.linear_model import LogisticRegression

from app.api.errors import DataFormatError
from app.api.resources import Model
from app.main import app
from app.model import DelayModel


class TestCreateModel(unittest.TestCase):
    _DATA_PATH = './data/data.csv'

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_create_model_success(self) -> None:
        # Create a model with a valid data path
        resp = self.client.post('/v1/models', json={'data_source': self._DATA_PATH})
        self.assertEqual(resp.status_code, 201)
        resp_json = resp.json()
        # The response should have 2 keys - the model ID and the status
        self.assertCountEqual(['id', 'status', 'deployed'], resp_json.keys())
        # Check the ID is a valid UUID
        try:
            _ = uuid.UUID(resp_json['id'])
        except ValueError:
            self.fail('The model ID is not a valid UUID')
        # The status should be completed as we do not support asynchronous training
        self.assertEqual(resp_json['status'], 'completed')
        # The response should contain a location header
        self.assertIn('location', resp.headers)
        expected_location = f'{self.client.base_url}/v1/models/{resp_json["id"]}'
        self.assertEqual(resp.headers['location'], expected_location)
        # By default, the model should not be deployed
        self.assertFalse(resp_json['deployed'])

    def test_create_model_saves_to_model_store(self) -> None:
        # Create a model with a valid data path
        resp = self.client.post('/v1/models', json={'data_source': self._DATA_PATH})
        self.assertEqual(resp.status_code, 201)
        resp_json = resp.json()
        # Check the ID is a valid UUID
        try:
            _ = uuid.UUID(resp_json['id'])
        except ValueError:
            self.fail('The model ID is not a valid UUID')
        # Check the model has been added to the model store
        self.assertIn(resp_json['id'], self.client.app.state.model_store)
        model = self.client.app.state.model_store[resp_json['id']]
        # The model should be a Model resource
        self.assertIsInstance(model, Model)
        # The model resource should contain a DelayModel
        self.assertIsInstance(model.model, DelayModel)
        # And the DelayModel should be a LogisticRegression model
        self.assertIsInstance(model.model._model, LogisticRegression)  # pylint: disable=protected-access

    def test_create_model_with_no_data_source(self) -> None:
        # Creating a model with no `data_source` in the req body should result in a 422
        resp = self.client.post('/v1/models', json={'data': 'some_value'})
        self.assertEqual(resp.status_code, 422)

    def test_create_model_with_unreadable_data_source(self) -> None:
        # Creating a model with a file that does not exist should results in a 422
        # FIXME: This should return a 400, but a custom hook for PyDantic errors is needed for this
        resp = self.client.post('/v1/models', json={'data_source': './a/fake/file.csv'})
        self.assertEqual(resp.status_code, 422)

    def test_create_model_with_missing_columns(self) -> None:
        # Attempting to train a model without the required columns should succeed but the model status should be `failed`
        resp = self.client.post('/v1/models', json={'data_source': './data/bad_data.csv'})
        self.assertEqual(resp.status_code, 201)
        resp_json = resp.json()
        # There should be 3 keys in the response
        self.assertCountEqual(['id', 'status', 'errors', 'deployed'], resp_json.keys())
        # Check the model ID is valid
        try:
            _ = uuid.UUID(resp_json['id'])
        except ValueError:
            self.fail('The model ID is not a valid UUID')
        # Errors should be a list with 1 error
        self.assertIsInstance(resp_json['errors'], list)
        self.assertEqual(len(resp_json['errors']), 1)
        # The error should be a `DataFormatError`
        self.assertEqual(resp_json['errors'][0], DataFormatError().json())
        # The status of the model is failed
        self.assertEqual(resp_json['status'], 'failed')
        # The model should not be deployed
        self.assertFalse(resp_json['deployed'])


if __name__ == '__main__':
    unittest.main()
