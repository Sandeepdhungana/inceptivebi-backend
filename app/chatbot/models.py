from app.extensions import lex_client
import os

class ChatBot:
    def __init__(self) -> None:
        pass

    def chat(self, user_message):
        try:
            response = lex_client.recognize_text(
                botId=os.getenv('BOT_ID'),
                botAliasId=os.getenv('BOT_ALIAS_ID'),
                localeId='en_US',
                sessionId='1234',
                text=user_message
            )
            reply = response.get('messages')
            return reply, response
        except Exception as e:
            print("Some error occured while processing chat ", e)
