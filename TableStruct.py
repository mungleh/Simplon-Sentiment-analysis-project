from typing import Optional
from pydantic import BaseModel

#struture table inputs
class bddinputs(BaseModel):
    input: Optional[str]
    prediction : Optional[int]
    probability : Optional[float]
    istrue : Optional[int]

#structure table test
class bddtest(BaseModel):
    id: Optional[int]
    review: Optional[str]
    rating: Optional[str]
