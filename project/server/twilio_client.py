from twilio.rest import Client
class TwilioClient():
    def __init__(self):
        self.client = None
        
    def init_app(self, app):
        if ("SMS_CREDENTIALS" not in app.config):
            warnings.warn("SMS_CREDENTIALS required for SMS is not found")
        else:
            sms_creds = app.config["SMS_CREDENTIALS"]
            account_sid = sms_creds.split(":")[0]
            auth_token = sms_creds.split(":")[1]
            self.client = Client(account_sid, auth_token)
                 
    def sendMessage(self, to, frm, body):
        message = self.client.messages.create(
            to = to,
            from_ = frm,
            body = body
        )
        return message.sid
    
    