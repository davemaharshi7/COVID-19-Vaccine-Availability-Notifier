"""Main file declaring router and startup events."""
from fastapi import FastAPI, Request
from utils import (
    Logger,
    API_PREFIX,
    API_TITLE,
    API_VERSION,
    API_DOCS_URL,
    send_email,
    MIN_AGE_LIMIT,
    POLL_INTERVAL,
)
from routers import (
    subscribe,
    get_districts,
    get_email_from_district_id,
    get_email_from_pincode,
    get_pincode,
    unsubscribe,
)
from fastapi_utils.tasks import repeat_every
import requests
from datetime import date


logger = Logger()
URL_DISTRICT = (
    "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict"
)
URL_PINCODE = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByPin"

# App declaration
app = FastAPI(title=API_TITLE, version=API_VERSION, docs_url=API_PREFIX + API_DOCS_URL)

# API Routers
app.include_router(
    subscribe.router, tags=["Subscribe"], prefix=API_PREFIX + "/subscribe"
)
app.include_router(
    unsubscribe.router, tags=["Unsubscribe"], prefix=API_PREFIX + "/unsubscribe"
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """To log every request to log file.

    Args:
        request (fastapi.Request): Request object containing metadata about request
        call_next : call to next route-path

    Returns:
        dict: Response from the API route
    """
    logger.debug(f"Requested {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"{request.method} {request.url} returned code={response.status_code}")
    return response


@app.on_event("startup")
@repeat_every(seconds=POLL_INTERVAL)
def check_vaccine_availability():
    """To check vaccine availability.

    Returns:
        Sends Email to notifier list.
    """
    logger.info("Check Vaccine availability periodic function called.")
    today = date.today()
    current_date = today.strftime("%d-%m-%Y")
    for ids in get_districts():
        param = dict(district_id=ids, date=current_date)
        resp = requests.get(url=URL_DISTRICT, params=param)
        logger.info("API call to get vaccine slots by district id - {}".format(ids))
        data = resp.json()
        _parse_json_response_to_check_vaccine_availablity(data, ids, True)
    for ids in get_pincode():
        param = dict(pincode=ids, date=current_date)
        resp = requests.get(url=URL_PINCODE, params=param)
        logger.info("API call to get vaccine slots by pincode - {}".format(ids))
        data = resp.json()
        _parse_json_response_to_check_vaccine_availablity(data, ids, False)


@app.on_event("shutdown")
def shutdown_event():
    """To log server shutdown events."""
    logger.info("API server stopped.")


# Default Router
@app.get("/", tags=["Root"])
async def default_route():
    """To route to main.

        This is default router which sends welcome message.

    Returns:
        dict: Welcome message and current API version
    """
    return {"message": "Welcome to {}!".format(API_TITLE), "version": API_VERSION}


def _parse_json_response_to_check_vaccine_availablity(json_data, id, flag):
    try:
        logger.debug(json_data)
        available_centers = []
        if "centers" in json_data:
            center_objects_array = json_data["centers"]
            for center in center_objects_array:
                if "sessions" in center:
                    center_session_details_array = center["sessions"]
                    for session in center_session_details_array:
                        if (
                            session["min_age_limit"] == MIN_AGE_LIMIT
                            and session["available_capacity"] > 0
                        ):
                            relevent_center_details = {
                                "date": session["date"],
                                "center_name": center["name"],
                                "center_state_name": center["state_name"],
                                "center_district_name": center["district_name"],
                                "center_pincode": center["pincode"],
                                "center_fee_type": center["fee_type"],
                                "center_min_age": session["min_age_limit"],
                                "center_available_capacity": session[
                                    "available_capacity"
                                ],
                            }
                            available_centers.append(relevent_center_details)
        logger.info(
            "Periodic invocation returned {} results".format(
                str(len(available_centers))
            )
        )
        if len(available_centers) > 0:
            if flag:
                email_list = get_email_from_district_id(id)
            else:
                email_list = get_email_from_pincode(id)
            send_email(available_centers, email_list, flag)
    except Exception as ex:
        logger.exception(str(ex))
