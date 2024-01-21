"""
Note: These tests will fail if you have not first trained the model.
"""
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import numpy as np
from sklearn.metrics import accuracy_score

from bikeshare_model.predict import make_prediction
from sklearn.metrics import mean_squared_error, r2_score

def test_make_prediction(sample_input_data):
    # Given
    expected_no_predictions = 3476

    # When
    result = make_prediction(input_data=sample_input_data)

    # Then
    predictions = result.get("predictions")
    assert isinstance(predictions, np.ndarray)
    assert isinstance(predictions[0], np.float64)
    assert result.get("errors") is None
    assert len(predictions) == expected_no_predictions
    _predictions = list(predictions)
    
    y_true = sample_input_data["cnt"]

    mse = mean_squared_error(_predictions, y_true)
    assert mse > 2700
    r2 = r2_score(_predictions, y_true)
    assert r2 > 0.8

