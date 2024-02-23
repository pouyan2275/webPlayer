import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class VideoConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):       
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        id = str(text_data_json['id'])
        if(command == 'pause' or command == 'play' ):
            async_to_sync(self.channel_layer.group_send)(id,
            {
                'command': command,
                'time': text_data_json['time'],
                'type':'receive_message',
            }
            )
        elif command == 'subtitle':
            pass
class ClientConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = str(self.scope['url_route']['kwargs']['id'])
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
    
    def receive_message(self, event):
        self.send(text_data=json.dumps(event))

    def send_movie_position(self, text_data,id):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        async_to_sync(self.channel_layer.group_send)(id,
            {
                'command': command,
                'time': text_data_json['time'],
            }
        )
        # text_data_json = json.loads(text_data)
        # command = text_data_json['command']
        # if(command == 'pause' or command == 'play' ):
        #     self.send(text_data=json.dumps({
        #         'command': command,
        #         'time': text_data_json['time'],
        #         'id': text_data_json['id'],
        #     }))
