from typing import Optional
from pydantic import BaseModel

#struture table inputs
class bddinputs(BaseModel):
    id: Optional[int]
    QUARTER : Optional[int]
    MONTH : Optional[int]

#structure table test
class bddtest(BaseModel):
    id: Optional[int]
    review: Optional[str]
    rating: Optional[str]
