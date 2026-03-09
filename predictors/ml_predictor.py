from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.utils.validation import check_consistent_length
from typing import List, Optional
import numpy as np


class MLPredictor:
    def __init__(self):
        self.rfregressor = RandomForestRegressor(n_estimators=100, random_state=45, verbose=1)
        self._feature_length = None

    def train_rf(self, data: List[list]) -> None:
        """
        Method for training the random forest regression model.

        :param data: a list of [x, y] pairs to train the model on.
        :type data: list
        :param y: y parameters to train the model on. If None, the method will attempt to extract y values from the data parameter.
        :type y: list
        """

        # Reshape x to 2D array (required by scikit-learn)
        x = np.array([item[:-1] for item in data]).reshape(-1, 1)
        self._feature_length = x.shape[1]
        y = np.array([item[-1] for item in data])
        self.rfregressor.fit(x, y)
    
    def return_rf_model_prediction(self, data: List[list]) -> list:
        """
        Method for returning the predictions of the trained random forest regression model.

        :param data: x parameters to make predictions on.
        :type data: list
        :return: Predictions of the trained random forest regression model.
        :rtype: list
        """
        
        if self._feature_length is None:
            raise ValueError("Model has not been trained. Call train_rf() first.")
        
        # Extract features the same way as training (all but last element)
        x = np.array([item[:-1] for item in data]).reshape(-1, 1)
        
        if x.shape[1] != self._feature_length:
            raise ValueError(
            f"Feature dimension mismatch: expected {self._feature_length} features, "
            f"got {x.shape[1]}"
            )
        
        return self.rfregressor.predict(x)