from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

import json
import sys

from service.main import pushToMessages

sys.path.insert(0, '..')

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
        print("MESSAGE SENDED")
        data = json.loads(text_data)
        pushToMessages(data)

    def chat_message(self, event):
        if event['information'] == "message":
            self.send(text_data=json.dumps({"message": event["message"], "typeMessage": event["typeMessage"], "type": event["information"], "from": event["from"]}))
            print("MESSAGE RECEIVED")
        else:
            self.send(text_data=json.dumps({"type": event["information"], "from": event["from"], "chunk": event["chunk"],  "max": event["max"]}))

