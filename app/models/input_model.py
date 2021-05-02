from pydantic import BaseModel

# from typing import List


class DistrictModel(BaseModel):
    """Subscribe API input with district ID"""

    email: str
    district_id: str


class PincodeModel(BaseModel):
    """Subscribe API input with Pincode"""

    email: str
    pincode: str
