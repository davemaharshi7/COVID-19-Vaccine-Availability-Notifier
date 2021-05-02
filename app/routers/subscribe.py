from fastapi import APIRouter, HTTPException
from utils import Logger, INTERNAL_SERVER_ERROR_STRING, BACKEND_FILE_PATH
from models import (
    DistrictModel,
    PincodeModel,
    OutputModel,
)
from .crud import add_user_to_district, add_user_to_pincode


router = APIRouter()
logger = Logger()


@router.post("/district", response_model=OutputModel)
async def subscribe_via_district(input_data: DistrictModel):
    try:
        # Input data from JSON
        input_email = input_data.email
        input_district_id = input_data.district_id
        # Processing logic
        add_user_to_district(input_email, input_district_id)
        # API Response
        return OutputModel(
            response="Email: {} successfully subscribed.".format(input_email)
        )
    except HTTPException as ex:
        raise ex
    except Exception as ex:
        logger.exception(INTERNAL_SERVER_ERROR_STRING + ": " + str(ex))
        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR_STRING)


@router.post("/pincode", response_model=OutputModel)
async def subscribe_via_pincode(input_data: PincodeModel):
    try:
        # Input data from JSON
        input_email = input_data.email
        input_pincode = input_data.pincode
        # Processing logic
        add_user_to_pincode(input_email, input_pincode)
        # API Response
        return OutputModel(
            response="Email: {} successfully subscribed.".format(input_email)
        )
    except HTTPException as ex:
        raise ex
    except Exception as ex:
        logger.exception(INTERNAL_SERVER_ERROR_STRING + ": " + str(ex))
        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR_STRING)
