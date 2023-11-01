import pickle
from datetime import datetime
from typing import Tuple, Union, List

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression


def get_min_diff(data: pd.DataFrame) -> float:
    fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
    fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
    min_diff = ((fecha_o - fecha_i).total_seconds()) / 60
    return min_diff


class DelayModel:
    def __init__(self) -> None:
        self._model = None  # type: LogisticRegression

    @classmethod
    def load(cls, file_name: str) -> 'DelayModel':
        with open(file_name, 'rb') as f:
            model = pickle.load(f)
        instance = cls()
        if not isinstance(model, LogisticRegression):
            raise AttributeError(f'The file {file_name!r} does not contain a valid model. '
                                 f'Expected type {type(LogisticRegression)!r} but got {type(model)!r} ')
        instance._model = model

        return instance

    def preprocess(self, data: pd.DataFrame, target_column: str = None) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        data['min_diff'] = data.apply(get_min_diff, axis=1)

        threshold_in_minutes = 15
        data['delay'] = np.where(data['min_diff'] > threshold_in_minutes, 1, 0)
        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix='OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),
            pd.get_dummies(data['MES'], prefix='MES')],
            axis=1
        )
        # For test data, see if there are any missing features
        missing_columns = set(self.features) - set(features.columns)
        # And if so, add them
        for column in missing_columns:
            features[column] = 0

        top_features = features[self.features]
        if target_column:
            return top_features, pd.DataFrame(data[target_column])

        return top_features

    def fit(self, features: pd.DataFrame, target: pd.DataFrame) -> 'DelayModel':
        n_y0 = len(features[features == 0])
        n_y1 = len(features[features == 1])

        self._model = LogisticRegression(class_weight={1: n_y0 / len(features), 0: n_y1 / len(features)})
        self._model.fit(features, target)

        return self

    def predict(self, features: pd.DataFrame) -> List[int]:
        return self._model.predict(features).tolist()

    def save(self, file_name: str) -> None:
        with open(file_name, 'wb') as f:
            pickle.dump(self._model, f)

    @property
    def features(self) -> list[str]:
        return [
            "OPERA_Latin American Wings",
            "MES_7",
            "MES_10",
            "OPERA_Grupo LATAM",
            "MES_12",
            "TIPOVUELO_I",
            "MES_4",
            "MES_11",
            "OPERA_Sky Airline",
            "OPERA_Copa Air"
        ]
