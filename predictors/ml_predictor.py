from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.utils.validation import check_consistent_length
from typing import List, Optional
import numpy as np


class MLPredictor:
    def __init__(self):
        self.model = linear_model.LinearRegression()
        self.rfregressor = RandomForestRegressor(n_estimators=1, random_state=42, verbose=1)

    ## These are the linear regression methods

    def train(self, data: List[list], y: Optional[List[float | int]] = None) -> None:
        """
        Method for training the linear regression model.

        :param data: x and y parameters to train the model on.
        :type data: list
        :param y: y parameters to train the model on. If None, the method will attempt to extract y values from the data parameter.
        :type y: list
        """
        if not y:
            x = [item[0] for item in data]
            y = [item[1] for item in data]
        else:
            x = data

        try:
            check_consistent_length(x, y)
        except ValueError as e:
            raise ValueError(
                f"Inconsistent lengths: X has {len(x)} samples, but y has {len(y)} labels."
            ) from e

        self.model.fit(data, [i for i in range(len(data))])

    def return_model_coefficients(self) -> list:
        """
        Method for returning the coefficients of the trained model.

        :return: Coefficients of the trained model.
        :rtype: list
        """
        return self.model.coef_

    
    ## These are the random forest regression methods

    def train_rf(self, data: List[list], y: Optional[List[float | int]] = None) -> None:
        """
        Method for training the random forest regression model.

        :param data: x and y parameters to train the model on.
        :type data: list
        :param y: y parameters to train the model on. If None, the method will attempt to extract y values from the data parameter.
        :type y: list
        """
        if not y:
            x = [item[0] for item in data]
            y = [item[1] for item in data]
        else:
            x = data

        try:
            check_consistent_length(x, y)
        except ValueError as e:
            raise ValueError(
                f"Inconsistent lengths: X has {len(x)} samples, but y has {len(y)} labels."
            ) from e

        # Reshape x to 2D array (required by scikit-learn)
        x = np.array(x).reshape(-1, 1)
        self.rfregressor.fit(x, y)
    
    def return_rf_model_prediction(self, data: List[list]) -> list:
        """
        Method for returning the predictions of the trained random forest regression model.

        :param data: x parameters to make predictions on.
        :type data: list
        :return: Predictions of the trained random forest regression model.
        :rtype: list
        """
        # Extract first element from each data point and reshape to 2D
        x = [item[0] for item in data]
        x = np.array(x).reshape(-1, 1)
        return self.rfregressor.predict(x)