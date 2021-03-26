import slack

from django.conf import settings

class SlackMockup:
    """ Mockup slack api to testing """

    def __init__( self ):
        response = {
                "ok": True,
                "members": [
                    {
                        "id": "W012A3CDE",
                        "profile": {
                            "real_name": "Egon Spengler",
                            "email": "spengler@ghostbusters.example.com",
                        },
                        "is_admin": True,
                        }
                    ]
        }

        response_chat = {
                    "ok": True,
                    "channel": "C1H9RESGL",
                    "ts": "1503435956.000247",
                    "message": {
                        "text": "Here's a message for you",
                        "username": "ecto1",
                        "bot_id": "B19LU7CSY",
                        "attachments": [
                            {
                                "text": "This is an attachment",
                                "id": 1,
                                "fallback": "This is an attachment's fallback"
                            }
                        ],
                        "type": "message",
                        "subtype": "bot_message",
                        "ts": "1503435956.000247"
                    }
        }
        self.api_call_response = response
        self.chat_response = response_chat

    def api_call(self,list):
        """ Simulates api_call from slack api """
        return self.api_call_response

    def chat_postMessage(self,channel,text):
        """ Simulates method chat_postMessage from slack api """
        return self.chat_response

def get_client():
    """ Returns the real api or the mocked api based on settings.Testing variable """
    if settings.TESTING:
        return SlackMockup()
    else:
        return slack.WebClient(token=settings.BOT_USER_ACCESS_TOKEN)