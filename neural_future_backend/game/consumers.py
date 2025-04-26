from channels.generic.websocket import AsyncJsonWebsocketConsumer


class PlayerConsumer(AsyncJsonWebsocketConsumer):
    GROUP_NAME = 'players'

    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()
            return

        self.user_id = self.scope['user'].id
        await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.GROUP_NAME, self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        """
        Ожидаем { "x": 123, "y": 456 }
        Добавляем user_id и отправляем всем
        """

        payload = {
            'type': 'player.position',
            'user_id': self.user_id,
        }
        payload.update(content)
        await self.channel_layer.group_send(self.GROUP_NAME, payload)

    async def player_position(self, event):
        if event["user_id"] == self.user_id:
            return
        del event["type"]
        await self.send_json(event)
