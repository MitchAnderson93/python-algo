import numpy as np


class LinearRegression:
    def __init__(self, data):
        self.data = data

    def calculate_linear_regression(self):
        # Calculate linear regression coefficients
        x = self.data['Days'].values
        y = self.data['Close'].values
        model = np.polyfit(x, y, 1)
        slope = model[0]
        intercept = model[1]
        return slope, intercept
