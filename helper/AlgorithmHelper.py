# import math
import numpy as np
from scipy.stats import norm
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
import seaborn as sns

def mk_test(x, alpha=0.05):
    n = len(x)

    # calculate S
    s = 0
    for k in range(n - 1):
        for j in range(k + 1, n):
            s += np.sign(x[j] - x[k])

    # calculate the unique data
    unique_x, tp = np.unique(x, return_counts=True)
    g = len(unique_x)

    # calculate the var(s)
    if n == g:  # there is no tie
        var_s = (n * (n - 1) * (2 * n + 5)) / 18
    else:  # there are some ties in data
        var_s = (n * (n - 1) * (2 * n + 5) - np.sum(tp * (tp - 1) * (2 * tp + 5))) / 18

    if s > 0:
        z = (s - 1) / np.sqrt(var_s)
    elif s < 0:
        z = (s + 1) / np.sqrt(var_s)
    else:  # s == 0:
        z = 0

    # calculate the p_value
    # p = 2 * (1 - norm.cdf(abs(z)))  # two tail test
    h = abs(z) > norm.ppf(1 - alpha / 2)

    if (z < 0) and h:
        trend = 'decreasing'
    elif (z > 0) and h:
        trend = 'increasing'
    else:
        trend = 'no trend'

    return trend

def NonlinearRegressionFitting(x_train=[[6], [8], [10], [14], [18]], y_train=[[6], [8], [10], [14], [18]], x_test=[[6], [8], [11], [16]], y_test=[[8], [12], [15], [18]]):
    sns.set()

    # X_train = [[6], [8], [10], [14], [18]]
    # y_train = [[6], [8], [10], [14], [18]]
    # X_test = [[6], [8], [11], [16]]
    # y_test = [[8], [12], [15], [18]]

    # 简单线性回归
    model = LinearRegression()
    model.fit(x_train, y_train)
    xx = np.linspace(x_train[0][0], x_train[len(x_train) - 1][0] + 5, 100)
    yy = model.predict(xx.reshape(xx.shape[0], 1))
    plt.scatter(x=x_train, y=y_train, color='k')
    plt.plot(xx, yy, '-g')

    # 多项式回归
    quadratic_featurizer = PolynomialFeatures(degree=2)
    X_train_quadratic = quadratic_featurizer.fit_transform(x_train)
    X_test_quadratic = quadratic_featurizer.fit_transform(x_test)
    model2 = LinearRegression()
    model2.fit(X_train_quadratic, y_train)
    xx2 = quadratic_featurizer.transform(xx[:, np.newaxis])
    yy2 = model2.predict(xx2)
    plt.plot(xx, yy2, '-r')

    print('X_train:\n', x_train)
    print('X_train_quadratic:\n', X_train_quadratic)
    print('X_test:\n', x_test)
    print('X_test_quadratic:\n', X_test_quadratic)
    print('简单线性回归R2：', model.score(x_test, y_test))
    print('二次回归R2：', model2.score(X_test_quadratic, y_test))
    plt.show()

def show_data(x_data=[1, 2, 3], y_data=[1, 2, 3]):
    plt.scatter(x=x_data, y=y_data, color='k')
    plt.show()