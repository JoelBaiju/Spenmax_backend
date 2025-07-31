import json
from channels.generic.websocket import AsyncWebsocketConsumer , WebsocketConsumer
from channels.db import database_sync_to_async

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.user = self.scope["user"]
        print(self.scope)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'notification_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'notification_message',
                'increment': 1
            }
        )

    async def notification_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'increment': 1
        }))


class NotificationRVM(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        # if user.is_authenticated and 
        self.room_name = "RVM"
        self.room_group_name = 'Notification_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def notification_RVM(self, event):
        number = event['increment']

        await self.send(text_data=json.dumps({
            'increment': number
        }))


class NotificationUser(AsyncWebsocketConsumer):
    
    async def connect(self):
        
        self.room_name = "AUU"
        self.room_group_name = 'Notification_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def notification_AUU(self, event):
        number = event['increment']

        await self.send(text_data=json.dumps({
            'increment': number
        }))



