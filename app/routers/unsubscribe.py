from fastapi import APIRouter, HTTPException
from utils import Logger, INTERNAL_SERVER_ERROR_STRING, BACKEND_FILE_PATH
from models import (
    DistrictModel,
    PincodeModel,
    OutputModel,
)
from .crud import delete_user_from_district, delete_user_from_pincode, reset_file


router = APIRouter()
logger = Logger()


@router.post("/district", response_model=OutputModel)
async def unsubscribe_via_district(input_data: DistrictModel):
    try:
        # Survey data from JSON
        input_email = input_data.email
        input_district_id = input_data.district_id
        # Processing logic
        delete_user_from_district(input_email, input_district_id)
        # API Response
        return OutputModel(
            response="Email: {} successfully unsubscribed.".format(input_email)
        )
    except HTTPException as ex:
        raise ex
    except Exception as ex:
        logger.exception(INTERNAL_SERVER_ERROR_STRING + ": " + str(ex))
        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR_STRING)


@router.post("/pincode", response_model=OutputModel)
async def unsubscribe_via_pincode(input_data: PincodeModel):
    try:
        # Survey data from JSON
        input_email = input_data.email
        input_pincode = input_data.pincode
        # Processing logic
        delete_user_from_pincode(input_email, input_pincode)
        # API Response
        return OutputModel(
            response="Email: {} successfully unsubscribed.".format(input_email)
        )
    except HTTPException as ex:
        raise ex
    except Exception as ex:
        logger.exception(INTERNAL_SERVER_ERROR_STRING + ": " + str(ex))
        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR_STRING)


@router.post("/reset", response_model=OutputModel)
async def unsubscribe_from_all():
    try:
        # Processing logic
        reset_file()
        # API Response
        return OutputModel(response="All subscription reset.")
    except HTTPException as ex:
        raise ex
    except Exception as ex:
        logger.exception(INTERNAL_SERVER_ERROR_STRING + ": " + str(ex))
        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR_STRING)
