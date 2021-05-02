from fastapi import HTTPException
from utils import Logger, INTERNAL_SERVER_ERROR_STRING, BACKEND_FILE_PATH
import json

logger = Logger()
DISTRICT_KEY = "districts"
PINCODE_KEY = "pincodes"


def add_user_to_district(user_email, district_id):
    data = fetch_current_data()
    if district_id in data[DISTRICT_KEY]:
        # Already District ID added
        user_email_list = data[DISTRICT_KEY][district_id]
        if not isinstance(user_email_list, list):
            user_email_list = []
        if user_email in user_email_list:
            # User already added in file
            raise HTTPException(status_code=400, detail="User already subscribed")
        else:
            user_email_list.append(user_email)
            data[DISTRICT_KEY][district_id] = user_email_list
    else:
        data[DISTRICT_KEY][district_id] = [user_email]
    # writing updated File
    _write_file(BACKEND_FILE_PATH, data)


def add_user_to_pincode(user_email, pincode):
    data = fetch_current_data()
    if pincode in data[PINCODE_KEY]:
        # Already pincode added
        user_email_list = data[PINCODE_KEY][pincode]
        if not isinstance(user_email_list, list):
            user_email_list = []
        if user_email in user_email_list:
            # User already added in file
            raise HTTPException(status_code=400, detail="User already subscribed")
        else:
            user_email_list.append(user_email)
            data[PINCODE_KEY][pincode] = user_email_list
    else:
        data[PINCODE_KEY][pincode] = [user_email]
    # writing updated File
    _write_file(BACKEND_FILE_PATH, data)


def fetch_current_data():
    current_data = _read_file(BACKEND_FILE_PATH)
    if current_data is None:
        data = {
            DISTRICT_KEY: {},
            PINCODE_KEY: {},
        }
        _write_file(BACKEND_FILE_PATH, data)
        return data
    else:
        return current_data


def reset_file():
    data = {
        DISTRICT_KEY: {},
        PINCODE_KEY: {},
    }
    _write_file(BACKEND_FILE_PATH, data)


def get_districts():
    data = fetch_current_data()
    return data[DISTRICT_KEY].keys()


def get_email_from_district_id(district_id):
    data = fetch_current_data()
    return data[DISTRICT_KEY][district_id]


def get_pincode():
    data = fetch_current_data()
    return data[PINCODE_KEY].keys()


def get_email_from_pincode(pin):
    data = fetch_current_data()
    return data[PINCODE_KEY][pin]


def delete_user_from_district(user_email, district_id):
    data = fetch_current_data()
    if district_id in data[DISTRICT_KEY]:
        # Already District ID exist
        user_email_list = data[DISTRICT_KEY][district_id]
        if not isinstance(user_email_list, list):
            user_email_list = []
        if user_email in user_email_list:
            # User already added in file - removing it
            user_email_list.remove(user_email)
            data[DISTRICT_KEY][district_id] = user_email_list
        else:
            # user doesnot exists in file - raise error
            raise HTTPException(status_code=400, detail="User already unsubscribed")
    else:
        # Input district ID not found
        raise HTTPException(status_code=400, detail="Input District ID not found!")
    # writing updated File
    _write_file(BACKEND_FILE_PATH, data)


def delete_user_from_pincode(user_email, pincode):
    data = fetch_current_data()
    if pincode in data[PINCODE_KEY]:
        # Already Pincode exist
        user_email_list = data[PINCODE_KEY][pincode]
        if not isinstance(user_email_list, list):
            user_email_list = []
        if user_email in user_email_list:
            # User already added in file - removing it
            user_email_list.remove(user_email)
            data[PINCODE_KEY][pincode] = user_email_list
        else:
            # user doesnot exists in file - raise error
            raise HTTPException(status_code=400, detail="User already unsubscribed")
    else:
        # Input Pincode not found
        raise HTTPException(status_code=400, detail="Input Pincode not found!")
    # writing updated File
    _write_file(BACKEND_FILE_PATH, data)


def _read_file(file_name):
    try:
        with open(file_name, "r") as config:
            data = json.load(config)
            return data
    except OSError as oserr:
        logger.exception(str(oserr))
        return None
    except Exception as ex:
        logger.exception(str(ex))
        return None


def _write_file(file, json_data):
    try:
        with open(file, "w") as f:
            json.dump(json_data, f)
            return True
    except OSError as oserr:
        logger.exception(str(oserr))
        return False
    except Exception as ex:
        logger.exception(str(ex))
        return False
