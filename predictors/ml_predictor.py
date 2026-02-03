from sklearn import linear_model

class MLPredictor:
    def __init__(self):
        self.model = linear_model.LinearRegression()
    
    def train(self, x: list, y: list):
        """
        Method for training the linear regression model.
        
        :param x: x parameters to train the model on.
        :type x: list
        :param y: y parameters to train the model on.
        :type y: list
        """
        self.model.fit(x, y)
    
    def return_model_coefficients(self) -> list:
        """
        Method for returning the coefficients of the trained model.
        
        :return: Coefficients of the trained model.
        :rtype: list
        """
        return self.model.coef_
    


