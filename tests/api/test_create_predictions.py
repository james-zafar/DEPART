import unittest

from fastapi.testclient import TestClient

from app.main import app


class TestCreateModel(unittest.TestCase):
    data = {
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

    def test_can_get_prediction(self) -> None:
        resp = self.client.post('/v1/predictions', json=self.data)
        self.assertEqual(resp.status_code, 200)
        resp_json = resp.json()
        # There should only be 1 key in the response
        self.assertEqual(len(resp_json), 1)
        # Which should be `predictions`
        self.assertCountEqual(['predictions'], resp_json.keys())
        # Predictions should be a list
        self.assertIsInstance(resp_json['predictions'], list)
        # There should be the same number of predictions as rows
        self.assertEqual(len(self.data['flights']), len(resp_json['predictions']))

    def test_can_get_multiple_predictions(self) -> None:
        extra_flight = {
            'opera': 'LATAM',
            'tipovuelo': 'I',
            'mes': 3,
            'Fecha-O': '2017-03-05 18:30:00',
            'Fecha-I': '2017-03-05 23:36:00'
        }
        data = self.data.copy()
        data['flights'].append(extra_flight)
        resp = self.client.post('/v1/predictions', json=data)
        self.assertEqual(resp.status_code, 200)
        resp_json = resp.json()
        # There should only be 1 key in the response
        self.assertEqual(len(resp_json), 1)
        # Which should be `predictions`
        self.assertCountEqual(['predictions'], resp_json.keys())
        # Predictions should be a list
        self.assertIsInstance(resp_json['predictions'], list)
        # There should be the same number of predictions as rows
        self.assertEqual(len(data['flights']), len(resp_json['predictions']))

    def test_can_get_predictions_with_extra_columns(self) -> None:
        data = {
            'flights': [
                {
                    'Fecha-I': '2017-01-29 06:25:00',
                    'Vlo-I': 176,
                    'Ori-I': 'SCEL',
                    'Des-I': 'SKBO',
                    'Emp-I': 'AVA',
                    'Fecha-O': '2017-01-29 06:31:00',
                    'Vlo-O,': 176,
                    'Ori-O': 'SCEL',
                    'Des-O': 'SKBO',
                    'Emp-O': 'AVA',
                    'DIA': 29,
                    'MES': 1,
                    'AÑO': 2017,
                    'DIANOM': 'Domingo',
                    'TIPOVUELO': 'I',
                    'OPERA': 'Avianca',
                    'SIGLAORI': 'Santiago',
                    'SIGLADES': 'Bogota'
                }
            ]
        }
        resp = self.client.post('/v1/predictions', json=data)
        self.assertEqual(resp.status_code, 200)
        resp_json = resp.json()
        # There should only be 1 key in the response
        self.assertEqual(len(resp_json), 1)
        # Which should be `predictions`
        self.assertCountEqual(['predictions'], resp_json.keys())
        # Predictions should be a list
        self.assertIsInstance(resp_json['predictions'], list)
        # There should be the same number of predictions as rows
        self.assertEqual(1, len(resp_json['predictions']))

    def test_predict_fails_with_missing_required_column(self) -> None:
        # Predict should fail with missing required column `opera`
        data = self.data.copy()
        del data['flights'][0]['opera']
        resp = self.client.post('/v1/predictions', json=data)
        self.assertEqual(resp.status_code, 422)

        # Predict should fail with missing required column `tipovuelo`
        data = self.data.copy()
        del data['flights'][0]['tipovuelo']
        resp = self.client.post('/v1/predictions', json=data)
        self.assertEqual(resp.status_code, 422)

        # Predict should fail with missing required column `mes`
        data = self.data.copy()
        del data['flights'][0]['mes']
        resp = self.client.post('/v1/predictions', json=data)
        self.assertEqual(resp.status_code, 422)

        # Predict should fail with missing required column `Fecha-O`
        data = self.data.copy()
        del data['flights'][0]['Fecha-O']
        resp = self.client.post('/v1/predictions', json=data)
        self.assertEqual(resp.status_code, 422)

        # Predict should fail with missing required column `Fecha-I`
        data = self.data.copy()
        del data['flights'][0]['Fecha-I']
        resp = self.client.post('/v1/predictions', json=data)
        self.assertEqual(resp.status_code, 422)

    def test_predict_fails_with_missing_field(self) -> None:
        # Predict should fail if the required field `flights` is missing
        resp = self.client.post('/v1/predictions', json={'flight': 'value'})
        self.assertEqual(resp.status_code, 422)

    def test_predict_fails_with_no_flights(self) -> None:
        # Predict should fail if no flights are specified in the `flights` field
        data = self.data.copy()
        data['flights'] = []
        resp = self.client.post('/v1/predictions', json=data)
        self.assertEqual(resp.status_code, 422)


if __name__ == '__main__':
    unittest.main()
