from pydantic import BaseModel

# from typing import List


class OutputModel(BaseModel):
    """Sample Output Model"""

    response: str
