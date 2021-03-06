# COVID-19 Vaccine Availability Notifier 🚀

🆕 Changes: Updated Co-WIN portal API as per the [Co-WIN API reference](https://apisetu.gov.in/public/marketplace/api/cowin/cowin-public-v2). If you are already using codebase, please fetch the latest changes. 

## Overview

This project developed for tracking COVID-19 vaccine slots available in your pincode and district for 18+ age category. Once available, it will send email notifications at periodic interval to subscribers until slots are available.

Note: The purpose of this project is help humanity in this covid crisis, where people can get vaccination slots easily and save their time.

## Prerequisites

- Python 3.6+

## How to use?

- Clone this project, open terminal under `/app` folder.
- Install the Python packages  
    `python -m pip install -r requirements.txt`  
    OR  
    `pip install -r requirements.txt`
- Configure sender's Email credentials - Create `/app/config.json` file for configurations.  
**Note**: This email credentials will be used to send email notification to subscribers. You may need to have [App passwords](https://support.google.com/accounts/answer/185833?p=InvalidSecondFactor&visit_id=637554658548216477-2576856839&rd=1) or "Less secure app access" turned on. 
```
{
    "email": "username@domain.com",
    "password": "YourSUPER@secretP@ssw0rd-Here",
    "logLevel": "INFO"
}
``` 

- Start the Uvicorn server  
    `python -m uvicorn main:app --port 8000`  
    OR  
    `uvicorn main:app --port 8000`
- Your API server Started 🚀
```
INFO:     Started server process [8408]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
- Navigate to Swagger UI docs - http://localhost:8000/api/docs  
This is the place you can manage subscribers list and much more...  
![Swagger Docs](https://github.com/davemaharshi7/COVID-19-Vaccine-Availability-Notifier/blob/main/swagger-docs-image.png?raw=true)
- To subscribe yourself to a particular pincode, hit the second enpoint `/api/subscribe/pincode` and enter your email-address and pincode to be checked.
```
{
  "email": "username@gmail.com",
  "pincode": "367005"
}
```
- You are done, sit back and relax, you will recieve email notification once slots are available ⚡⚡  
Example screenshot attached.
![Email Template](https://github.com/davemaharshi7/COVID-19-Vaccine-Availability-Notifier/blob/main/email_template.png?raw=true)

## Subscribe notification for district

- Make sure API server is running.
- One can subscribe to district via `/api/subscribe/district` and enter your email-address and district_id as:
```
{
  "email": "username@gmail.com",
  "district_id": "154"
}
```
- You can find your `district_id` by referring [link](https://github.com/davemaharshi7/COVID-19-Vaccine-Availability-Notifier/wiki/How-to-find-your-district_id%3F)

## Unsubscribe to Email Notification

- One can unsubscribe via POST: `/api/unsubscribe/reset` endpoint, resulting in removal of all subscribers.

## Features

- Developed with [Fast API](https://fastapi.tiangolo.com/)🚀
- Subscribe via District and Pincode, periodically polled to fetch available slots.
- Incase of errors, it is logged in separate logger file.


