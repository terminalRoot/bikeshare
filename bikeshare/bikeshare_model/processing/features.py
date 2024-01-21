from typing import List
import sys
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder

class WeekdayImputer(BaseEstimator, TransformerMixin):
    """ Impute missing values in 'weekday' column by extracting dayname from 'dteday' column """

    def __init__(self):
        # YOUR CODE HERE
        pass

    def fit(self, X, y=None):
        # YOUR CODE HERE
        return self

    def transform(self, X):
        # YOUR CODE HERE
        X = X.copy()
        nan_indices = X[X['weekday'].isnull()].index
        day_names = X.loc[nan_indices, 'dteday'].dt.day_name().str[:3]
        X.loc[nan_indices, 'weekday'] = day_names
        return X

class WeathersitImputer(BaseEstimator, TransformerMixin):
    """ Impute missing values in 'weathersit' column by replacing them with the most frequent category value """

    def __init__(self):
        # YOUR CODE HERE
        pass

    def fit(self, X, y=None):
        # YOUR CODE HERE
        self.most_frequent_category_ = X['weathersit'].mode().iloc[0]
        return self

    def transform(self, X):
        # YOUR CODE HERE
        X = X.copy()
        X['weathersit'].fillna(self.most_frequent_category_, inplace=True)
        return X
    

class Mapper(BaseEstimator, TransformerMixin):
    """
    Ordinal categorical variable mapper:
    Treat column as Ordinal categorical variable, and assign values accordingly
    """
    def __init__(self):
        # YOUR CODE HERE
        self.column_mappings = {
            'yr': {2011: 0, 2012: 1},
            'mnth': {'January': 1, 'February': 2, 'March': 3, 'April': 4,
                      'May': 5, 'June': 6, 'July': 7, 'August': 8,
                     'September': 9, 'October': 10, 'November': 11, 'December': 12},

            'season': {'spring': 1, 'summer': 2, 'fall': 3,  'winter': 4},
            'weathersit': {'Clear': 1, 'Mist': 2, 'Light Rain': 3, 'Heavy Rain': 4},
            'holiday': {'No': 0, 'Yes': 1},
            'workingday': {'No': 0, 'Yes': 1},
            'hr': {'12am': 0, '1am': 1, '2am': 2, '3am': 3, '4am': 4, '5am': 5,
                   '6am': 6, '7am': 7, '8am': 8, '9am': 9, '10am':  10,'11am':  11,
                   '12pm': 12, '1pm': 13, '2pm': 14, '3pm': 15, '4pm': 16, '5pm': 17,
                   '6pm': 18, '7pm': 19, '8pm': 20, '9pm':  21, '10pm': 22, '11pm':  23}
        }

    def fit(self, X, y=None):
        # YOUR CODE HERE
        return self

    def transform(self, X):
        # YOUR CODE HERE
        X = X.copy()
        # Apply mappings to each specified column
        for column, mapping in self.column_mappings.items():
            X[column] = X[column].map(mapping)

        return X
    


class OutlierHandler(BaseEstimator, TransformerMixin):
    """
    Change the outlier values:
        - to upper-bound, if the value is higher than upper-bound, or
        - to lower-bound, if the value is lower than lower-bound respectively.
    """

    def __init__(self, columns=None, lower_bound=None, upper_bound=None):
        # YOUR CODE HERE
        self.columns = columns
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def fit(self, X, y=None):
        # YOUR CODE HERE
        return self

    def transform(self, X):
      # YOUR CODE HERE
      X = X.copy()
      for colm in self.columns:
        # print(colm)
        q1 = X.describe()[colm].loc[self.lower_bound]
        q3 = X.describe()[colm].loc[self.upper_bound]
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        # print(f'lower_bound {lower_bound} upper_bound {upper_bound}')
        for i in X.index:
          if X.loc[i,colm] > upper_bound:
            X.loc[i,colm]= upper_bound
          if X.loc[i,colm] < lower_bound:
            X.loc[i,colm]= lower_bound
      return X
    

class WeekdayOneHotEncoder(BaseEstimator, TransformerMixin):
    """ One-hot encode weekday column """

    def __init__(self):
        # YOUR CODE HERE
        self.encoder = OneHotEncoder(sparse_output=False)

    def fit(self, X, y=None):
        # YOUR CODE HERE
        self.encoder.fit(X[['weekday']])
        self.columns = self.encoder.get_feature_names_out(['weekday'])
        return self

    def transform(self, X):
        # YOUR CODE HERE
        X = X.copy()
        weekday_encoded = self.encoder.transform(X[['weekday']])
        X[self.columns] = weekday_encoded
        return X
 

class DropColumns(BaseEstimator, TransformerMixin):

    """ Drop specified columns from the DataFrame """

    def __init__(self, columns):
      self.columns = columns

    def fit(self, X, y=None):
      return self

    def transform(self, X):
      X = X.copy()
      X = X.drop(self.columns, axis=1)
      return X
    

