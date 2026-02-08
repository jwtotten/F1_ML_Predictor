from sklearn import linear_model
from sklearn.utils.validation import check_consistent_length
from typing import List, Optional, Union


class MLPredictor:
    def __init__(self):
        self.model = linear_model.LinearRegression()

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
