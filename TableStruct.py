from typing import Optional
from pydantic import BaseModel

#struture table inputs
class bddinputs(BaseModel):
    title: Optional[str]
    feature : Optional[str]
    prediction : Optional[str]

#structure table test
class bddtest(BaseModel):
    id: Optional[int]
    review: Optional[str]
    rating: Optional[str]
