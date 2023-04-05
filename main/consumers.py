from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

import sys

sys.path.insert(0, '..')
from service.main import pushToMessages


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

    def receive(self, text_data=None, bytes_data=None):
        print(" MESSAGE RECEIVED")
        data = json.loads(text_data)
        message = data['message']
        pushToMessages(message)
        


    def chat_message(self, event):
        self.send(text_data=json.dumps({"message": event["message"], "from": event["from"]}))


