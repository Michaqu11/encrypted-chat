from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class WSConsumer(WebsocketConsumer):
    def connect(self):

        self.room_name = "chat"
        async_to_sync(self.channel_layer.group_add)(
           self.room_name, self.channel_name
        )

        self.accept()
        print("CONNECTED")

    def disconnect(self, close_code):
        self.channel_layer.group_discard( self.room_name, self.channel_name)
        print("DISCONNECED CODE: ", close_code)

    def chat_message(self, event):
        self.send(text_data=json.dumps({"message": event["message"], "from": event["from"]}))


