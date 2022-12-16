import smtplib
from syslog import *


def notify_new_request(receiver_email,task_info,req_date,work_shift,ref_ID,vol_ID,receiver):

    if receiver_email == "" or '@' not in receiver_email:
        return

    gmail_user = 'abidmore.auction@gmail.com'
    gmail_password = 'divdrhfnsvziilvs'

    sent_from = gmail_user
    to = [receiver_email]
    subject = 'New Request Created'
    body = ""
    if receiver == "volunteer":
        body = f"""
        Dear Volunteer ID: [{vol_ID}],

        You have received a new task request({task_info}) from a refugee ID: [{ref_ID}] 
        on {req_date} for your {work_shift} work shift. 
        
        This will be a part of your schedule for this week.

        Best Regards,
        Emergency System Team K
        """
    elif receiver == "refugee":
        body = f"""
        Dear Refugee ID: [{ref_ID}],

        You have created a new request({task_info}) to a volunteer ID: [{vol_ID}] 
        on {req_date} during the {work_shift} shift.

        This will be a part of your schedule for this week.

        Best Regards,
        Emergency System Team K
        """


    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)