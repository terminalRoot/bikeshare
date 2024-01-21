import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

from bikeshare_model.config.core import config
from bikeshare_model.processing.features import WeekdayImputer, WeathersitImputer
from bikeshare_model.processing.features import Mapper
from bikeshare_model.processing.features import OutlierHandler, WeekdayOneHotEncoder
from bikeshare_model.processing.features import DropColumns

bikeshare_pipe=Pipeline([
    ('weekday_imputer', WeekdayImputer()),         # Impute missing values in 'weekday' column
    ('weathersit_imputer', WeathersitImputer()),   # Impute missing values in 'weathersit' column
    ('mapper', Mapper()),             # Map categorical columns
    ('outlier_handler', OutlierHandler(columns=config.model_config.numerical_features, lower_bound='25%', upper_bound='75%')),  # Handle outliers in numerical columns
    ('weekday_onehot_encoder', WeekdayOneHotEncoder()),  # One-hot encode 'weekday' column
    ('drop_columns', DropColumns(columns=config.model_config.unused_fields)),  # Custom transformer to drop specified columns
    ('scaler', StandardScaler()),                  # Standardize numerical features
    ('regressor', RandomForestRegressor(n_estimators=config.model_config.n_estimators,
                                        max_depth=config.model_config.max_depth,
                                        random_state=config.model_config.random_state))              # Regression model (you can replace with your regressor)      
     ])