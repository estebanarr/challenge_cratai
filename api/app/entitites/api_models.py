from xmlrpc.client import _datetime
from pydantic import BaseModel
from typing import List

class InputText(BaseModel):  
    text_description: List   

class Response(BaseModel):
    prob_label_0: float
    prob_label_1: float
    prediction_class: str
    api_version: str
    model_version: str


