from random import randint
import numpy as np
from scipy.stats import norm
from sklearn.datasets.base import load_boston
from sklearn.model_selection import train_test_split

from skpro.base import ProbabilisticEstimator
from skpro.metrics import log_loss


class MyCustomModel(ProbabilisticEstimator):
    """ Estimator class that represents the probabilistic model"""

    class Distribution(ProbabilisticEstimator.Distribution):
        """ Distribution class returned by MyCustomModel.predict(X)

        self.estimator provides access to the parent
        ProbabilisticEstimator object, e.g. MyCustomModel
        self.X provides access to the test sample X
        """

        def point(self):
            """ Implements the point prediction """
            return np.ones((len(self.X), 1)) * self.estimator.random_mean_prediction_

        def std(self):
            """ Implements the variance prediction """
            return np.ones((len(self.X), 1)) * self.estimator.random_std_prediction_

        def pdf(self, x):
            """ Implements the pdf function """
            return norm.pdf(x, loc=self.point(), scale=self.std())

    def __init__(self):
        self.random_mean_prediction_ = None
        self.random_std_prediction_ = None

    def fit(self, X, y):
        # Generate random parameter estimates
        self.random_mean_prediction_ = randint(np.min(y), np.max(y))
        self.random_std_prediction_ = 0.2 * self.random_mean_prediction_

        return self


# Use custom model
model = MyCustomModel()

X, y = load_boston(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
y_pred = model.fit(X_train, y_train).predict(X_test)
print('Loss: %f+-%f' % log_loss(y_pred, y_test, return_std=True))