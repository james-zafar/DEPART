import unittest

import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from app.model import DelayModel


class TestModel(unittest.TestCase):
    FEATURES_COLS = [
        'OPERA_Latin American Wings',
        'MES_7',
        'MES_10',
        'OPERA_Grupo LATAM',
        'MES_12',
        'TIPOVUELO_I',
        'MES_4',
        'MES_11',
        'OPERA_Sky Airline',
        'OPERA_Copa Air'
    ]

    TARGET_COL = [
        'delay'
    ]

    def setUp(self) -> None:
        self.model = DelayModel()
        self.data = pd.read_csv(filepath_or_buffer='./data/data.csv')

    def test_model_preprocess_for_training(self) -> None:
        features, target = self.model.preprocess(data=self.data, target_column='delay')

        self.assertIsInstance(features, pd.DataFrame)
        self.assertEqual(features.shape[1], len(self.FEATURES_COLS))
        self.assertEqual(set(features.columns), set(self.FEATURES_COLS))

        self.assertIsInstance(target, pd.DataFrame)
        self.assertEqual(target.shape[1], len(self.TARGET_COL))
        self.assertEqual(set(target.columns), set(self.TARGET_COL))

    def test_model_preprocess_for_serving(self) -> None:
        features = self.model.preprocess(data=self.data)

        self.assertIsInstance(features, pd.DataFrame)
        self.assertEqual(features.shape[1], len(self.FEATURES_COLS))
        self.assertEqual(set(features.columns), set(self.FEATURES_COLS))

    def test_model_fit(self):
        features, target = self.model.preprocess(data=self.data, target_column='delay')

        _, features_validation, _, target_validation = train_test_split(features, target, test_size=0.33, random_state=42)

        self.model.fit(features=features, target=target)

        predicted_target = self.model._model.predict(features_validation)

        report = classification_report(target_validation, predicted_target, output_dict=True)  # type: dict

        self.assertGreater(report['0']['recall'], 0.60)
        self.assertGreater(report['0']['f1-score'], 0.70)
        self.assertLess(report['1']['recall'], 0.60)
        self.assertLess(report['1']['f1-score'], 0.30)

    def test_model_predict(self):
        features, target = self.model.preprocess(data=self.data, target_column='delay')

        self.model.fit(features=features, target=target)
        features = self.model.preprocess(data=self.data)
        predicted_targets = self.model.predict(features=features)

        self.assertIsInstance(predicted_targets, list)
        self.assertEqual(len(predicted_targets), features.shape[0])
        self.assertTrue(all(isinstance(predicted_target, int) for predicted_target in predicted_targets))
