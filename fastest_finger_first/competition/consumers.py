import json

from channels.generic.websocket import AsyncWebsocketConsumer


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room group
        await self.channel_layer.group_add("game", self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard("game", self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        if self.scope["user"].is_staff:
            question = json.loads(text_data)
            print(question)

            # Send message to room group
            await self.channel_layer.group_send(
                "game", {"type": "question", "question": question}
            )
        
        else:
            result = json.loads(text_data)
            if result["choice"] == "pick":
                pick = f"picked by {self.scope['user'].username}"
                print(pick)
                await self.channel_layer.group_send(
                    "game", {"type": "result", "result": pick}
                )
            else:
                await self.send(text_data=json.dumps({"result": "skipped"}))

    # Receive message from room group
    async def question(self, event):
        message = event["question"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    async def result(self, event):
        message = event["result"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
        