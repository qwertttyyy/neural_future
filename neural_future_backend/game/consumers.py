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
        x = content.get('x')
        y = content.get('y')
        if x is None or y is None:
            return

        await self.channel_layer.group_send(
            self.GROUP_NAME,
            {
                'type': 'player.position',
                'user_id': self.user_id,
                'x': x,
                'y': y,
            },
        )

    async def player_position(self, event):
        if event["user_id"] == self.user_id:
            return

        await self.send_json(
            {
                "user_id": event["user_id"],
                "x": event["x"],
                "y": event["y"],
            }
        )
