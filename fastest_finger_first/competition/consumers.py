import json

from .models import Allotment, Question
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

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
            question_number = int(text_data) + 1
            question = await self.get_question(question_number)
            print(question)

            # Send message to room group
            await self.channel_layer.group_send(
                "game", {
                    "type": "question",
                    "question": {
                        "question": question.question,
                        "option0": question.option0,
                        "option1": question.option1,
                        "option2": question.option2,
                        "option3": question.option3,
                        "number": question_number
                    }
                }
            )
        
        else:
            result = json.loads(text_data)
            print(result)
            if result["choice"] == "pick":
                await self.store_question(result["question"])
                await self.channel_layer.group_send(
                    "game", {"type": "result", "result": "picked", "user": self.scope['user'].username}
                )
            else:
                await self.channel_layer.group_send(
                    "game", {"type": "result", "result": "skipped", "user": self.scope['user'].username}
                )

    # Receive message from room group
    async def question(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"type": "question", "question": event["question"]}))

    async def result(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"type": "result", "result": event["result"], "user": event["user"]}))

    @database_sync_to_async
    def get_question(self, question_number):
        return Question.objects.get(pk=question_number)

    @database_sync_to_async
    def store_question(self, question):
        allotment, _ = Allotment.objects.get_or_create(user=self.scope['user'])
        questions = json.loads(allotment.questions)
        questions.append(question)
        allotment.questions = json.dumps(questions)
        allotment.save()
        