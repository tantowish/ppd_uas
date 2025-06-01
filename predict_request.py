from pydantic import BaseModel
from typing import Literal

class PredictRequest(BaseModel):
    gender: Literal["Male", "Female"] # gender
    age: int # age in years
    height: float  # height in cm
    weight: float  # weight in kg
    is_family_history_with_overweight: bool # family history with overweight
    favc: bool  # do you eat high calorie food
    fcvc: int  # do you eat vegetables?, normal input: 1-3
    ncp: int   # how many meals consumed daily?, normal input: 1-4
    caec: Literal["Frequently", "Sometimes", "no"] # do you eat any food between meals?
    smoke: bool # do you smoke?
    ch2o: float  # how many liters of water consumed daily?, normal input: 1-3
    scc: bool  # do you monitor your calories daily?
    faf: int  # how many physical activity?, normal input: 0-3
    tue: int  # time spent on technology use, normal input: 0-2
    calc: Literal["Frequently", "Sometimes", "no"] # do you consume alcohol?
    mtrans: Literal["Bike", "Motorbike", "Public Transportation", "Walking"] # mode of transportation