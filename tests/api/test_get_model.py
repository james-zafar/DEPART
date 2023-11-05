import unittest

from fastapi.testclient import TestClient

from app.api.errors import DataFormatError
from app.api.resources import Model
from app.api.schemas import Status
from app.main import app


class TestGetModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def setUp(self) -> None:
        resp = self.client.post('/v1/models', json={'data_source': './data/data.csv'})
        assert resp.status_code == 201
        self.model_id = resp.json()['id']

    def tearDown(self) -> None:
        self.client.app.state.model_store.clear()

    def test_can_retrieve_completed_model(self) -> None:
        resp = self.client.get(f'/v1/models/{self.model_id}')
        self.assertEqual(resp.status_code, 200)
        resp_json = resp.json()
        # As the model succeeded, only the id and status should be present
        self.assertCountEqual(['id', 'status'], resp_json)
        # The ID should match the ID in the request
        self.assertEqual(resp_json['id'], self.model_id)
        # And the status should be `completed`
        self.assertEqual(resp_json['status'], Status.COMPLETED.value)

    def test_can_retrieve_pending_model(self) -> None:
        # Create a new model that is `pending`
        pending_model = Model.new_model()
        self.client.app.state.model_store.add_model(pending_model)
        resp = self.client.get(f'/v1/models/{str(pending_model.id)}')
        self.assertEqual(resp.status_code, 200)
        resp_json = resp.json()
        # The ID should match the ID in the request
        self.assertEqual(resp_json['id'], str(pending_model.id))
        # And the status should be `pending`
        self.assertEqual(resp_json['status'], Status.PENDING.value)

    def test_can_retrieve_failed_model(self) -> None:
        # Create a new model that failed
        create_resp = self.client.post('/v1/models', json={'data_source': './data/bad_data.csv'})
        self.assertEqual(create_resp.status_code, 201)
        self.assertEqual(create_resp.json()['status'], Status.FAILED.value)

        model_id = create_resp.json()['id']
        resp = self.client.get(f'/v1/models/{model_id}')
        self.assertEqual(resp.status_code, 200)
        resp_json = resp.json()
        # The response should have an `errors` field as well as the ID and status
        self.assertCountEqual(['id', 'status', 'errors'], resp_json)
        # Check the model ID is correct
        self.assertEqual(resp_json['id'], model_id)
        # And the status should be `failed`
        self.assertEqual(resp_json['status'], Status.FAILED.value)
        # Check the errors field is a list with exactly 1 error
        self.assertIsInstance(resp_json['errors'], list)
        self.assertEqual(len(resp_json['errors']), 1)
        # A `DataFormatError` should be present in the errors list
        self.assertEqual(DataFormatError().json(), resp_json['errors'][0])

    def test_can_retrieve_running_model(self) -> None:
        running_model = Model.new_model()
        self.client.app.state.model_store.add_model(running_model)
        self.client.app.state.model_store.update_status(str(running_model.id), Status.RUNNING)
        resp = self.client.get(f'/v1/models/{str(running_model.id)}')
        self.assertEqual(resp.status_code, 200)
        resp_json = resp.json()
        # The ID should match the ID in the request
        self.assertEqual(resp_json['id'], str(running_model.id))
        # And the status should be `running`
        self.assertEqual(resp_json['status'], Status.RUNNING.value)

    def test_can_export_completed_model(self) -> None:
        ...


if __name__ == '__main__':
    unittest.main()
