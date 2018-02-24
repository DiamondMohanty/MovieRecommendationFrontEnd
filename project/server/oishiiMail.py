# Importing the module
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 

class OishiiMailer():
    def __init__(self):
        # Setuo the SMTP server
        self.smtpObj = smtplib.SMTP(host='smtp.gmail.com', port=587)
    
    def init_app(self, app):
        if ("MAIL_CREDENTIALS" not in app.config):
            warnings.warn(
                'MAIL_CREDENTIALS not present in the Config'
            )
        else:
            creds = app.config["MAIL_CREDENTIALS"]
            username = creds.split(":")[0]
            password = creds.split(":")[1]
            self.smtpObj.ehlo()
            self.smtpObj.starttls()
            self.smtpObj.login(username, password)
        
    
    def sendSubscriptionMail(self, to, mealObj):
       
        
        # Creating the message body
        htmlMessage = """\
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8" />
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <title></title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                
                <style>
            
                    .footer {
                        color: gray;
                        font-size: 0.8em;
                    }
            
                    .container {
                        font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        width: 50%;
                        padding: 20px;
                        margin: 20px auto;
                        box-shadow: 2px 3px 3px 2px lightgray;
                    }
            
                    table  {
                        width: 100%;
                    }
            
                    table > tbody > tr:nth-child(2n+1) > td, table > tbody > tr:nth-child(2n+1) > th {
                        background-color: #f4f4f4;
                        padding: 5px;
                        font-weight: bold;
                    }
            
                    hr {
                        display: block;
                        height: 1px;
                        border: 0;
                        border-top: 1px solid #ccc;
                        margin: 1em 0;
                        padding: 0;
                    }
            
                    
            
            
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="row">
                        <div class="col-md-12">
                            <div class="header">
                                <img src="
                                https://firebasestorage.googleapis.com/v0/b/oishii-91c5e.appspot.com/o/oishiiLogo.png?alt=media&token=375c72f7-920f-462c-8206-d52c43253a73" class="img img-responsive" />
                            </div>
                            <div class="body">
                                <h1>Thank You</h1>
                                <p>
                                    You've sucessfully subscribed to Oishii meal services. 
                                </p>
                                <p><b>Details</b></p>
                                <table>
                                    <tr>
                                        <td>Name</td>
                                        <td>Meal Count</td>
                                        <td>Price</td>
                                    </tr>
                                    <tr>
                                        <td>"""+mealObj['mealName']+"""</td>
                                        <td>"""+mealObj['mealCount']+"""</td>
                                        <td>"""+mealObj['mealPrice']+"""</td>
                                    </tr>
                                    </table>
                                <hr />
                                <p><b>Login Details</b></p>
                                <p>
                                    <b>Username: </b> """+to+""" <br />
                                    <b>Password: </b> """ + to +""" <br />
                                    We request you to change your default password by visiting <a href="https://oishii.in/login">https://oishii.in/login</a>
                                </p>
                                <hr />
                                
                            </div>
                            <div class="footer">
                                DISCLAIMER: This e-mail and any file(s) transmitted with it, is intended for the exclusive use by the person(s) mentioned above as recipient(s). This e-mail may contain confidential information and/or information protected by intellectual property rights or other rights. If you are not the intended recipient of this e-mail, you are hereby notified that any dissemination, distribution, copying, or action taken in relation to the contents of and attachments to this e-mail is strictly prohibited and may be unlawful. If you have received this e-mail in error, please notify the sender and delete the original and any copies of this e-mail and any printouts immediately from your system and destroy all copies of it.
                            </div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        """         
        
         # Create a Message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Oishii Subscription Confirmation"
        msg["From"] = "support@oishii.com"
        msg["To"] = to
        message = MIMEText(htmlMessage, 'html')
        msg.attach(message)
        
        self.smtpObj.sendmail(msg['From'], to, msg.as_string())

        del msg
