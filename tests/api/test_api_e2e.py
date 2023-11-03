import os
import random
import string
import unittest
import uuid

from fastapi.testclient import TestClient
from sklearn.linear_model import LogisticRegression

from app.api.errors import ModelNotFoundError
from app.api.schemas import Status
from app.main import app
from app.model import DelayModel


class TestCreateModel(unittest.TestCase):
    _TRAIN_DATA = './data/data.csv'
    _PREDICT_DATA = {
        'flights': [
            {
                'opera': 'Aerolineas Argentinas',
                'tipovuelo': 'N',
                'mes': 3,
                'Fecha-O': '2017-01-01 23:30:00',
                'Fecha-I': '2017-01-01 23:32:00'
            }
        ]
    }

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)
        random.seed(15)

    def test_e2e_model_success(self) -> None:
        # First check that a model has been loaded and is running
        self.assertIsNotNone(self.client.app.state.model)
        # And that the model is a `DelayModel`
        self.assertIsInstance(self.client.app.state.model, DelayModel)
        # Now let's create a new model
        create_model_resp = self.client.post('/v1/models', json={'data_source': self._TRAIN_DATA})
        self.assertEqual(create_model_resp.status_code, 201)
        create_model_resp_json = create_model_resp.json()
        model_id = create_model_resp_json['id']
        self.assertCountEqual(['id', 'status'], create_model_resp_json.keys())
        # Check the response body
        try:
            _ = uuid.UUID(model_id)
        except ValueError:
            self.fail('The model ID must be a valid UUID')
        self.assertEqual(create_model_resp_json['status'], Status.COMPLETED.value)
        # A location header should be present
        self.assertIn('location', create_model_resp.headers)
        self.assertEqual(f'{self.client.base_url}/v1/models/{model_id}', create_model_resp.headers['location'])

        # Check the model is in the `ModelStore`
        self.assertIn(model_id, self.client.app.state.model_store)
        # And that the model has been trained
        trained_model = self.client.app.state.model_store[model_id]
        self.assertIsInstance(trained_model.model, DelayModel)
        self.assertIsInstance(trained_model.model._model, LogisticRegression)
        # The model should not have any errors
        self.assertEqual(len(trained_model.errors), 0)

        # Now retrieve the trained model through GET /models/{model_id}
        get_model_response = self.client.get(f'/v1/models/{str(model_id)}')
        self.assertEqual(get_model_response.status_code, 200)
        get_model_response_json = get_model_response.json()
        # The response should contain only the ID and status of the model
        self.assertCountEqual(['id', 'status'], get_model_response_json)
        self.assertEqual(model_id, get_model_response_json['id'])
        self.assertEqual(get_model_response_json['status'], Status.COMPLETED.value)

        # Now let's try deploying the model
        # Set an API key first
        api_key = f'admin={"".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))}'
        os.environ['API_KEY'] = api_key
        deploy_response = self.client.put(f'/v1/models/deploy?model-id={model_id}', headers={'X-api-key': api_key})
        self.assertEqual(deploy_response.status_code, 200)
        deploy_response_json = deploy_response.json()
        # The response should contain only 2 fields
        self.assertCountEqual(['id', 'deployed'], deploy_response_json.keys())
        # The ID should be the same as the input ID
        self.assertEqual(model_id, deploy_response_json['id'])
        # FIXME: We should ideally track the ID of he model currently in prod

        # Next let's generate some predictions
        predict_response = self.client.post('/v1/predictions', json=self._PREDICT_DATA)
        self.assertEqual(predict_response.status_code, 200)
        # The response should contain only one key
        predict_response_json = predict_response.json()
        self.assertEqual(len(predict_response_json.keys()), 1)
        self.assertEqual(['predictions'], list(predict_response_json))
        # Predictions should be a list
        self.assertIsInstance(predict_response_json['predictions'], list)
        # With the same number of elements as inputs
        self.assertEqual(len(self._PREDICT_DATA), len(predict_response_json['predictions']))

        # Finally let's delete the model
        delete_response = self.client.delete(f'/v1/models/{model_id}')
        self.assertEqual(delete_response.status_code, 204)
        # The response body must be empty
        self.assertIsNone(delete_response.json())
        # The model should have been removed from the model_store
        self.assertNotIn(model_id, self.client.app.state.model_store)
        # There must still be a model in production
        self.assertIsNotNone(self.client.app.state.model)

        # And check that the model can no longer be retrieved
        fail_get_model_response = self.client.get(f'/v1/models/{str(model_id)}')
        self.assertEqual(fail_get_model_response.status_code, 404)
        fail_get_model_resp_json = fail_get_model_response.json()
        # The error returned should be a `ModelNotFoundError`
        self.assertIn('errors', fail_get_model_resp_json)
        self.assertEqual(len(fail_get_model_resp_json), 1)
        self.assertEqual(fail_get_model_resp_json['errors'][0], ModelNotFoundError().json())

        # Tear down
        del os.environ['API_KEY']


if __name__ == '__main__':
    unittest.main()
