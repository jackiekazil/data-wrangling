from twilio.rest import TwilioRestClient
import ConfigParser


def send_text(sender, recipient, text_message, config=None):
    if not config:
        config = ConfigParser('config/development.cfg')

    client = TwilioRestClient(config.get('twilio', 'account_sid'),
                              config.get('twilio', 'auth_token'))
    sms = client.sms.messages.create(body=text_message,
                                      to=recipient,
                                      from_=sender)

def example():
    send_text("+11008675309", "+11088675309", "JENNY!!!!")
