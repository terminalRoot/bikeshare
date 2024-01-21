from typing import Any, List, Optional

from pydantic import BaseModel
from bikeshare_model.processing.validation import DataInputSchema
from datetime import datetime

class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    #predictions: Optional[List[int]]
    predictions: Optional[int]


class MultipleDataInputs(BaseModel):
    inputs: List[DataInputSchema]

    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        'dteday': datetime.strptime("2012-11-05", "%Y-%m-%d"),
                        'season': "winter",
                        'hr': "6am",
                        'holiday': "No",
                        'weekday':"Mon",
                        'workingday': "Yes",
                        'weathersit': "Mist",
                        'temp': 6.1,
                        'atemp': 3.0014000000000003,
                        'hum': 49.0,
                        'windspeed': 19.0012,
                        'casual': 4,
                        'registered': 135,
                    }
                ]
            }
        }


# class MultipleDataInputs(BaseModel):
#     inputs: List[DataInputSchema]

#     class Config:
#         schema_extra = {
#             "example": {
#                 "inputs": [
#                     {
#                         "PassengerId": 79,
#                         "Pclass": 2,
#                         "Name": "Caldwell, Master. Alden Gates",
#                         "Sex": "male",
#                         "Age": 0.83,
#                         "SibSp": 0,
#                         "Parch": 2,
#                         "Ticket": "248738",
#                         "Cabin": 'A5',
#                         "Embarked": "S",
#                         "Fare": 29,
#                     }
#                 ]
#             }
#         }
