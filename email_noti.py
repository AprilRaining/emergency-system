import smtplib


def email_noti(receiver_name='',receiver_email='',request_list='',ref_ID=0,purpose=''):

    if receiver_email == "" or '@' not in receiver_email:
        return

    gmail_user = 'abidmore.auction@gmail.com'
    gmail_password = 'divdrhfnsvziilvs'

    sent_from = gmail_user
    to = [receiver_email]
    subject = 'New Request Created'
    body = ""
    if purpose == "add_req":
        req_coll = []
        for ind,val in enumerate(request_list):
            req_coll.append(f"{ind+1}. "+f"{val['task']} with volunteer ID {val['volunteer']} on {val['date']} during {val['workshift']} period")
        req_statement = "\n".join(req_coll)

        body = f"""
        Dear {receiver_name},
        
        Refugee ID: [{ref_ID}]

        You have created new request(s) to the volunteer(s). 
        Please see the details of your request(s) below:

        {req_statement}

        This will be a part of your schedule for this week.

        Best Regards,
        Emergency System Team K
        """
    elif purpose == "register":
        body = f"""
        Dear {receiver_name},

        You are successfully registered to our emergency system.
        
        Your ID is {ref_ID}. 
        
        Note: Please use this ID to inform our volunteers when you would 
        like to make change to your information or make request(s).

        Hope we could be your best companion during the hardest time.

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
        print(u"\U0001F4E7"+"Confirmation email sent successfully!")
    except Exception as ex:
        print("Refugee email address not found.")
        # print ("Something went wrong….",ex)