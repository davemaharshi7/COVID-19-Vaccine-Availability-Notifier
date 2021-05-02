import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .logger import Logger
from .configuration import Configurations


logger = Logger()
conf = Configurations()


def send_email(email_content, emails, flag):
    for user in emails:
        send_email_worker_function(email_content, user, flag)


def send_email_worker_function(email_content, receiver_email, flag):
    message = MIMEMultipart("alternative")
    if flag:
        subject = "COVID-19 Vaccine Slots Available in your district! Schedule Appointment ASAP🚀"
    else:
        subject = "COVID-19 Vaccine Slots Available in your locality! Schedule Appointment ASAP🚀"
    message["Subject"] = subject
    message["From"] = conf.email
    message["To"] = conf.password

    # contents
    availability_html_content =""
    availability_raw_content =""
    for element in email_content:
        location = element["center_district_name"] + ", " + element["center_state_name"]

        availability_html_content = availability_html_content + """<tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
        </tr>""".format(element["date"], location, element["center_name"], element["center_pincode"], element["center_fee_type"], element["center_min_age"], element["center_available_capacity"])
        availability_raw_content = availability_raw_content + "{} | {} | {} | {} | {} | {}\n".format(location, element["center_name"], element["center_pincode"], element["center_fee_type"], element["center_min_age"], element["center_available_capacity"])

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    COVID-19 Vaccine Slots available:
    {}
    """.format(availability_raw_content)
    html = """
    <html>
    <head>
    <style>
    table {{
        font-family: arial, sans-serif;
        border-collapse: collapse;
    }}
    td, th {{
        border: 1px solid #dddddd;
        text-align: left;
        padding: 4px;
    }}
    </style>
    </head>
    <body>
        <p>Hi,<br>
        COVID-19 Vaccine Slots available:
        <table>
        <tr>
            <th>Date</th>
            <th>City, State</th>
            <th>Center Name</th>
            <th>Pincode</th>
            <th>Fee type</th>
            <th>Minimum Age</th>
            <th>Availability</th>
        </tr>
        {}
        </table>
        <br>
        <p>You are reciving notification as you have subscribed to COVID-19 vaccination notifier.</p>
    </body>
    </html>
    """.format(availability_html_content)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
    logger.info("Email Sent successfully!")
