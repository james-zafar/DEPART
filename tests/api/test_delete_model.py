import random
import unittest
import uuid

from fastapi.testclient import TestClient

from app.api.errors import ModelNotFoundError
from app.main import app


class TestCreateModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)
        random.seed(15)

    def setUp(self) -> None:
        resp = self.client.post('/v1/models', json={'data_source': './data/data.csv'})
        assert resp.status_code == 201
        self.model_id = resp.json()['id']

    def tearDown(self) -> None:
        self.client.app.state.model_store.clear()

    def test_delete_valid_model(self) -> None:
        # Check the model exists in the model store
        self.assertIn(self.model_id, self.client.app.state.model_store)
        resp = self.client.delete(f'/v1/models/{self.model_id}')
        self.assertEqual(resp.status_code, 204)
        # There should be no response body
        self.assertIsNone(resp.json())
        # Check the model is no longer in the model store
        self.assertNotIn(self.model_id, self.client.app.state.model_store)

    def test_delete_fails_with_nonexistent_model(self) -> None:
        fake_model = str(uuid.uuid4())
        # Check the model is not in the model store
        self.assertNotIn(fake_model, self.client.app.state.model_store)
        resp = self.client.delete(f'/v1/models/{fake_model}')
        self.assertEqual(resp.status_code, 404)
        resp_json = resp.json()
        # Response should have one key
        self.assertEqual(len(resp_json), 1)
        self.assertIn('errors', resp_json)
        # `errors` should be a list
        self.assertIsInstance(resp_json['errors'], list)
        # With just one error
        self.assertEqual(len(resp_json['errors']), 1)
        # Which should be a `ModelNotFoundError`
        self.assertEqual(resp_json['errors'][0], ModelNotFoundError().json())

    def test_delete_single_model(self) -> None:
        # Add multiple models to the model store
        create_model_resp = self.client.post('/v1/models', json={'data_source': './data/data.csv'})
        self.assertEqual(create_model_resp.status_code, 201)
        # Check there are two models in the model store
        self.assertEqual(len(self.client.app.state.model_store), 2)
        # And that one of the models is the one we created earlier
        self.assertIn(self.model_id, self.client.app.state.model_store)
        resp = self.client.delete(f'/v1/models/{self.model_id}')
        self.assertEqual(resp.status_code, 204)
        # The model should no longer by in the model store
        self.assertNotIn(self.model_id, self.client.app.state.model_store)
        # The other model should still be there
        self.assertEqual(len(self.client.app.state.model_store), 1)
        self.assertIn(create_model_resp.json()['id'], self.client.app.state.model_store)


if __name__ == '__main__':
    unittest.main()
